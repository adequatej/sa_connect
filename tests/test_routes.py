import datetime
import os
from app.application.application_models import SAApplication, SAPosition
import pytest
from app import create_app, db
from app.course.course_models import Course, CourseExperience, CourseSection
from app.user.user_models import Faculty, Student
from config import Config
import sqlalchemy as sqla

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.test_request_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_student(username, email, passwd, first_name, last_name, phone_number, wpi_id, major, cum_gpa, grad_year):
    user = Student(username = username, email = email, first_name = first_name, last_name = last_name, phone_number = phone_number, wpi_id = wpi_id, major = major, cum_gpa = cum_gpa, grad_year = grad_year)
    user.set_password(passwd)
    return user

def new_faculty(username, email, passwd, first_name, last_name, phone_number, wpi_id, department):
    user = Faculty(username = username, email = email, first_name = first_name, last_name = last_name, phone_number = phone_number, wpi_id = wpi_id, department = department)
    user.set_password(passwd)
    return user

@pytest.fixture
def init_database(request,test_client):
    # Create the database and the database table
    db.create_all()
    # initialize all courses
    if Course.query.count() == 0:
        courses = [{'major':'CS','coursenum':'1101'},
            {'major':'DS','coursenum':'4432'},
            {'major':'RBE','coursenum':'2010'},
            {'major':'ME','coursenum':'2221'}, 
            {'major':'MA','coursenum': '3031'},
            {'major':'CS','coursenum':'2303'},
            {'major':'CS','coursenum':'3733'},
            {'major':'CS','coursenum':'3013'},
            {'major':'DS','coursenum':'4441'}, 
            {'major':'MA','coursenum': '1024'}  ]
        for c in courses:
            db.session.add(Course(major = c['major'], coursenum = c['coursenum']))
        db.session.commit()

    
    # add users
    student_user = new_student('student1', 'student@wpi.edu', '123', 'Stu', 'Dent', '1234567890', '123456789', 'CS', 3.0, 2026)
    db.session.add(student_user)
    faculty_user = new_faculty('faculty1', 'faculty@wpi.edu', '123', 'Fac', 'Ulty', '0987654321', '987654321', 'Computer Science')
    db.session.add(faculty_user)
    db.session.commit()

    # Create course experiences for all courses for student
    courses = db.session.scalars(sqla.select(Course)).all()
    for c in courses:
        db.session.add(CourseExperience(course_id=c.id, user_id=student_user.id))
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_student_register_page(request,test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/register' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/student/register')
    assert response.status_code == 200
    assert b"Student Registration" in response.data

def test_student_register(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student/register', 
                          data=dict(username='test', email='test@wpi.edu',password="bad",confirm_password="bad", first_name='Test',last_name='Me', phone_number='4545687954', wpi_id='555555544', major='DS', gpa=2.0, graduation_year='2027'),
                          follow_redirects = True)
    assert response.status_code == 200
    # get the data for the new user from DB
    s = db.session.scalars(sqla.select(Student).where(Student.username == 'test')).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(Student.username == 'test'))

    assert s.last_name == 'Me'
    assert s_count == 1
    assert b"Registration successful!" in response.data

def test_faculty_register_page(request,test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/register' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/faculty/register')
    assert response.status_code == 200
    assert b"Faculty Registration" in response.data

def test_faculty_register(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/faculty/register', 
                          data=dict(username='testfac', email='testfac@wpi.edu',password="bad",confirm_password="bad", first_name='Test',last_name='Me', phone_number='4545687957', wpi_id='555455544', department='Computer Science'),
                          follow_redirects = True)
    assert response.status_code == 200
    # get the data for the new user from DB
    s = db.session.scalars(sqla.select(Faculty).where(Faculty.username == 'testfac')).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(Faculty.username == 'testfac'))

    assert s.last_name == 'Me'
    assert s_count == 1
    assert b"Registration successful!" in response.data

def test_invalidlogin(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='none', password='none',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data 
    assert b"Login" in response.data 

# ------------------------------------
# Helper functions

def do_login(test_client, path , username, passwd):
    response = test_client.post(path, 
                          data=dict(username= username, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome," in response.data

def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to index page after logout. 
    assert b"logged out" in response.data
    assert b"Welcome to SA Connect" in response.data
# ------------------------------------

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    do_login(test_client, path = '/login', username = 'student1', passwd = '123')

    do_logout(test_client, path = '/logout')

    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')

    do_logout(test_client, path = '/logout')

def test_student_edit_profile_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/edit-profile' page is requested (GET)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'student1', passwd = '123')
    response = test_client.get('/student/edit-profile')
    assert response.status_code == 200
    assert b"Edit Student Profile" in response.data
    do_logout(test_client, path = '/logout')

def test_student_edit_profile(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/edit-profile' page is submitted (POST)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'student1', passwd = '123')
    response = test_client.post('/student/edit-profile', 
                          data=dict(email='student@wpi.edu', first_name='Stu',last_name='Dent', phone_number='1234567890',major='DS', cum_gpa=2.0, grad_year=2026, courses_taken=[], courses_served=[], submit_button='scroll'),
                          follow_redirects = True)
    assert response.status_code == 200
    # Assumptions: page redirects to itself
    assert Student.query.filter_by(username='student1').first().major == 'DS'
    assert b"DS" in response.data
    assert b"Student profile updated" in response.data
    do_logout(test_client, path = '/logout')

def test_faculty_edit_profile_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/edit-profile' page is requested (GET)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    response = test_client.get('/faculty/edit-profile')
    assert response.status_code == 200
    assert b"Edit Faculty Profile" in response.data
    do_logout(test_client, path = '/logout')

def test_faculty_edit_profile(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/edit-profile' page is submitted (POST)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    response = test_client.post('/faculty/edit-profile', 
                          data=dict(email='faculty@wpi.edu', first_name='Fac',last_name='Ulty', phone_number='0987654321',department='Data Science'),
                          follow_redirects = True)
    assert response.status_code == 200
    # Assumptions: page redirects to itself
    assert Faculty.query.filter_by(username='faculty1').first().department == 'Data Science'
    assert b"Data Science" in response.data
    assert b"Faculty profile updated" in response.data
    do_logout(test_client, path = '/logout')

def test_student_course_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/course/<int:course_id>' page is requested (GET)
    THEN check that the response is valid
    """
    course_id = Course.query.filter_by(coursenum = '1101').first().id
    do_login(test_client, path = 'login', username = 'student1', passwd = '123')
    response = test_client.get('/student/course/'+str(course_id))
    assert response.status_code == 200
    assert b"Taken Course" in response.data
    assert b"Term Taken" in response.data
    do_logout(test_client, path = '/logout')

def test_student_edit_course(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/course/<int:course_id>' page is submitted (POST)
    THEN check that the response is valid
    """
    course = Course.query.filter_by(coursenum = '1101').first()
    course_id = course.id
    experience = CourseExperience.query.filter_by(course=course).first()
    do_login(test_client, path = 'login', username = 'student1', passwd = '123')
    response = test_client.post('/student/course/'+str(course_id),
                               data=dict(been_sa=True, has_taken=True, grade='A', term_taken='2022-E2', submit_button='scroll'),
                               follow_redirects = True)
    assert response.status_code == 200
    assert experience.term_taken == '2022-E2'
    assert b"Course experience updated" in response.data
    assert b"My Courses" in response.data
    do_logout(test_client, path = '/logout')

def test_create_course_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/course/create' page is requested (GET)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    response = test_client.get('/course/create')
    assert response.status_code == 200
    # Assumptions: page redirects to index
    assert b"Create a New Class" in response.data
    do_logout(test_client, path = '/logout')

def test_create_course(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/course/create' page is submitted (POST)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    course = Course.query.filter_by(coursenum='1101').first()
    response = test_client.post('/course/create', 
                          data=dict(section_number=10, course_choices=course.id, term='2024-A'),
                          follow_redirects = True)
    assert response.status_code == 200
    assert CourseSection.query.filter_by(term = '2024-A', section_number = 10).first() is not None
    assert b"is created" in response.data
    do_logout(test_client, path = '/logout')

def test_create_sa_position_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/create' page is requested (GET)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    response = test_client.get('/faculty/create')
    assert response.status_code == 200
    assert b"Create SA Position" in response.data
    do_logout(test_client, path = '/logout')

def test_create_sa_position_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/create' page is submitted (POST)
    THEN check that the response is valid
    """
    new_section = CourseSection(section_number = 3,
                                 instructor=Faculty.query.filter_by(username='faculty1').first(),
                                 course=Course.query.filter_by(coursenum='1101').first(), term='2024-A')
    db.session.add(new_section)
    db.session.commit()
    assert CourseSection.query.filter_by(section_number = 3, term='2024-A').first().course.coursenum == '1101'
    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    response = test_client.post('/faculty/create',
                                data=dict(course_section=CourseSection.query.first().id, number_of_sas=1, min_gpa=2.0, min_grade='B', prior_experience=False),
                                follow_redirects = True)
    assert response.status_code == 200
    assert SAPosition.query.first().min_grade == 'B'
    assert b"SA Position created successfully!" in response.data
    assert b"1101" in response.data
    do_logout(test_client, path = '/logout')

def test_apply_page(request, test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/apply/<int:pos_id>' page is requested (GET)
    THEN check that the response is valid
    """
    new_section = CourseSection(section_number = 1,
                                 instructor=Faculty.query.filter_by(username='faculty1').first(),
                                 course=Course.query.filter_by(coursenum='2303').first(), term='2024-A')
    db.session.add(new_section)
    new_position = SAPosition(course_section=new_section, number_of_sas=1, min_gpa=2.0, min_grade='B', prior_experience=False, current_date = datetime.datetime.now(datetime.timezone.utc).date())
    db.session.add(new_position)
    db.session.commit()

    pos_id = new_position.id

    do_login(test_client, path = '/login', username = 'student1', passwd = '123')
    response = test_client.get('/student/apply/'+str(pos_id))
    assert response.status_code == 200
    assert b"Apply For SA Position" in response.data
    assert b"2303" in response.data
    do_logout(test_client, path = '/logout')

def test_apply_and_withdraw(request, test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/apply/<int:pos_id>' page is submitted (POST)
    THEN check that the response is valid
    WHEN the '/student/withdraw_application/<int:application_id>' page is submitted (POST)
    THEN check that the response is valid
    """
    new_section = CourseSection(section_number = 20,
                                 instructor=Faculty.query.filter_by(username='faculty1').first(),
                                 course=Course.query.filter_by(coursenum='2303').first(), term='2024-A')
    db.session.add(new_section)
    new_position = SAPosition(course_section=new_section, number_of_sas=1, min_gpa=2.0, min_grade='B', prior_experience=False, current_date = datetime.datetime.now(datetime.timezone.utc).date())
    db.session.add(new_position)
    db.session.commit()

    pos_id = new_position.id

    do_login(test_client, path = '/login', username = 'student1', passwd = '123')
    response = test_client.post('/student/apply/'+str(pos_id),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"SA Application successful" in response.data
    assert b"Withdraw" in response.data

    app_id = SAApplication.query.first().id
    response = test_client.post('/withdraw_application/'+str(app_id),
                                follow_redirects=True)
    assert response.status_code == 200
    assert len(SAApplication.query.all()) == 0

    do_logout(test_client, path = '/logout')

def test_view_and_approve_application(request, test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/faculty/view-applications/<int:pos_id>' page is requested (GET)
    THEN check that the response is valid
    WHEN the '/faculty/approve_application/<int:app_id>' page is submitted (POST)
    THEN check that the response is valid
    """
    new_section = CourseSection(section_number = 21,
                                 instructor=Faculty.query.filter_by(username='faculty1').first(),
                                 course=Course.query.filter_by(coursenum='2303').first(), term='2024-A')
    db.session.add(new_section)
    new_position = SAPosition(course_section=new_section, number_of_sas=1, min_gpa=2.0, min_grade='B', prior_experience=False, current_date = datetime.datetime.now(datetime.timezone.utc).date())
    db.session.add(new_position)
    new_application = SAApplication(student = Student.query.filter_by(username='student1').first(),
                                    saPosition = new_position,
                                    grade = 'A',
                                    year_term_course = '2020-A',
                                    year_term_apply = '2024-B',
                                    is_assigned = False)
    db.session.add(new_application)
    db.session.commit()

    pos_id = new_position.id
    app_id = new_application.id

    do_login(test_client, path = '/login', username = 'faculty1', passwd = '123')
    response = test_client.get('/faculty/view-applications/'+str(pos_id))
    assert len(SAApplication.query.all()) == 1
    assert b"Applications for CS 2303" in response.data
    assert b"Stu Dent" in response.data

    response = test_client.post('/faculty/approve_application/'+str(app_id),
                               follow_redirects = True)
    assert b"Application approved successfully" in response.data
    assert b"Already Hired" in response.data

    do_logout(test_client, path = '/logout')



