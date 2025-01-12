from app import db
from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, TextAreaField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, EqualTo, Email, Optional, Length
from app.user.user_models import User, Student, Faculty
from app.course.course_models import Course, CourseSection
from app.static import form_options
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy import cast, Integer
 


class CreateCourseForm(FlaskForm):
    section_number = IntegerField('Section (Optional: Section number will be auto-assigned if left empty)', 
                                 validators=[Optional(), NumberRange(min=0, max=999)])
    term = SelectField("Term", choices=form_options.future_class_terms)
    submit = SubmitField('Create')

    course_choices = QuerySelectField(
        "Courses",
        query_factory=lambda: db.session.query(Course).order_by(Course.major, Course.coursenum).all(),
        get_label=lambda course: f"{course.major} {course.coursenum}",
    )

    def validate_section_number(self, section_number):
        course_offering = CourseSection.query.filter_by(section_number = section_number.data, term = self.term.data, course = self.course_choices.data).first()
        if not course_offering is None:
            raise ValidationError('Course with the same section number already exists in this term.')
        
class EditCourseExperience(FlaskForm):
    has_taken = BooleanField("")
    taken_term = SelectField("Term Taken", choices=form_options.past_class_terms)
    grade = SelectField("Grade", choices=form_options.grades)