from typing import Optional
from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(user_id):
    # Tried querying Student and Faculty 
    #user = Student.query.get(int(user_id)) or Faculty.query.get(int(user_id))
    user = Student.query.filter_by(username=user_id).first() or Faculty.query.filter_by(username=user_id).first()
    return user

# Stores common fields
class User(db.Model, UserMixin):
    __abstract__ = True  # Specifies that this is an abstract base class

    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique=True, nullable=False)
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True, nullable=False)
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    first_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), nullable=False)
    last_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), nullable=False)
    phone_number: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), nullable=False)
    wpi_id: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), nullable=False)

    def __repr__(self):
        # Excluded password_hash for security
        return f"<User(id={self.id}, username='{self.username}')>"

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
    
    # change id to username since user_id overlaps between Student and Faculty tables
    def get_id(self):
        return self.username
   

    # #FJDOISHGOISDHOG
    # GET BACK TO THIS
    # LOOK UP

# Student Model
class Student(User):

    major: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), default="none", nullable=False)
    cum_gpa: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, default=0, nullable=False)
    grad_year: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0, nullable=False)

    #relationship
    experiences : sqlo.Mapped[list['CourseExperience']] = sqlo.relationship('CourseExperience', back_populates= 'user')
    studentSAApplications: sqlo.Mapped[list['SAApplication']] = sqlo.relationship('SAApplication', back_populates='student')

    def __repr__(self):
        return f"<Student(id={self.id}, major='{self.major}', email='{self.email}')>"
    def take_course(self, course, g, tt):
        from app.course.course_models import CourseExperience           
        newCourseExp = CourseExperience( course_id = course.id, user_id=self.id, has_taken=True, been_sa=False, grade=g, term_taken=tt )
        db.session.add(newCourseExp)
        db.session.commit()
    def get_SAApplications(self):
        return self.studentSAApplications


# Faculty Model
class Faculty(User):
    department: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), default="none", nullable=False)

    # user: sqlo.Mapped['User'] = sqlo.relationship('User', back_populates='faculty_profile')
    course_sections : sqlo.Mapped[list['CourseSection']] = sqlo.relationship('CourseSection', back_populates='instructor')


    def __repr__(self):
        return f"<Faculty(id={self.id}, department='{self.department}')>"
    def get_course_sections(self):
        return self.course_sections
    def take_course(self, course, g, tt):
        from app.course.course_models import CourseExperience   

        newCourseExp = CourseExperience( course_id = course.id, user_id=self.id, has_taken=True, been_sa=False, grade=g, term_taken=tt )
        db.session.add(newCourseExp)
        db.session.commit()
