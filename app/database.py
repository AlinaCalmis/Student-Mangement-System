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

    def isUserRegistered(self, uid):
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.isUserRegistered", return_type, (int(uid),))
            return result
        except cx_Oracle.DatabaseError as e:
            print("error is here: ", e)

    def checkPasswd(self, uid, passwd):
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.checkPasswd", return_type, (int(uid), passwd))
            return result
        except cx_Oracle.DatabaseError as e:
            print(e)

    def userType(self, uid):
        try:
            return_type = cx_Oracle.DB_TYPE_VARCHAR
            result = self.cursor.callfunc("functions_pck.userType", return_type, (int(uid),))
            return result
        except cx_Oracle.DatabaseError as e:
            print(e)

    def loadUser(self, uid, ut):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.loginUser", (int(uid), ut, new_cursor))
            self.db.commit()
            data_c = new_cursor.fetchall()
            data = [list(d) for d in data_c]
            new_cursor.close()
            return True, data
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False, []

    def logoutUser(self, uid):
        try:
            self.cursor.callproc("procedures_pck.logoutUser", (int(uid), ))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError:
            return False

    def showDepartments(self):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showDepts", (new_cursor, ))
            depts_c = new_cursor.fetchall()
            depts = [list(c) for c in depts_c]
            new_cursor.close()
            return depts
        except cx_Oracle.DatabaseError as e:
            print(e)

    def getAllInfoStudent(self, uid):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.getAllInfoStudent", (uid, new_cursor))
            depts_c = new_cursor.fetchall()
            info = [list(c) for c in depts_c]
            new_cursor.close()
            return info
        except cx_Oracle.DatabaseError as e:
            print(e)

    def getAllInfoProf(self, uid):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.getAllInfoProf", (uid, new_cursor))
            depts_c = new_cursor.fetchall()
            info = [list(c) for c in depts_c]
            new_cursor.close()
            return info
        except cx_Oracle.DatabaseError as e:
            print(e)

    def getAllInfoDept(self, uid):
        try:
            return_type = cx_Oracle.DB_TYPE_NUMBER
            new_cursor = self.db.cursor()
            nprof = self.cursor.callfunc("functions_pck.doCountProfInDept", return_type, (uid, new_cursor))
            nstud = self.cursor.callfunc("functions_pck.doCountStudentsInDept", return_type, (uid,))
            dept_c = new_cursor.fetchall()
            info = [list(c) for c in dept_c]
            info[0].extend([int(nstud), int(nprof)])
            new_cursor.close()
            return info
        except cx_Oracle.DatabaseError as e:
            print(e)

    def removeDept(self, uid):
        try:
            self.cursor.callproc("procedures_pck.removeDepartment", (uid,))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def addDept(self, uid, name):
        try:
            self.cursor.callproc("procedures_pck.addDepartment", (uid, name))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def checkDept(self, uid, name):
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            return self.cursor.callfunc("functions_pck.checkDept", return_type, (uid, name))
        except cx_Oracle.DatabaseError as e:
            print(e)

    def showProfessors(self):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showProfessors", (new_cursor, ))
            profs_c = new_cursor.fetchall()
            new_cursor.close()
            profs = [list(p) for p in profs_c]
            new_cursor.close()
            return profs
        except cx_Oracle.DatabaseError as e:
            print(e)

    def removeProf(self, uid):
        try:
            self.cursor.callproc("procedures_pck.removeProfessor", (uid, ))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def addProfessor(self, cnp, fn, ln, bd, phone, email, password, gen, dept):
        try:
            self.cursor.callproc("procedures_pck.addProfessor", (0, cnp, fn, ln, bd, phone, email, password, gen, dept))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def removeCourseProf(self, prof_id, course_id):
        try:
            self.cursor.callproc("procedures_pck.removeGivenCourse", (int(course_id), int(prof_id)))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def addCourseProf(self, prof_id, course_id):
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.addGivenCourse", return_type, (course_id, prof_id))
            self.db.commit()
            return result
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False

    def showProfCourses(self, prof_id):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showProfCourses", (prof_id, new_cursor))
            course_c = new_cursor.fetchall()
            new_cursor.close()
            courses_ids = [list(p) for p in course_c]
            return courses_ids
        except cx_Oracle.DatabaseError as e:
            print(e)

    def showCourses(self):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showCourses", (new_cursor, ))
            courses_c = new_cursor.fetchall()
            courses = [list(c) for c in courses_c]
            new_cursor.close()
            return courses
        except cx_Oracle.DatabaseError as e:
            print(e)

    def showOneCourse(self, course_id):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.getCourseData", (course_id, new_cursor))
            course_c = new_cursor.fetchall()
            new_cursor.close()
            courses = [list(p) for p in course_c]
            return courses
        except cx_Oracle.DatabaseError as e:
            print(e)

    def addCourse(self, cn, cp, u):
        try:
            self.cursor.callproc("procedures_pck.addCourse", (1, cn, cp, u))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def removeCourse(self, course_id):
        try:
            self.cursor.callproc("procedures_pck.removeCourse", (course_id,))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            return False

    def showStudents(self, mode):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showStudents", (mode, new_cursor))
            stud_c = new_cursor.fetchall()
            students = [list(s) for s in stud_c]
            new_cursor.close()
            return students
        except cx_Oracle.DatabaseError as e:
            print(e)

    def showStudyYears(self):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.studyYears", (new_cursor, ))
            study_c = new_cursor.fetchall()
            years = list(s for s in study_c)
            new_cursor.close()
            return years
        except cx_Oracle.DatabaseError as e:
            print(e)

    def showStudGender(self):
        try:
            return_type = cx_Oracle.DB_TYPE_NUMBER
            new_cursor = self.db.cursor()
            fem = self.cursor.callfunc("functions_pck.studGender", return_type, (new_cursor, ))
            gender_c = new_cursor.fetchall()
            gender = [list(s) for s in gender_c]

            men = self.cursor.callfunc("functions_pck.countMen", return_type, ('stud', ))
            gender[0].append(int(men))
            gender[1].append(int(fem))

            new_cursor.close()
            return gender
        except cx_Oracle.DatabaseError as e:
            print(e)

    def showStudCourses(self, stud_id):
        try:
            new_cursor = self.db.cursor()
            self.cursor.callproc("procedures_pck.showStudCourses", (stud_id, new_cursor))
            courses_c = new_cursor.fetchall()
            courses = [list(c) for c in courses_c]
            new_cursor.close()
            return courses
        except cx_Oracle.DatabaseError as e:
            print(e)

    def addCourseStud(self, stud_id, course_id):
        try:
            return_type = cx_Oracle.DB_TYPE_BOOLEAN
            result = self.cursor.callfunc("functions_pck.addCourseStud", return_type, (stud_id, course_id))
            self.db.commit()
            return result
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False

    def updateCourseStud(self, stud_id, course_id, grade):
        try:
            self.cursor.callproc("procedures_pck.updateCourseStud", (stud_id, course_id, grade))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False

    def removeCourseStudent(self, stud_id, course_id):
        try:
            self.cursor.callproc("procedures_pck.removeStudRecord", (stud_id, course_id))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False

    def addStudent(self, cnp, f, l, bd, phone, email, passwd, add, gender, enr, year, dept):
        try:
            self.cursor.callproc("procedures_pck.addStudent",
                                 (0, cnp, f, l, bd, phone, email, passwd, add, gender,
                                  enr, int(year), int(dept)))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False

    def removeStudent(self, stud_id):
        try:
            self.cursor.callproc("procedures_pck.removeStudent", (stud_id,))
            self.db.commit()
            return True
        except cx_Oracle.DatabaseError as e:
            print(e)
            return False
