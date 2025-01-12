from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from werkzeug.security import generate_password_hash, check_password_hash
from app.user.user_models import Student
from app.course.course_models import CourseSection
from datetime import date

 
 
 
#SA Position Model
class SAPosition(db.Model):
    __tablename__ = 'sa_position'  # Explicitly defines the table name
    
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    course_section_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('course_section.id'), nullable=False)
    number_of_sas: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, nullable=False)
    min_gpa: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, nullable=False, default=0.0)  
    min_grade: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4), nullable=False, default="C")  
    prior_experience: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, nullable=False, default=False)  
    current_date : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), nullable = False)

    # Relationship
    saApplications: sqlo.Mapped[list['SAApplication']] = sqlo.relationship('SAApplication', back_populates='saPosition')

    course_section: sqlo.Mapped['CourseSection'] = sqlo.relationship('CourseSection', back_populates='sa_positions')

    def __repr__(self):
        return (
            f"<SAPosition(id={self.id}, course_section_id={self.course_section_id}, "
            f"number_of_sas={self.number_of_sas}, min_gpa={self.min_gpa}, "
            f"min_grade='{self.min_grade}', prior_experience={self.prior_experience})>"
        )
    def get_saApplications(self):
        return self.saApplications
    def get_course_section(self):
        return self.course_section
    
    def apply(self, course_section, sID, g, ytc, yta, isA):

        saAPP = SAApplication(position_id=self.id, student_id=sID, grade=g, year_term_course=ytc, year_term_apply=yta, is_assigned=isA)
        db.session.add(saAPP)
        db.session.commit()

class SAApplication(db.Model):    
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    position_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('sa_position.id'))
    student_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('student.id'))
    grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(2), nullable=False, default="C")  

    year_term_course : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), nullable=False, default="2020A")  
    year_term_apply : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), nullable=False, default="2020B")

    is_assigned: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)

    saPosition: sqlo.Mapped['SAPosition'] = sqlo.relationship('SAPosition', back_populates='saApplications')
    student: sqlo.Mapped['Student'] = sqlo.relationship('Student', back_populates='studentSAApplications')

   
    def __repr__(self):
        return (
            f"<SAApplication(id={self.id}, saPosition = {self.saPosition}, student_id={self.student_id}, position_id={self.position_id}, "
            f"grade='{self.grade}', year_term_course='{self.year_term_course}', year_term_apply='{self.year_term_apply}')>"
        )
    def get_saPosition(self):
        return self.saPosition
    def get_student(self):
        return self.student
    
    def withdraw_other_applications(self):
        other_applications = db.session.query(SAApplication).filter(
            SAApplication.student_id == self.student_id,
            SAApplication.id != self.id
        ).all()
        for app in other_applications:
            app.is_assigned = False  
            db.session.delete(app)  
        db.session.commit()