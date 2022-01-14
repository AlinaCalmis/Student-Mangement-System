import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r'C:\oracle\instantclient_21_3')

class OracleConnection:

    def __init__(self, host, port, schema, username, password):
        self.host = host
        self.port = port
        self.schema = schema
        self.username = username
        self.password = password

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

    def dumpobject (self,obj, prefix=""):
        if obj.type.iscollection:
            print(prefix, "[")
            for value in obj.aslist():
                if isinstance(value, cx_Oracle.Object):
                    self.dumpobject(value, prefix + "  ")
                else:
                    print(prefix + "  ", repr(value))
            print(prefix, "]")
        else:
            print(prefix, "{")
            for attr in obj.type.attributes:
                value = getattr(obj, attr.name)
                if isinstance(value, cx_Oracle.Object):
                    print(prefix + "   " + attr.name + ":")
                    self.dumpobject(value, prefix + "  ")
                else:
                    print(prefix + "   " + attr.name + ":", repr(value))
            print(prefix, "}")

    def getProfessorData(self, profId):
        try:
            # salLow = self.cursor.var(cx_Oracle.NUMBER)
            # salHigh = self.cursor.var(cx_Oracle.NUMBER)
            # avgVenit = self.cursor.callfunc("pck_example.exemplu_functie", cx_Oracle.NUMBER, [jobId, salLow, salHigh])
            return_type = self.db.gettype('FUNCTIONS_PCK.PROF_DATA')
            result = self.cursor.callfunc("functions_pck.getProfessorData", return_type, (profId,))

            # verifica daca e colectie, in alt caz obj.type.attributes
            # print(result.type.iscollection)
            print(self.dumpobject(result))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    oc = OracleConnection('localhost', 1521, 'xe', 'system', 'Unudoitrei.123')
    oc.openConnection()
    # oc.addCourse(11, 'Sisteme de Prelucrare Grafica', 6, 15)
    oc.getProfessorData(8)
    oc.closeConnection()