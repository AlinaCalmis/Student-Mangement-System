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

    def getProfessorData(self, profId):
        try:
            return_type = cx_Oracle.DB_TYPE_VARCHAR
            fullName = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            phone = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            email = self.cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
            dept = self.cursor.callfunc("functions_pck.getProfData", return_type, (int(profId), fullName, phone, email))

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
            dept = self.cursor.callfunc("functions_pck.getProfData", return_type,
                                        (studId, fullName, phone, email, addr, sex, year))

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
        print("In main, this is your uid ", uid, " and type of it is ", type(uid), int(uid))
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.isUserRegistered", return_type, (int(uid),))
            print("Result: ", result)
            return result
        except cx_Oracle.DatabaseError as e:
            print("error is here: ", e)

    def checkPasswd(self, uid, passwd):
        return_type = cx_Oracle.DB_TYPE_BOOLEAN
        result = self.cursor.callfunc("functions_pck.checkPasswd", return_type, (int(uid), passwd))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!   ", result)
        return result

    def userType(self, uid):
        return_type = cx_Oracle.DB_TYPE_VARCHAR
        result = self.cursor.callfunc("functions_pck.userType", return_type, (int(uid),))
        return result

    def loadUser(self, uid):
        self.cursor.callproc("procedures_pck.loginUser", (int(uid),))

    def logoutUser(self, uid):
        self.cursor.callproc("procedures_pck.logoutUser", (int(uid),))

    def showDepartments(self):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.showDepts", (cursor,))
        depts_c = cursor.fetchall()
        depts = [list(c) for c in depts_c]
        print(depts)
        cursor.close()
        return depts

    def getAllInfoStudent(self, id):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.getAllInfoStudent", (id, cursor))
        depts_c = cursor.fetchall()
        info = [list(c) for c in depts_c]
        print(info)
        cursor.close()
        return info

    def getAllInfoProf(self, id):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.getAllInfoProf", (id, cursor))
        depts_c = cursor.fetchall()
        info = [list(c) for c in depts_c]
        print(info)
        cursor.close()
        return info

    def getAllInfoDept(self, id):

        return_type = cx_Oracle.DB_TYPE_NUMBER
        cursor = self.db.cursor()
        nprof = self.cursor.callfunc("functions_pck.doCountProfInDept", return_type, (id, cursor))
        nstud = self.cursor.callfunc("functions_pck.doCountStudentsInDept", return_type, (id,))
        dept_c = cursor.fetchall()
        info = [list(c) for c in dept_c]
        print(info)
        info[0].extend([int(nstud), int(nprof)])
        print(nstud, nprof, info)
        return info

    def removeDept(self, id):
        self.cursor.callproc("procedures_pck.removeDepartment", (id,))
        self.db.commit()

    def addDept(self, id, name):
        self.cursor.callproc("procedures_pck.addDepartment", (id, name))
        self.db.commit()

    def checkDept(self, id, name):
        return_type = cx_Oracle.DB_TYPE_BOOLEAN
        return self.cursor.callfunc("functions_pck.checkDept", return_type, (id, name))

    def showProfessors(self):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.showProfessors", (cursor,))
        profs_c = cursor.fetchall()
        # cursor.close()
        profs = [list(p) for p in profs_c]
        return profs

    def removeProf(self, id):
        self.cursor.callproc("procedures_pck.removeProfessor", (id,))
        self.db.commit()

    def addProfessor(self, cnp, fn, ln, bd, phone, email, password, gen, dept):
        try:
            self.cursor.callproc("procedures_pck.addProfessor", (0, cnp, fn, ln, bd, phone, email, password, gen, dept))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def removeCourseProf(self, prof_id, course_id):
        self.cursor.callproc("procedures_pck.removeGivenCourse", (course_id, prof_id))
        self.db.commit()

    def addCourseProf(self, prof_id, course_id):
        self.cursor.callproc("procedures_pck.addGivenCourse", (course_id, prof_id))
        self.db.commit()

    def showProfCourses(self, prof_id):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.showProfCourses", (cursor,))
        course_c = cursor.fetchall()
        cursor.close()
        courses_ids = [list(p) for p in course_c]
        courses_names = self.showCourses()

        final = []
        for c in courses_names:
            for cid in courses_ids:
                if c[0] == cid[0] and cid[1] == prof_id:
                    final.append([c[0], c[1]])

        return final

    def showCourses(self):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.showCourses", (cursor,))
        # print(cursor.fetchall())
        courses_c = cursor.fetchall()
        courses = [list(c) for c in courses_c]
        cursor.close()
        return courses

    def showOneCourse(self, course_id):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.getCourseData", (course_id, cursor))
        course_c = cursor.fetchall()
        cursor.close()
        courses = [list(p) for p in course_c]
        print(courses)
        return courses

    def addCourse(self, cn, cp, u):
        try:
            self.cursor.callproc("procedures_pck.addCourse", (1, cn, cp, u))
            self.db.commit()
            return True
        except Exception as e:
            return False

    def removeCourse(self, course_id):
        self.cursor.callproc("procedures_pck.removeCourse", (course_id,))
        self.db.commit()

    def showStudents(self, mode):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.showStudents", (mode, cursor))
        stud_c = cursor.fetchall()
        students = [list(s) for s in stud_c]
        return students

    def showStudyYears(self):
        cursor = self.db.cursor()
        self.cursor.callproc("procedures_pck.studyYears", (cursor,))
        study_c = cursor.fetchall()
        years = list(s for s in study_c)
        print(years)
        return years

    def showStudGender(self):
        return_type = cx_Oracle.DB_TYPE_NUMBER
        cursor = self.db.cursor()
        fem = self.cursor.callfunc("functions_pck.studGender", return_type, (cursor,))
        gender_c = cursor.fetchall()
        gender = [list(s) for s in gender_c]
        men = self.cursor.callfunc("functions_pck.countMen", return_type, ('stud',))
        gender[0].append(int(men))
        gender[1].append(int(fem))
        print(gender, fem, men),
        return gender

    def showStudCourses(self, stud_id):
        try:
            cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showStudCourses", (stud_id, cursor))
            courses_c = cursor.fetchall()
            courses = [list(c) for c in courses_c]
            print("Show Stud Courses", courses, stud_id)

            final = []
            for c in courses:
                if c[-1] == stud_id:
                    final.append(c)

            print(final)
            return final
        except cx_Oracle.DatabaseError as e:
            print(e)

    def addCourseStud(self, stud_id, course_id):
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.addCourseStud", return_type, (stud_id, course_id))
            self.db.commit()
            print("ADDING COURSE", result, stud_id, course_id)
            return result
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False

    def updateCourseStud(self, stud_id, course_id, grade):
        try:
            self.cursor.callproc("procedures_pck.updateCourseStud", (stud_id, course_id, grade))
            self.db.commit()
        except cx_Oracle.DatabaseError as e:
            print(e)

    def removeCourseStudent(self, stud_id, course_id):
        try:
            self.cursor.callproc("procedures_pck.removeStudRecord", (stud_id, course_id))
            self.db.commit()
        except cx_Oracle.DatabaseError as e:
            print(e)

    def addStudent(self, cnp, f, l, bd, phone, email, passwd, add, gender, enr, year, dept):
        try:
            self.cursor.callproc("procedures_pck.addStudent",
                                 (0, cnp, f, l, bd, phone, email, passwd, add, gender,
                                  enr, int(year), int(dept)))
            return True
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False


if __name__ == "__main__":
    oc = OracleConnection('localhost', 1521, 'xe', 'system', 'Unudoitrei.123')
    oc.openConnection()
    # oc.addCourse(11, 'Sisteme de Prelucrare Grafica', 6, 15)
    # oc.getProfessorData(8)
    # oc.isUserRegistered("1")
    oc.closeConnection()
