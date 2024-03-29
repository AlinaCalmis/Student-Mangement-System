from flask import Flask, render_template, url_for, redirect, session, flash, request
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "Unudoitrei.123"


def logout_user(uid):
    with DBC() as db:
        db.logoutUser(uid)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with DBC() as db:
            uid = form.username.data
            user_id = db.isUserRegistered(uid=uid)
            if user_id:
                passwd = db.checkPasswd(uid=uid, passwd=form.password.data)
                if passwd:
                    usr_type = db.userType(uid)
                    loaded, user = db.loadUser(uid, usr_type)
                    if not loaded:
                        flash('The user is already logged in!', 'danger')
                        return render_template('login.html', form=form, title='Login', session=session)
                    if usr_type == "admin":
                        session["username"] = "Admin"
                    else:
                        session["username"] = user[0][2]
                    session["uid"] = uid
                    session['active'] = True
                    session['type'] = usr_type
                    return redirect(url_for('home'))
                else:
                    flash(f'Login unsuccessful. If you don\'t have your credentials, please contact secretary!',
                          'danger')
            else:
                flash(f'Login unsuccessful. If you don\'t have your credentials, please contact secretary!', 'danger')
    return render_template('login.html', form=form, title='Login', session=session)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user(session['uid'])
    session.clear()
    return redirect(url_for('home'))


@app.route('/dashboard_admin', methods=["GET", "POST"])
def dashboard_admin():
    if session['uid'] == '0':
        with DBC() as db:
            courses = db.showCourses()
        return render_template('dashboard_admin.html', courses=courses)
    else:
        flash('You are not an administrator!', 'danger')
        return redirect(url_for('personal_data'))


@app.route('/personal_data', methods=["GET", "POST"])
def personal_data():
    with DBC() as db:
        if session['type'] == 'student':
            user_data = db.getAllInfoStudent(session['uid'])
            courses = db.showStudCourses(session['uid'])
        else:
            user_data = db.getAllInfoProf(session['uid'])
            courses = db.showProfCourses(session['uid'])
    return render_template('personal_data.html', user_data=user_data, type=session['type'], courses=courses)


# -------- Department managemnet -----------
@app.route('/dashboard_admin/manage_departments', methods=["GET", "POST"])
def manage_departments():
    with DBC() as db:
        depts = db.showDepartments()
    return render_template('dashboard_admin/manage_departments.html', depts=depts)


@app.route('/dashboard_admin/single_department/<int:dept_id>')
def single_dept(dept_id):
    with DBC() as db:
        dept = db.getAllInfoDept(dept_id)
    return render_template('dashboard_admin/single_department.html', dept=dept)


@app.route('/dashboard_admin/delete_department/<int:dept_id>', methods=["GET", "POST"])
def delete_dept(dept_id):
    with DBC() as db:
        if db.removeDept(dept_id):
            flash('Department deleted successfully', 'success')
        else:
            flash('Something went wrong. Department has students and/or professors. '
                  'You cannot delete this', 'danger')
    return redirect(url_for('manage_departments'))


@app.route('/dashboard_admin/add_department', methods=["GET", "POST"])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        with DBC() as db:
            checked = db.checkDept(form.dept_name.data)
            if not checked:
                db.addDept(form.dept_name.data)
                flash('Department added to database successfully', 'success')
                return redirect(url_for('manage_departments'))
        flash('Something went wrong. Check id or name and try again', 'danger')
    return render_template('/dashboard_admin/add_department.html', form=form)


# ---------- Manage professors ---------------

@app.route('/dashboard_admin/manage_professors', methods=["GET", "POST"])
def manage_professors():
    with DBC() as db:
        profs = db.showProfessors()
        depts = db.showDepartments()
    return render_template('dashboard_admin/manage_professors.html', depts=depts, profs=profs)


@app.route('/dashboard_admin/delete_professor/<int:prof_id>', methods=['GET', 'POST'])
def delete_professor(prof_id):
    with DBC() as db:
        db.removeProf(prof_id)
    flash('Professor deleted successfully', 'success')
    return redirect(url_for('manage_professors'))


@app.route('/dashboard_admin/single_professor/<int:prof_id>')
def single_professor(prof_id):
    with DBC() as db:
        courses = db.showCourses()
        my_courses = db.showProfCourses(prof_id)
        prof = db.getAllInfoProf(prof_id)
    return render_template('dashboard_admin/single_professor.html', prof=prof, courses=courses,
                           my_courses=my_courses, session=session)


@app.route('/dashboard_admin/delete_course_prof/<int:prof_id>/<int:course_id>', methods=['GET', 'POST'])
def delete_course_prof(prof_id, course_id):
    with DBC() as db:
        db.removeCourseProf(prof_id, course_id)
        flash('Course deleted successfully from professor\'s teachig list', 'success')
    return redirect(url_for('single_professor', prof_id=prof_id))


@app.route('/dashboard_admin/add_professor', methods=['GET', 'POST'])
def add_professor():
    form = AddProfessor()
    if request.method == 'POST':
        if form.validate():
            with DBC() as db:
                add = db.addProfessor(form.cnp.data,
                                      form.f_name.data,
                                      form.l_name.data,
                                      form.bdate.data,
                                      form.phone.data,
                                      form.email.data,
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
    with DBC() as db:
        add = db.addCourseProf(prof_id, course_id)
    if add:
        flash('Course successfully added', 'success')
    else:
        flash('Course already exists', 'danger')
    return redirect(url_for('single_professor', prof_id=prof_id))


@app.route('/dashboard_admin/course_details/<int:course_id>', methods=['GET', 'POST'])
def course_details(course_id):
    with DBC() as db:
        courses = db.showOneCourse(course_id)
    return render_template('dashboard_admin/course_details.html', courses=courses)


# --------------- Manage Courses -------------------
@app.route('/dashboard_admin/manage_courses', methods=["GET", "POST"])
def manage_courses():
    with DBC() as db:
        courses = db.showCourses()
    return render_template('dashboard_admin/manage_courses.html', courses=courses)


@app.route('/dashboard_admin/add_course', methods=["GET", "POST"])
def add_course():
    form = AddCourse()
    if request.method == 'POST':
        if form.validate():
            with DBC() as db:
                add = db.addCourse(form.name.data, form.pts.data, form.units.data)
            if add:
                flash("New course added successfully", 'success')
                return redirect(url_for('manage_courses'))
    return render_template('/dashboard_admin/add_course.html', form=form)


@app.route('/dashboard_admin/delete_course/<int:course_id>', methods=["GET", "POST"])
def delete_course(course_id):
    with DBC() as db:
        db.removeCourse(course_id)
    flash('Course deleted successfully', 'success')
    return redirect(url_for('manage_courses'))


# --------------- Manage Students -------------------
@app.route('/dashboard_admin/manage_students', methods=["GET", "POST"])
def manage_students():
    with DBC() as db:
        students = db.showStudents('all')
    return render_template('dashboard_admin/manage_students.html', students=students)


@app.route('/dashboard_admin/manage_students/by_departments', methods=["GET", "POST"])
def by_departments():
    with DBC() as db:
        students = db.showStudents('dept')
        depts = db.showDepartments()
    return render_template('dashboard_admin/manage_students/by_departments.html', students=students, depts=depts)


@app.route('/dashboard_admin/manage_students/by_study_year', methods=["GET", "POST"])
def by_study_year():
    with DBC() as db:
        students = db.showStudents('year')
        years = db.showStudyYears()
    return render_template('dashboard_admin/manage_students/by_study_year.html', students=students, years=years)


@app.route('/dashboard_admin/manage_students/by_gender', methods=["GET", "POST"])
def by_gender():
    with DBC() as db:
        students = db.showStudents('gender')
        gens = db.showStudGender()
    return render_template('dashboard_admin/manage_students/by_gender.html',
                           students=students, genders=gens)


@app.route('/dashboard_admin/manage_students/single_student/<int:stud_id>', methods=["GET", "POST"])
def single_student(stud_id):
    with DBC() as db:
        student = db.getAllInfoStudent(stud_id)
        courses = db.showStudCourses(stud_id)
        all_courses = db.showCourses()
    return render_template('dashboard_admin/manage_students/single_student.html',
                           student=student, s_courses=courses, courses=all_courses)


@app.route('/dashboard_admin/manage_students/add_student_course/<int:stud_id>/<int:course_id>')
def add_student_course(stud_id, course_id):
    with DBC() as db:
        added = db.addCourseStud(stud_id, course_id)
    if added:
        flash('Course added successfully.', 'success')
    else:
        flash('Course already exists.', 'danger')
    return redirect(url_for('single_student', stud_id=stud_id))


@app.route('/dashboard_admin/manage_students/update_student_course/<int:stud_id>/<int:course_id>',
           methods=["GET", "POST"])
def update_student_course(stud_id, course_id):
    form = UpdateCourseStud()
    if request.method == 'POST':
        if form.validate():
            with DBC() as db:
                db.updateCourseStud(stud_id, course_id, form.final.data)
                flash("Course Updated Successfully", "success")
            return redirect(url_for('single_student', stud_id=stud_id))
    return render_template('/dashboard_admin/manage_students/update_student_course.html', form=form)


@app.route('/dashboard_admin/manage_students/delete_student_course/<int:stud_id>/<int:course_id>',
           methods=["GET", "POST"])
def delete_student_course(stud_id, course_id):
    with DBC() as db:
        db.removeCourseStudent(stud_id, course_id)
        flash("Course deleted successfully", "success")
    return redirect(url_for('single_student', stud_id=stud_id))


@app.route('/dashboard_admin/manage_students/add_student', methods=["GET", "POST"])
def add_student():
    form = AddStudent()
    if request.method == 'POST':
        if form.validate():
            with DBC() as db:
                add = db.addStudent(form.cnp.data,
                                    form.f_name.data,
                                    form.l_name.data,
                                    form.bdate.data,
                                    form.phone.data,
                                    form.email.data,
                                    form.address.data,
                                    form.gender.data,
                                    form.enrolment.data,
                                    form.year.data,
                                    form.dept.data)
            if add:
                flash('Student added successfully.', 'success')
                return redirect(url_for('manage_students'))
            flash('An error occurred. Check data.', 'danger')
    return render_template('/dashboard_admin/manage_students/add_student.html', form=form)


@app.route('/dashboard_admin/manage_students/delete_student/<int:stud_id>/<string:criterion>', methods=["GET", "POST"])
def delete_student(stud_id, criterion):
    with DBC() as db:
        db.removeStudent(stud_id)
    if 'all' in criterion:
        flash('Student deleted successfully', 'success')
        return redirect(url_for('manage_students'))
    else:
        flash('Student deleted successfully', 'success')
        return redirect(url_for(criterion))


if __name__ == '__main__':
    print("Running app")
    app.run(debug=True)
