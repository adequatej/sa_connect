from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Optional
from app.static import form_options
from app.user.user_models import User, Student, Faculty

class CreateSAPositionForm(FlaskForm):
    course_section = SelectField('Course Section', choices=[], validators=[DataRequired()])
    number_of_sas = IntegerField('Number of SAs', validators=[DataRequired(), NumberRange(min=1, max=99)])
    min_gpa = FloatField('Minimum GPA', validators=[DataRequired(), NumberRange(min=0.0, max=4.0)])
    min_grade = SelectField('Minimum Grade Earned', choices=form_options.min_grades)
    prior_experience = BooleanField('Requires Prior SA Experience')
    
    submit = SubmitField('Create SA Position')

class ApplyForSAPosition(FlaskForm):
    # test = IntegerField()
    # grade = SelectField('Grade Earned', choices=[], validators=[DataRequired()])
    # year_term_course = SelectField('Year and term you took the course', choices=form_options.past_class_terms)
    # year_term_apply = SelectField('Year and term you are applying for SAship', choices=form_options.future_class_terms)
    submit = SubmitField('Apply For SA Position')