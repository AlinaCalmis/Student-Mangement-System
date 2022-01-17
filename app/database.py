import cx_Oracle
# cx_Oracle.init_oracle_client(lib_dir=r'C:\oracle\instantclient_21_3')
cx_Oracle.init_oracle_client(lib_dir=r'C:\Program Files (x86)\instantclient_21_3')

class OracleConnection:

    def __init__(self, host, port, schema, username, password):
        self.host = host
        self.port = port
        self.schema = schema
        self.username = username
        self.password = password
        self.cursor = None

    def openConnection(self):
        try:
            dsn_tns = cx_Oracle.makedsn(self.host, self.port, self.schema)
            self.db = cx_Oracle.connect(self.username, self.password, dsn_tns)
            # self.db = cx_Oracle.connect(self.username, self.password, dsn="localhost:1521/xe")
            self.cursor = self.db.cursor()
            print("Connection open!")
        except Exception as e:
            print("Connection not open!")
            print(e)

    def closeConnection(self):
        try:
            self.cursor.close()
            self.db.close()
            print("Connection close!")
        except Exception as e:
            print("Connection not closed!")
            print(e)

    def addCourse(self, c_id, c_n, c_p, u):
        try:
            self.cursor.callproc("procedures_pck.addCourse", (c_id, c_n, c_p, u))
            self.cursor.execute('select * from courses')
            res = self.cursor.fetchall()
            print(res)
            self.db.commit()
            # numeDept = self.cursor.var(cx_Oracle.STRING)
            # angajati = self.cursor.var(cx_Oracle.CURSOR)
            # self.cursor.callproc("pck_example.exemplu_procedura", [idDept, numeDept, angajati])
            # for elem in angajati.getvalue():
            #     print(elem[0], elem[1].strftime("%Y-%m-%d"), elem[2], elem[3], numeDept.getvalue())
        except Exception as e:
            print(e)

    def getProfessorData(self, profId):
        try:
            return_type = cx_Oracle.DB_TYPE_VARCHAR
            fullName = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            phone = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            email = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            dept = self.cursor.callfunc("functions_pck.getProfData", return_type, (int(profId),fullName,phone,email))

            result = {'Name': fullName.getvalue(),
                      'Phone': phone.getvalue(),
                      'Email': email.getvalue(),
                      'DeptName': dept
                      }
            print(result)
            return result
        except Exception as e:
            print(e)

    def getStudentData(self, studId):
        try:
            return_type = cx_Oracle.DB_TYPE_VARCHAR
            fullName = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            phone = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            email = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            addr = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            sex = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            year = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            dept = self.cursor.callfunc("functions_pck.getProfData", return_type, (studId,fullName,phone,email, addr,sex,year))

            result = {'Name': fullName.getvalue(),
                      'Phone': phone.getvalue(),
                      'Email': email.getvalue(),
                      'Address': addr,
                      'Sex': sex,
                      'StudyYear': year,
                      'DeptName': dept
                      }
            print(result)
            return result
        except cx_Oracle.DatabaseError as e:
            print(e)

    def isUserRegistered(self, uid):
        print("In main, this is your uid ",uid, " and type of it is ", type(uid),int(uid))
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.isUserRegistered", return_type, (int(uid),))
            print("Result: ", result)
            return result
        except cx_Oracle.DatabaseError as e:
            print("error is here: ",e)


    def checkPasswd(self, uid, passwd):
        return_type = cx_Oracle.DB_TYPE_BOOLEAN
        result = self.cursor.callfunc("functions_pck.checkPasswd", return_type, (int(uid), passwd))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!   ", result)
        return result

    def userType(self,uid):
        return_type= cx_Oracle.DB_TYPE_VARCHAR
        result = self.cursor.callfunc("functions_pck.userType", return_type,(int(uid), ))
        return result

    def loadUser(self,uid):
        self.cursor.callproc("procedures_pck.loginUser", (int(uid), ))

    def logoutUser(self, uid):
        self.cursor.callproc("procedures_pck.logoutUser", (int(uid), ))

    def showCourses(self):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.showCourses", (cursor, ))
        # print(cursor.fetchall())
        courses_c = cursor.fetchall()
        courses = [list(c) for c in courses_c]
        cursor.close()
        return courses

if __name__ == "__main__":
    oc = OracleConnection('localhost', 1521, 'xe', 'system', 'Unudoitrei.123')
    oc.openConnection()
    # oc.addCourse(11, 'Sisteme de Prelucrare Grafica', 6, 15)
    # oc.getProfessorData(8)
    # oc.isUserRegistered("1")
    oc.closeConnection()