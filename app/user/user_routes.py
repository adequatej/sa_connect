from flask import render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.user.user_forms import FacultyEditProfileForm, StudentEditProfileForm, StudentRegistrationForm, FacultyRegistrationForm, LoginForm, EditCourseExperience
from app.user.user_models import User, Student, Faculty
from app.course.course_models import CourseExperience, CourseSection
from app.application.application_models import SAApplication, SAPosition
from app.course.course_models import Course, CourseExperience
from app.static import recommended
from app.user import user_blueprint as bp_user
import sqlalchemy as sqla
import identity.web
from config import Config as app_config
from flask_session import Session 

auth = None

@bp_user.record
def record_auth(setup_state):
    global auth
    auth = identity.web.Auth(
        session=session,
        authority=setup_state.app.config["AUTHORITY"],
        client_id=setup_state.app.config["CLIENT_ID"],
        client_credential=setup_state.app.config["CLIENT_SECRET"],
    )
@bp_user.route('/')
@bp_user.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()  

    if not current_user.is_authenticated:
        return render_template('index.html', form=form)

    isStudent = isinstance(current_user, Student)
    listOfRelevantPos = []
    facultyCourses = []
    SAPosCourses = []
    applications = []

    if isStudent:
        studentCourses = db.session.scalars(sqla.select(CourseExperience).where(CourseExperience.has_taken == True)).all()
        SAPosCourses = db.session.scalars(sqla.select(SAPosition)).all()
        applications = db.session.scalars(sqla.select(SAApplication).where(SAApplication.student_id==current_user.id)).all()

        for app in applications:
            if app.saPosition in SAPosCourses:
                SAPosCourses.remove(app.saPosition)

        SAPosCourses = sorted(SAPosCourses, key=lambda pos: recommended.get_weight(current_user, pos), reverse=True)

        for pos in SAPosCourses:
            if recommended.meets_requirements(current_user, pos):
                listOfRelevantPos.append(pos)
        listOfRelevantPos = sorted(listOfRelevantPos, key=lambda pos: recommended.get_weight(current_user, pos), reverse=True)

        for pos in listOfRelevantPos:
            SAPosCourses.remove(pos)

    elif isinstance(current_user, Faculty):
        facultyCourses = db.session.scalars(
            sqla.select(CourseSection).where(CourseSection.instructor_id == current_user.id)).all()
        faculty_section_ids = [section.id for section in facultyCourses]
        SAPosCourses = db.session.scalars(
            sqla.select(SAPosition).where(SAPosition.course_section_id.in_(faculty_section_ids))).all()

    return render_template('index.html',
                         applications=applications,
                         facultyCourses=facultyCourses,
                         current_user=current_user,
                         isStudent=isStudent,
                         is_faculty=isinstance(current_user, Faculty),
                         listOfRelevantPos=listOfRelevantPos,
                         SAPosCourses=SAPosCourses,
                         form=form)

@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=form.username.data).first() or \
               Faculty.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user.index'))
    
    return render_template('login.html', form=form, auth=auth)  

@bp_user.route('/login/azure')
def login_azure():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    if auth is None:
        flash("Authentication not configured", "error")
        return redirect(url_for('user.login'))

    try:
        # Generate the Azure login URL
        auth_data = auth.log_in(
            scopes=current_app.config["SCOPE"],
            redirect_uri=url_for("user.auth_response", _external=True),
            prompt="select_account"
        )
        print("Generated auth data:", auth_data)
        
        if 'auth_uri' in auth_data:
            return redirect(auth_data['auth_uri'])
            
        flash("Failed to generate authentication URL", "error")
        return redirect(url_for('user.login'))
        
    except Exception as ex:
        print(f"Exception in login_azure: {str(ex)}")
        flash(f"Failed to initiate login: {str(ex)}", "error")
        return redirect(url_for('user.login'))

@bp_user.route("/getAToken")
def auth_response():
    try:
        result = auth.complete_log_in(request.args)
        print("Auth result:", result)
        
        if "error" in result:
            print("Error in result:", result["error"])
            return render_template("auth_error.html", result=result)
        
        if "preferred_username" in result:
            email = result["preferred_username"]
            print(f"Looking up user with email: {email}")
            
            # Look for user in both Student and Faculty tables
            user = Student.query.filter_by(email=email).first() or \
                   Faculty.query.filter_by(email=email).first()
            
            if user is None:
                print(f"No user found for email: {email}")
                flash(f"No account found with email: {email}. Please register first.", "error")
                return redirect(url_for("user.register_student"))

            print(f"Found user: {user}")
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('user.index')
            return redirect(next_page)

        print("No email found in token")
        flash("Authentication failed: No email information received", "error")
        return redirect(url_for('user.login'))
        
    except Exception as ex:
        print(f"Exception in auth_response: {str(ex)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        flash(f"Authentication failed: {str(ex)}", "error")
        return redirect(url_for('user.login'))

@bp_user.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('user.index')) 

@bp_user.route('/student/register', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()

    if form.validate_on_submit():
        new_user = Student(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            wpi_id=form.wpi_id.data,
            major=form.major.data,
            grad_year=form.graduation_year.data,
            cum_gpa=form.gpa.data,
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)

        # Create course experiences for all courses
        courses = db.session.scalars(sqla.select(Course)).all()
        for c in courses:
            db.session.add(CourseExperience(course_id=c.id, user_id=new_user.id))
        db.session.commit()
       
        # Update course experiences based on form data
        for c in form.courses_served.data:
            experience = CourseExperience.query.filter_by(course=c, user=new_user).first()
            experience.been_sa = True
        for c in form.courses_taken.data:
            experience = CourseExperience.query.filter_by(course=c, user=new_user).first()
            experience.has_taken = True
            
        db.session.commit()
        flash('Registration successful! Please log in with your WPI account.', 'success')
        return redirect(url_for('user.index'))  
        
    return render_template('register_student.html', form=form)

@bp_user.route('/faculty/register', methods=['GET', 'POST'])
def register_faculty():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    form = FacultyRegistrationForm()
    if form.validate_on_submit():
        new_user = Faculty(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            wpi_id=form.wpi_id.data,
            department=form.department.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in with your WPI account.', 'success')
        return redirect(url_for('user.index')) 
        
    return render_template('register_faculty.html', form=form)

# Profile editing routes
@bp_user.route('/student/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_student_profile():
    if not isinstance(current_user, Student):
        flash("Unauthorized access", "danger")
        return redirect(url_for('user.index'))
    
    form = StudentEditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.major = form.major.data
        current_user.cum_gpa = form.cum_gpa.data
        current_user.grad_year = form.grad_year.data

        # Update course experiences
        experiences = CourseExperience.query.filter_by(user=current_user).all()
        for e in experiences:
            e.has_taken = False
            e.been_sa = False
        for c in form.courses_served.data:
            experience = CourseExperience.query.filter_by(course=c, user=current_user).first()
            experience.been_sa = True
        for c in form.courses_taken.data:
            experience = CourseExperience.query.filter_by(course=c, user=current_user).first()
            experience.has_taken = True
        db.session.commit()
        flash('Student profile updated successfully!')
        
        if request.form['submit_button'] == 'scroll':
            return redirect(url_for('user.edit_student_profile', _anchor='courses_card'))
        return redirect(url_for('user.edit_student_profile', _anchor='profile_card'))

    if request.method == 'GET':
        experiences = CourseExperience.query.filter_by(user=current_user).all()
        for e in experiences:
            if e.been_sa:
                form.courses_served.data.append(e.course)
            if e.has_taken:
                form.courses_taken.data.append(e.course)
    
    return render_template('edit_student_profile.html', 
                         form=form, 
                         courses=db.session.query(CourseExperience)
                         .filter(CourseExperience.user == current_user, 
                                sqla.or_(CourseExperience.has_taken, CourseExperience.been_sa))
                         .join(CourseSection.course)
                         .order_by(CourseExperience.been_sa.desc(), Course.major, Course.coursenum)
                         .all())

@bp_user.route('/faculty/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_faculty_profile():
    if not isinstance(current_user, Faculty):
        flash("Unauthorized access")
        return redirect(url_for('user.index'))
    
    form = FacultyEditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.department = form.department.data
        db.session.commit()
        flash('Faculty profile updated successfully!')
        return redirect(url_for('user.edit_faculty_profile'))
    
    return render_template('edit_faculty_profile.html', form=form, is_faculty=True)

@bp_user.route('/student/course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(course_id):
    if not isinstance(current_user, Student):
        flash("Unauthorized access", "danger")
        return redirect(url_for('user.index'))
    
    experience = db.session.query(CourseExperience).filter(
        CourseExperience.course_id == course_id, 
        CourseExperience.user == current_user
    ).first()
    
    form = EditCourseExperience(obj=experience)
    if form.validate_on_submit():
        experience.been_sa = form.been_sa.data
        experience.has_taken = form.has_taken.data
        experience.grade = form.grade.data
        experience.term_taken = form.term_taken.data
        db.session.commit()
        flash('Course experience updated successfully!')
        return redirect(url_for('user.edit_student_profile', _anchor='courses_card'))
    
    return render_template('edit_experience.html', form=form, course=experience.course)