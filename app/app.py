from flask import Flask, render_template, url_for, redirect, session, flash
from flask_wtf import FlaskForm
from flask_login import LoginManager
from wtforms import StringField, PasswordField, SubmitField
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
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")



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
    #il salvez in baza de date petru statistici, useri activi
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
    return render_template('dashboard_professor.html', courses=courses)\

@app.route('/dashboard_admin')
def dashboard_admin():
    courses = db.showCourses()
    return render_template('dashboard_admin.html', courses=courses)


@app.route('/personal_data', methods=["GET", "POST"])
def personal_data():
    professor_data = db.getProfessorData(session['id'])
    print(professor_data)
    return render_template('/personal_data.html', professor_data=professor_data)
# db.closeConnection()

if __name__ == '__main__':
    app.run(debug=True)