from flask_wtf import FlaskForm

from wtforms import FloatField, StringField, PasswordField, SubmitField, IntegerField, RadioField, BooleanField, TextAreaField, SelectField, ValidationError, FieldList, FormField
from wtforms.validators import DataRequired, EqualTo, Email, Optional, Length, NumberRange
from app.user.user_models import User, Student, Faculty
from app.course.course_models import Course
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.static import form_options

from app import db

def is_numeric(form, field):
    if not field.data.isdigit():
        raise ValidationError('Field can only contain numeric characters.')


class GradeForm(FlaskForm):
    gradeReceived = RadioField(
    "Grade Received",
    choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('NR', 'NR')]
)
class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    major = SelectField('Major', choices=form_options.majors)
    gpa = FloatField('GPA (Optional)', validators=[Optional(), NumberRange(min=0.0, max=4.0)])
    graduation_year = SelectField('Graduation Year', choices=form_options.grad_years)
    wpi_id = StringField('WPI ID', validators=[DataRequired(), Length(min=9, max=9), is_numeric])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10), is_numeric])
    courses_served = QuerySelectMultipleField(
        "Courses Served as SA", 
        query_factory=lambda: db.session.query(Course).order_by(Course.major, Course.coursenum).all(), 
        get_label=lambda course: f"{course.major} {course.coursenum}", 
        widget=ListWidget(prefix_label=False), 
        option_widget=CheckboxInput(),  
    )
    courses_taken = QuerySelectMultipleField(
        "Courses Taken",
        query_factory=lambda: db.session.query(Course).order_by(Course.major, Course.coursenum).all(), 
        get_label=lambda course: f"{course.major} {course.coursenum}", 
        widget=ListWidget(prefix_label=False), 
        option_widget=CheckboxInput(),  
    ) 
    # grades = FieldList(FormField(GradeForm),"Test", min_entries=10)

    submit = SubmitField('Register')

    

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')
        user = Faculty.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email address.')
        user = Faculty.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email address.')
        
    def validate_phone_number(self, phone_number):
        user = Student.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone number already exists. Please choose a different phone number.')
        user = Faculty.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone number already exists. Please choose a different phone number.')

    def validate_wpi_id(self, wpi_id):
        user = Student.query.filter_by(wpi_id=wpi_id.data).first()
        if user:
            raise ValidationError('WPI ID is already registered. Please use a different WPI ID.')
        user = Faculty.query.filter_by(wpi_id=wpi_id.data).first()
        if user:
            raise ValidationError('WPI ID is already registered. Please use a different WPI ID.')


class FacultyRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    department = SelectField('Department', choices=form_options.departments)
    wpi_id = StringField('WPI ID', validators=[DataRequired(), Length(min=9, max=9), is_numeric])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10), is_numeric])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')
        user = Faculty.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email address.')
        user = Faculty.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email address.')
        
    def validate_phone_number(self, phone_number):
        user = Student.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone number already exists. Please choose a different phone number.')
        user = Faculty.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone number already exists. Please choose a different phone number.')

    def validate_wpi_id(self, wpi_id):
        user = Student.query.filter_by(wpi_id=wpi_id.data).first()
        if user:
            raise ValidationError('WPI ID is already registered. Please use a different WPI ID.')
        user = Faculty.query.filter_by(wpi_id=wpi_id.data).first()
        if user:
            raise ValidationError('WPI ID is already registered. Please use a different WPI ID.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')

class StudentEditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10), is_numeric])
    major = SelectField('Major', choices=form_options.majors)
    cum_gpa = FloatField('Cumulative GPA', validators=[Optional(), NumberRange(min=0.0, max=4.0)])
    grad_year = SelectField('Graduation Year', choices=form_options.grad_years)
    courses_served = QuerySelectMultipleField(
        "Courses Served as SA", 
        query_factory=lambda: db.session.query(Course).order_by(Course.major, Course.coursenum).all(), 
        get_label=lambda course: f"{course.major} {course.coursenum}", 
        widget=ListWidget(prefix_label=False), 
        option_widget=CheckboxInput(),  
    )
    courses_taken = QuerySelectMultipleField(
        "Courses Taken",
        query_factory=lambda: db.session.query(Course).order_by(Course.major, Course.coursenum).all(), 
        get_label=lambda course: f"{course.major} {course.coursenum}", 
        widget=ListWidget(prefix_label=False), 
        option_widget=CheckboxInput(),  
    )
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user and not user.email == email.data:
            raise ValidationError('Email is already registered. Please use a different email address.')
        user = Faculty.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email address.')


class EditCourseExperience(FlaskForm):
    been_sa = BooleanField("SA'd Course")
    has_taken = BooleanField("Taken Course")
    term_taken = SelectField("Term Taken", choices=form_options.past_class_terms)
    grade = SelectField("Grade", choices=form_options.grades)
    submit = SubmitField('Save')

class FacultyEditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10), is_numeric])
    department = SelectField('Department', choices=form_options.departments)
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different email address.')
        user = Faculty.query.filter_by(email=email.data).first()
        if user and not user.email == email.data:
            raise ValidationError('Email is already registered. Please use a different email address.')