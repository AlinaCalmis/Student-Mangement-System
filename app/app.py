from flask import Flask, render_template, url_for, redirect, session, flash, request
from flask_wtf import FlaskForm
from flask_login import LoginManager
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import InputRequired, Length
from database import *

app = Flask(__name__)
# datab = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://system:Unudoitrei.123@127.0.0.1:1521/xe'
app.config['SECRET_KEY'] = "Unudoitrei.123"
db = OracleConnection('localhost', 1521, 'xe', 'system', 'Unudoitrei.123')
db.openConnection()


# # db.getProfessorData(8)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class DepartmentForm(FlaskForm):
    dept_id = StringField(validators=[InputRequired(), Length(min=4, max=10)],
                          render_kw={"placeholder": "Department ID"})
    dept_name = StringField(validators=[InputRequired(), Length(min=4, max=100)],
                            render_kw={"placeholder": "Department Name"})
    submit = SubmitField("Add")


class UpdateCourseStud(FlaskForm):
    final = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Final Grade"})
    submit = SubmitField("Update")


class AddProfessor(FlaskForm):
    cnp = StringField(validators=[InputRequired(), Length(min=13, max=13)], render_kw={"placeholder": "Professor CNP"})
    f_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Professor First Name"})
    l_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Professor Last Name"})
    bdate = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                        render_kw={"placeholder": "Birthdate dd-mm-yyyy"})
    phone = StringField(validators=[InputRequired(), Length(min=12, max=50)], render_kw={"placeholder": "Phone"})
    email = StringField(validators=[InputRequired(), Length(min=12, max=50)], render_kw={"placeholder": "Email"})
    passwd = PasswordField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Password"})
    gender = RadioField('Gender', choices=[('M', 'male'), ('F', 'female')])
    dept = StringField(validators=[InputRequired(), Length(min=4, max=5)], render_kw={"placeholder": "Department"})
    submit = SubmitField("Add professor")


class AddStudent(FlaskForm):
    cnp = StringField(validators=[InputRequired(), Length(min=13, max=13)], render_kw={"placeholder": "Student CNP"})
    f_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Student First Name"})
    l_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Student Last Name"})
    bdate = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                        render_kw={"placeholder": "Birthdate dd-mm-yyyy"})
    phone = StringField(validators=[InputRequired(), Length(min=12, max=50)], render_kw={"placeholder": "Phone"})
    address = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Address"})
    email = StringField(validators=[InputRequired(), Length(min=12, max=50)], render_kw={"placeholder": "Email"})
    passwd = PasswordField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Password"})
    gender = RadioField('Gender', choices=[('M', 'male'), ('F', 'female')])
    enrolment = StringField(validators=[InputRequired(), Length(min=10, max=50)],
                            render_kw={"placeholder": "Enrolment Date"})
    year = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Study Year"})
    dept = StringField(validators=[InputRequired(), Length(min=4, max=5)], render_kw={"placeholder": "Department"})
    submit = SubmitField("Add student")


class AddCourse(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Course Name"})
    pts = StringField(validators=[InputRequired()], render_kw={"placeholder": "Credit Points"})
    units = StringField(validators=[InputRequired()], render_kw={"placeholder": "Units"})
    submit = SubmitField("Add course")


def load_user(uid):
    # db.openConnection()

    usr_type = db.userType(uid)
    print(usr_type)
    # user = None

    if usr_type == 'student':
        user = db.getStudentData(uid)
    elif usr_type == 'professor':
        user = db.getProfessorData(uid)
    elif usr_type == 'admin':
        user = None
    print(user)
    # il salvez in baza de date petru statistici, useri activi
    db.loadUser(uid)
    # db.closeConnection()
    return user


def logout_user(uid):
    db.logoutUser(uid)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # db = OracleConnection('localhost', 1521, 'xe', 'system', 'Unudoitrei.123')
        # db.openConnection()
        uid = form.username.data
        user_id = db.isUserRegistered(uid=uid)
        if user_id:
            passwd = db.checkPasswd(uid=uid, passwd=form.password.data)
            print("IS user registered? ", passwd)
            if passwd:
                user = load_user(uid=uid)
                usr_type = db.userType(uid)
                if usr_type == "admin":
                    session["username"] = "Admin"
                else:
                    session["username"] = user["Name"]
                session["uid"] = uid
                session['active'] = True
                session['type'] = usr_type
                print(usr_type)
                return redirect(url_for(f'dashboard_{usr_type}'))
            else:
                flash(f'Login unsuccessful. If you don\'t have your credentials, please contact secretary!', 'danger')
        else:
            flash(f'Login unsuccessful. If you don\'t have your credentials, please contact secretary!', 'danger')
    return render_template('login.html', form=form, title='Login', session=session)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    print("LOG OUT ", session['uid'])
    logout_user(session['uid'])
    session.pop('uid')
    session.pop('username')
    session.pop('active')
    session.pop('type')
    return render_template('home.html')


@app.route('/dashboard_professor')
def dashboard_professor():
    courses = db.showCourses()
    return render_template('dashboard_professor.html', courses=courses)


@app.route('/dashboard_admin', methods=["GET", "POST"])
def dashboard_admin():
    courses = db.showCourses()
    return render_template('dashboard_admin.html', courses=courses)


@app.route('/personal_data', methods=["GET", "POST"])
def personal_data():
    professor_data = db.getProfessorData(session['id'])
    print(professor_data)
    return render_template('personal_data.html', professor_data=professor_data)


# -------- Department managemnet -----------
@app.route('/dashboard_admin/manage_departments', methods=["GET", "POST"])
def manage_departments():
    depts = db.showDepartments()
    return render_template('dashboard_admin/manage_departments.html', depts=depts)


@app.route('/dashboard_admin/single_department/<int:dept_id>')
def single_dept(dept_id):
    dept = db.getAllInfoDept(dept_id)
    return render_template('dashboard_admin/single_department.html', dept=dept)


@app.route('/dashboard_admin/delete_department/<int:dept_id>', methods=["GET", "POST"])
def delete_dept(dept_id):
    db.removeDept(dept_id)
    return redirect(url_for('manage_departments'))


@app.route('/dashboard_admin/add_department', methods=["GET", "POST"])
def add_department():
    form = DepartmentForm()
    # if request.method == 'POST':
    #     id = request.form['dept_id']
    #     name = request.form['dept_name']
    if form.validate_on_submit():
        checked = db.checkDept(form.dept_id.data, form.dept_name.data)
        if not checked:
            db.addDept(form.dept_id.data, form.dept_name.data)
            flash('Department added to database successfully', 'success')
            return redirect(url_for('manage_departments'))
        flash('Something went wrong. Check id or name and try again', 'danger')
    return render_template('/dashboard_admin/add_department.html', form=form)


# ---------- Manage professors ---------------

@app.route('/dashboard_admin/manage_professors', methods=["GET", "POST"])
def manage_professors():
    profs = db.showProfessors()
    depts = db.showDepartments()
    print(profs)
    return render_template('dashboard_admin/manage_professors.html', depts=depts, profs=profs)


@app.route('/dashboard_admin/delete_professor/<int:prof_id>', methods=['GET', 'POST'])
def delete_professor(prof_id):
    print("DELETING PROFESSOR")
    db.removeProf(prof_id)
    return redirect(url_for('manage_professors'))


@app.route('/dashboard_admin/single_professor/<int:prof_id>')
def single_professor(prof_id):
    print("Single prof id ", prof_id)
    courses = db.showCourses()
    my_courses = db.showProfCourses(prof_id)
    print("Single prof_id courses ", my_courses)
    prof = db.getAllInfoProf(prof_id)
    return render_template('dashboard_admin/single_professor.html', prof=prof, courses=courses, my_courses=my_courses)


@app.route('/dashboard_admin/delete_course_prof/<int:prof_id>/<int:course_id>', methods=['GET', 'POST'])
def delete_course_prof(prof_id, course_id):
    print("DELETING COURSE from prof id", prof_id, " this course ", course_id)
    db.removeCourseProf(prof_id, course_id)
    return redirect(url_for('single_professor', prof_id=prof_id))


@app.route('/dashboard_admin/add_professor', methods=['GET', 'POST'])
def add_professor():
    form = AddProfessor()
    if request.method == 'POST':
        if form.validate():
            add = db.addProfessor(form.cnp.data,
                                  form.f_name.data,
                                  form.l_name.data,
                                  form.bdate.data,
                                  form.phone.data,
                                  form.email.data,
                                  form.passwd.data,
                                  form.gender.data,
                                  form.dept.data)

            if add:
                flash("Professor added", 'success')
                return redirect(url_for('manage_professors'))
            flash("This professor already exists", 'danger')
        else:
            flash("Incorrect data", 'danger')
    return render_template('/dashboard_admin/add_professor.html', form=form)


@app.route('/dashboard_admin/add_course_prof/<int:prof_id>/<int:course_id>', methods=['GET', 'POST'])
def add_course_prof(prof_id, course_id):
    print("ADDING COURSE to prof_id", prof_id, course_id)
    db.addCourseProf(prof_id, course_id)
    return redirect(url_for('single_professor', prof_id=prof_id))


@app.route('/dashboard_admin/course_details/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    # print("ADDING COURSE to prof_id", prof_id, course_id)
    courses = db.showOneCourse(course_id)
    return render_template('dashboard_admin/course_details.html', courses=courses)


# --------------- Manage Courses -------------------
@app.route('/dashboard_admin/manage_courses', methods=["GET", "POST"])
def manage_courses():
    courses = db.showCourses()
    print(courses)
    return render_template('dashboard_admin/manage_courses.html', courses=courses)


@app.route('/dashboard_admin/add_course', methods=["GET", "POST"])
def add_course():
    form = AddCourse()
    if request.method == 'POST':
        if form.validate():
            add = db.addCourse(form.name.data, form.pts.data, form.units.data)
            if add:
                flash("New course added successfully", 'succes')
                return redirect(url_for('manage_courses'))
    return render_template('/dashboard_admin/add_course.html', form=form)


@app.route('/dashboard_admin/delete_course/<int:course_id>', methods=["GET", "POST"])
def delete_course(course_id):
    db.removeCourse(course_id)
    return redirect(url_for('manage_courses'))


# --------------- Manage Students -------------------
@app.route('/dashboard_admin/manage_students', methods=["GET", "POST"])
def manage_students():
    students = db.showStudents('all')
    print(students)
    return render_template('dashboard_admin/manage_students.html', students=students)


@app.route('/dashboard_admin/manage_students/by_departments', methods=["GET", "POST"])
def by_departments():
    students = db.showStudents('dept')
    depts = db.showDepartments()
    print(students)
    return render_template('dashboard_admin/manage_students/by_departments.html', students=students, depts=depts)


@app.route('/dashboard_admin/manage_students/by_study_year', methods=["GET", "POST"])
def by_study_year():
    students = db.showStudents('year')
    years = db.showStudyYears()
    print(students)
    return render_template('dashboard_admin/manage_students/by_study_year.html', students=students, years=years)


@app.route('/dashboard_admin/manage_students/by_gender', methods=["GET", "POST"])
def by_gender():
    students = db.showStudents('gender')
    gens = db.showStudGender()
    return render_template('dashboard_admin/manage_students/by_gender.html',
                           students=students, genders=gens)


@app.route('/dashboard_admin/manage_students/single_student/<int:stud_id>', methods=["GET", "POST"])
def single_student(stud_id):
    student = db.getAllInfoStudent(stud_id)
    courses = db.showStudCourses(stud_id)
    all_courses = db.showCourses()
    return render_template('dashboard_admin/manage_students/single_student.html',
                           student=student, s_courses=courses, courses=all_courses)


@app.route('/dashboard_admin/manage_students/add_student_course/<int:stud_id>/<int:course_id>')
def add_student_course(stud_id, course_id):
    print(stud_id, course_id)
    added = db.addCourseStud(stud_id, course_id)
    if added:
        flash('Course added successfully.', 'success')
    else:
        flash('Course already exists.', 'danger')
    print("Course ", course_id, " added to ", stud_id)
    return redirect(url_for('single_student', stud_id=stud_id))


@app.route('/dashboard_admin/manage_students/update_student_course/<int:stud_id>/<int:course_id>',
           methods=["GET", "POST"])
def update_student_course(stud_id, course_id):
    form = UpdateCourseStud()
    if request.method == 'POST':
        if form.validate():
            db.updateCourseStud(stud_id, course_id, form.final.data)
            flash("Course Updated Successfully", "success")
            return redirect(url_for('single_student', stud_id=stud_id))
    return render_template('/dashboard_admin/manage_students/update_student_course.html', form=form)


@app.route('/dashboard_admin/manage_students/delete_student_course/<int:stud_id>/<int:course_id>',
           methods=["GET", "POST"])
def delete_student_course(stud_id, course_id):
    db.removeCourseStudent(stud_id, course_id)
    return redirect(url_for('single_student', stud_id=stud_id))


@app.route('/dashboard_admin/manage_students/add_student', methods=["GET", "POST"])
def add_student():
    form = AddStudent()
    if request.method == 'POST':
        if form.validate():
            add = db.addStudent(form.cnp.data,
                                form.f_name.data,
                                form.l_name.data,
                                form.bdate.data,
                                form.phone.data,
                                form.email.data,
                                form.passwd.data,
                                form.address.data,
                                form.gender.data,
                                form.enrolment.data,
                                form.year.data,
                                form.dept.data)
            if add:
                flash('Student added successfully.', 'succes')
                return redirect(url_for('manage_students'))
            flash('An error occured. Check data.', 'danger')
    return render_template('/dashboard_admin/manage_students/add_student.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

# db.closeConnection()
