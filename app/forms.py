from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import InputRequired, Length
from database import *


class DBC:
    def __init__(self):
        self.db = OracleConnection('localhost', 1521, 'xe', 'system', 'Unudoitrei.123')

    def __enter__(self):
        self.db.openConnection()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.closeConnection()


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class DepartmentForm(FlaskForm):
    dept_name = StringField(validators=[InputRequired(), Length(min=4, max=100)],
                            render_kw={"placeholder": "Department Name"})
    submit = SubmitField("Add")


class UpdateCourseStud(FlaskForm):
    final = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Final Grade"})
    submit = SubmitField("Update")


class AddProfessor(FlaskForm):
    cnp = StringField(validators=[InputRequired(), Length(min=13, max=13)],
                      render_kw={"placeholder": "Professor CNP"})
    f_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Professor First Name"})
    l_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Professor Last Name"})
    bdate = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                        render_kw={"placeholder": "Birthdate dd-mm-yyyy"})
    phone = StringField(validators=[InputRequired(), Length(min=12, max=50)],
                        render_kw={"placeholder": "Phone"})
    email = StringField(validators=[InputRequired(), Length(min=12, max=50)],
                        render_kw={"placeholder": "Email"})
    gender = RadioField('Gender', choices=[('M', 'male'), ('F', 'female')])
    dept = StringField(validators=[InputRequired(), Length(min=1, max=5)],
                       render_kw={"placeholder": "Department"})
    submit = SubmitField("Add professor")


class AddStudent(FlaskForm):
    cnp = StringField(validators=[InputRequired(), Length(min=13, max=13)],
                      render_kw={"placeholder": "Student CNP"})
    f_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Student First Name"})
    l_name = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                         render_kw={"placeholder": "Student Last Name"})
    bdate = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                        render_kw={"placeholder": "Birthdate dd-mm-yyyy"})
    phone = StringField(validators=[InputRequired(), Length(min=12, max=50)],
                        render_kw={"placeholder": "Phone"})
    address = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                          render_kw={"placeholder": "Address"})
    email = StringField(validators=[InputRequired(), Length(min=12, max=50)],
                        render_kw={"placeholder": "Email"})
    gender = RadioField('Gender', choices=[('M', 'male'), ('F', 'female')])
    enrolment = StringField(validators=[InputRequired(), Length(min=10, max=50)],
                            render_kw={"placeholder": "Enrolment Date"})
    year = StringField(validators=[InputRequired(), Length(min=1, max=50)],
                       render_kw={"placeholder": "Study Year"})
    dept = StringField(validators=[InputRequired(), Length(min=1, max=5)],
                       render_kw={"placeholder": "Department"})
    submit = SubmitField("Add student")


class AddCourse(FlaskForm):
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Course Name"})
    pts = StringField(validators=[InputRequired()], render_kw={"placeholder": "Credit Points"})
    units = StringField(validators=[InputRequired()], render_kw={"placeholder": "Units"})
    submit = SubmitField("Add course")