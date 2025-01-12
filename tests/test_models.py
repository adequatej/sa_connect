import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.user.user_forms import FacultyEditProfileForm, StudentEditProfileForm, StudentRegistrationForm, FacultyRegistrationForm, LoginForm, EditCourseExperience
from app.user.user_models import User, Student, Faculty
from app.course.course_models import CourseExperience, CourseSection
from app.application.application_models import SAApplication, SAPosition
from app.course.course_models import Course, CourseExperience
from app.static import recommended
from app.user import user_blueprint as bp_user
from config import Config
from datetime import date

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



    def test_password_hashing(self):
        u = User(username='jacob', email='jjlu@wpi.edu')
        u.set_password('iluvcats')
        self.assertFalse(u.check_password('hatekittens'))
        self.assertTrue(u.check_password('iluvcats'))
        self.assertEqual(u.check_password('iluvcats'),True, 'Password check is good')

    def test_get_id(self):
        u = User(username='jacob', email='jjlu@wpi.edu')
        self.assertEqual(u.get_id(),'jacob')
    def test_student_repr(self):
        s = Student(username='kbacon', email='kbacon@wpi.edu', first_name='Kevin', last_name='Bacon', phone_number='1234567891', wpi_id='901019090', major='CS', cum_gpa=1.23, grad_year=2027)
        self.assertEqual(s.__repr__(),"<Student(id=None, major='CS', email='kbacon@wpi.edu')>" )
       
    def test_faculty_repr(self):
        f = Faculty(username='jsmith', email='jjsmith@wpi.edu', first_name='John', last_name='Smith', phone_number='9876543219', wpi_id='901019090', department = 'CS')
        self.assertEqual(f.__repr__(),"<Faculty(id=None, department='CS')>" )
       
    def test_Student_take_course(self):
        course = Course(major='CS', coursenum='3733')
        db.session.add(course)
        db.session.commit()
        s = Student(username='kbacon', email='kbacon@wpi.edu', first_name='Kevin', last_name='Bacon', phone_number='1234567891', wpi_id='901019090', major='CS', cum_gpa=1.23, grad_year=2027)
        db.session.add(s)
        db.session.commit()
        s.set_password('iluvcats')
        s.take_course(course, 'A', '2024A')
        self.assertEqual(s.experiences[0].grade, 'A')
    
    def test_Faculty_get_course_sections(self):
        f = Faculty(username='jsmith', email='jjsmith@wpi.edu', first_name='John', last_name='Smith', phone_number='9876543219', wpi_id='901019090', department = 'CS')
        db.session.add(f)
        db.session.commit()
        course = Course(major='CS', coursenum='3733')
        db.session.add(course)
        db.session.commit()
        courseS = CourseSection(section_number='1',term="2024A", course_id=course.id,instructor_id=f.id)
        db.session.add(courseS)
        db.session.commit()
        self.assertEqual(len(f.get_course_sections()),1)
        self.assertEqual((f.get_course_sections()[0]).term,'2024A')
        courseS2 = CourseSection(section_number='1',term="2024B", course_id=course.id,instructor_id=f.id)
        db.session.add(courseS2)
        db.session.commit()
        self.assertEqual(len(f.get_course_sections()),2)
        self.assertEqual((f.get_course_sections()[1]).term,'2024B')

    def test_Student_get_SAApplications(self):
        s = Student(username='kbacon', email='kbacon@wpi.edu', first_name='Kevin', last_name='Bacon', phone_number='1234567891', wpi_id='901019090', major='CS', cum_gpa=1.23, grad_year=2027)
        db.session.add(s)
        db.session.commit()
        sap = SAApplication(position_id=-1, student_id=s.id, grade="", year_term_course="", year_term_apply="", is_assigned=False)
        db.session.add(sap)
        db.session.commit()
        self.assertEqual(s.get_SAApplications()[0],sap)




    def test_CourseSection_repr(self):
        courseS = CourseSection(section_number='1',term="2024A")
        self.assertEqual(courseS.__repr__(),"<CourseSection(id=None, course='None', section_number='1')>")

    def test_CourseSection_get_sa_positions(self):
        courseS = CourseSection(section_number='1',term="2024A", course_id=-1,instructor_id=-1)
        db.session.add(courseS)
        db.session.commit()
        saPos = SAPosition(course_section_id = courseS.id, number_of_sas = 3, min_gpa=3.0, min_grade='A', prior_experience=True, current_date = "test")
        db.session.add(saPos)
        db.session.commit()
        self.assertEqual(len(courseS.get_sa_positions()), 1)
        self.assertEqual(courseS.get_sa_positions()[0].number_of_sas,3)
        saPos2 = SAPosition(course_section_id = courseS.id, number_of_sas = 1, min_gpa=3.0, min_grade='C', prior_experience=False, current_date = "12/11/2024")
        db.session.add(saPos2)
        db.session.commit()
        self.assertEqual(len(courseS.get_sa_positions()), 2)
        self.assertEqual(courseS.get_sa_positions()[1].number_of_sas,1)

    def test_CourseSection_get_course(self):
        course = Course(major='CS', coursenum='3733')
        db.session.add(course)
        db.session.commit()
        courseS = CourseSection(section_number='1',term="2024A", course_id=-1,instructor_id=-1)
        courseS.assign_course(course.id)
        db.session.add(courseS)
        db.session.commit()
        self.assertEqual(courseS.get_course().major, 'CS')
        self.assertEqual(courseS.get_course().coursenum, '3733')


    def test_Course_get_experiences(self):
        course = Course(major='CS', coursenum='3733')
        db.session.add(course)
        db.session.commit()
        courseXP = CourseExperience(course_id=course.id, user_id=-1, has_taken=True, been_sa=True, grade='A', term_taken='2023A')
        db.session.add(courseXP)
        db.session.commit()
        experiences = course.get_experiences()
        self.assertEqual(experiences[0].has_taken, True)


    def test_Course_get_course_sections(self):
        course = Course(major='CS', coursenum='3733')
        db.session.add(course)
        db.session.commit()
        courseS = CourseSection(section_number='1',term="2024A", course_id=course.id,instructor_id=-1)
        db.session.add(courseS)
        db.session.commit()
        sections = course.get_course_sections()
        self.assertEqual(sections[0].term,'2024A')
        courseS2 = CourseSection(section_number='1',term="2024B", course_id=course.id,instructor_id=-1)
        db.session.add(courseS2)
        db.session.commit()
        sections = course.get_course_sections()
        self.assertEqual(sections[1].term,'2024B')


    def test_CourseExperience_get_course(self):
        course = Course(major='CS', coursenum='3733')
        db.session.add(course)
        db.session.commit()
        courseXP = CourseExperience(course_id=course.id, user_id=-1, has_taken=True, been_sa=True, grade='A', term_taken='2023A')
        db.session.add(courseXP)
        db.session.commit()
        self.assertEqual(courseXP.get_course().major,'CS')
        self.assertEqual(courseXP.get_course().coursenum,'3733')


    


    



    def test_SAApplication_get_student(self):
        s = Student(username='kbacon', email='kbacon@wpi.edu', first_name='Kevin', last_name='Bacon', phone_number='1234567891', wpi_id='901019090', major='CS', cum_gpa=1.23, grad_year=2027)
        db.session.add(s)
        db.session.commit()
        sap = SAApplication(position_id=-1, student_id=s.id, grade="", year_term_course="", year_term_apply="", is_assigned=False)
        db.session.add(sap)
        db.session.commit()
        self.assertEqual(sap.get_student(), s)

    def test_SAApplication_get_saPosition(self):
        saPos = SAPosition(course_section_id = -1, number_of_sas = 3, min_gpa=3.0, min_grade='A', prior_experience=True, current_date = "test")
        db.session.add(saPos)
        db.session.commit()
        sap = SAApplication(position_id=saPos.id, student_id=-1, grade="", year_term_course="", year_term_apply="", is_assigned=False)
        db.session.add(sap)
        db.session.commit()
        self.assertEqual(sap.get_saPosition(), saPos)
    
    def test_SAPosition_apply(self):
        saPos = SAPosition(course_section_id = -1, number_of_sas = 3, min_gpa=3.0, min_grade='A', prior_experience=True, current_date = "test")
        db.session.add(saPos)
        db.session.commit()
        saPos.apply(1, 1, 'A', '2024A', '2024B', False)
        self.assertEqual(saPos.saApplications[0].grade, 'A')
        saPos.apply(2, 2, 'B', '2024D', '2025B', False)
        self.assertEqual(saPos.saApplications[1].grade, 'B')



    def test_SAPosition_get_applications(self):
        
        saPos = SAPosition(course_section_id = -1, number_of_sas = 3, min_gpa=3.0, min_grade='A', prior_experience=True, current_date = "test")
        db.session.add(saPos)
        db.session.commit()
        sap = SAApplication(position_id=saPos.id, student_id=-1, grade="", year_term_course="", year_term_apply="", is_assigned=False)
        
        db.session.add(sap)
        db.session.commit()


        self.assertEqual(len(saPos.get_saApplications()), 1)
        sap2 = SAApplication(position_id=saPos.id, student_id=-1, grade="B", year_term_course="", year_term_apply="", is_assigned=False)
        
        db.session.add(sap2)
        db.session.commit()
        self.assertEqual(saPos.get_saApplications()[1].grade, "B")

    def test_SAPosition_get_applications(self):
        courseS2 = CourseSection(section_number='1',term="2024B", course_id=1,instructor_id=1)
        db.session.add(courseS2)
        db.session.commit()
        saPos = SAPosition(course_section_id = courseS2.id, number_of_sas = 3, min_gpa=3.0, min_grade='A', prior_experience=True, current_date = "test")
        db.session.add(saPos)
        db.session.commit()
        
        self.assertEqual(saPos.get_course_section().term, "2024B")
