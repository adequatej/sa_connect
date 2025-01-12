from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from app.user.user_models import Student

# Course Section Model
class CourseSection(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    section_number: sqlo.Mapped[int] = sqlo.mapped_column(nullable=False)
    instructor_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('faculty.id'))
    course_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('course.id'))
    term: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), nullable=False)

    # Relationships
    instructor: sqlo.Mapped['Faculty'] = sqlo.relationship('Faculty', back_populates='course_sections')
    sa_positions: sqlo.Mapped[list['SAPosition']] = sqlo.relationship('SAPosition', back_populates='course_section')
    course: sqlo.Mapped['Course'] = sqlo.relationship('Course', back_populates='course_sections')

    def __repr__(self):
        return f"<CourseSection(id={self.id}, course='{self.course}', section_number='{self.section_number}')>"
    
    def get_major(self):
        return self.course.major
    
    def get_coursenum(self):
        return self.course.coursenum
    
    def get_sa_positions(self):
        return (self.sa_positions)

    def get_course(self):
        return self.course

    def assign_course(self, courseID):
        self.course_id=courseID
     



class Course(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    major: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))
    coursenum: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4))

    #relationship
    experiences : sqlo.Mapped['CourseExperience'] = sqlo.relationship(back_populates= 'course')
    course_sections : sqlo.Mapped['CourseSection'] = sqlo.relationship(back_populates= 'course')
    #changed sqlo.writeonlymapped to sqlo.mapped for course_sections
    def __repr__(self):
        return f"<Course(id={self.id}, major='{self.major}', coursenum='{self.coursenum}')>"
    def get_experiences(self):
        return CourseExperience.query.filter_by(course_id=self.id).all()
    def get_course_sections(self):
        return CourseSection.query.filter_by(course_id=self.id).all()
    
    
# Course Experience Model
class CourseExperience(db.Model):
    course_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id), primary_key=True)
    user_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id), primary_key=True)
    has_taken : sqlo.Mapped[bool] = sqlo.mapped_column(default=False)
    been_sa : sqlo.Mapped[bool] = sqlo.mapped_column(default=False)
    grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), default="?")
    term_taken : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), default="?")

    # relationships
    course : sqlo.Mapped[Course] = sqlo.relationship( back_populates= 'experiences')
    user : sqlo.Mapped[Student] = sqlo.relationship( back_populates= 'experiences')
    def __repr__(self):
        return f"<Course(id={self.course_id}, major='{self.grade}', userid='{self.user_id}')>"

    def get_course(self):
        return self.course
