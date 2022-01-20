from flask import Flask, render_template, url_for, redirect, session, flash,request
from flask_wtf import FlaskForm
from flask_login import LoginManager
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets
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
    dept_id = StringField(validators=[InputRequired(),Length(min=4, max=10)], render_kw={"placeholder": "Department ID"})
    dept_name = StringField(validators=[InputRequired(),Length(min=4, max=100)], render_kw={"placeholder": "Department Name"})
    submit = SubmitField("Add")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AddExistingCourse(FlaskForm):
    course = MultiCheckboxField('Select Cards for Deck', coerce=str)
    submit = SubmitField("Add")


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


@app.route('/dashboard_admin/single_student/<int:stud_id>')
def single_student(stud_id):
    student = db.getAllInfoStudent(stud_id)
    return render_template('dashboard_admin/single_student.html', student=student)


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


@app.route('/dashboard_admin/delete_professor/<int:prof_id>', methods=['GET','POST'])
def delete_professor(prof_id):
    print("DELETING PROFESSOR")
    db.removeProf(prof_id)
    return redirect(url_for('manage_professors'))


@app.route('/dashboard_admin/single_professor/<int:prof_id>')
def single_professor(prof_id):
    print("Single prof id ", prof_id)
    courses = db.showCourses()
    my_courses = db.showProfCourses(prof_id)
    print("Single prof_id courses ",my_courses)
    prof = db.getAllInfoProf(prof_id)
    return render_template('dashboard_admin/single_professor.html', prof=prof, courses=courses, my_courses=my_courses)


@app.route('/dashboard_admin/delete_course_prof/<int:prof_id>/<int:course_id>', methods=['GET','POST'])
def delete_course_prof(prof_id, course_id):
    print("DELETING COURSE from prof id", prof_id, " this course ",course_id)
    db.removeCourseProf(prof_id, course_id)
    return redirect(url_for('single_professor', prof_id=prof_id))


@app.route('/dashboard_admin/add_course_prof/<int:prof_id>/<int:course_id>', methods=['GET','POST'])
def add_course_prof(prof_id, course_id):
    print("ADDING COURSE to prof_id", prof_id, course_id)
    db.addCourseProf(prof_id, course_id)
    return redirect(url_for('single_professor', prof_id=prof_id))

@app.route('/dashboard_admin/course_details/<int:course_id>', methods=['GET','POST'])
def course_details(course_id):
    # print("ADDING COURSE to prof_id", prof_id, course_id)
    db.showOneCourse(course_id)
    return render_template('dashboard_admin/course_details.html')





if __name__ == '__main__':
    app.run(debug=True)


# db.closeConnection()


