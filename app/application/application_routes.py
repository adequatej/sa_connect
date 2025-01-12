from flask import jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user
from app import db
from app.application.application_forms import CreateSAPositionForm, ApplyForSAPosition
from app.application.application_models import SAPosition, SAApplication
from app.user.user_models import Faculty
from app.user import user_blueprint as bp_user
from app.course.course_models import CourseSection, Course, CourseExperience
from datetime import date, datetime
from datetime import timezone
from app.static import recommended
import datetime
import sqlalchemy.orm as sqlo
import sqlalchemy as sqla



@bp_user.route('/faculty/create', methods=['GET', 'POST'])
@login_required
def create_sa_position():
    # Check if the current user is a Faculty member
    if not isinstance(current_user, Faculty):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.index'))


    form = CreateSAPositionForm()


    # Populate the course section dropdown
    course_sections = CourseSection.query.filter_by(instructor_id=current_user.id).join(CourseSection.course).order_by(Course.major, Course.coursenum, CourseSection.term, CourseSection.section_number).all()
    form.course_section.choices = [(str(section.id), f"{section.course.major} {section.course.coursenum} - {section.section_number} - {section.term}") for section in course_sections]

    if form.validate_on_submit():
        sa_position = SAPosition(
            course_section_id=form.course_section.data,
            number_of_sas=form.number_of_sas.data,
            min_gpa=form.min_gpa.data,
            min_grade=form.min_grade.data,
            prior_experience=form.prior_experience.data,
            current_date = datetime.datetime.now(timezone.utc).date()

        )
        db.session.add(sa_position)
        db.session.commit()
        flash('SA Position created successfully!', 'success')
        return redirect(url_for('user.index'))  # fix to reflect faculty main page

    return render_template('create.html', form=form, is_faculty=True)



@bp_user.route('/student/apply/<int:pos_id>', methods=['GET', 'POST'])
@login_required
def apply(pos_id):
    if isinstance(current_user, Faculty):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('user.index'))

    form = ApplyForSAPosition()
    pos = SAPosition.query.get_or_404(pos_id)

    existing_application = SAApplication.query.filter_by(student_id=current_user.id, position_id=pos_id).first()
    if existing_application:
        flash('You have already applied for this position.', 'warning')
        return redirect(url_for('user.index'))

    experience = db.session.query(CourseExperience).filter(
        CourseExperience.user == current_user,
        CourseExperience.course == pos.course_section.course
    ).first()

    term_course = 'None'
    course_grade = 'NA'
    if experience and experience.has_taken:
        term_course = experience.term_taken
        course_grade = experience.grade

    if form.validate_on_submit():
        sa_application = SAApplication(
            student=current_user,
            position_id=pos.id,
            grade=course_grade,
            year_term_course=term_course,
            year_term_apply=pos.course_section.term
        )
        db.session.add(sa_application)
        db.session.commit()
        flash('SA Application successful!', 'success')
        return redirect(url_for('user.index'))

    sa_experience = "Yes" if db.session.query(CourseExperience).filter(
        CourseExperience.user == current_user,
        CourseExperience.been_sa == True
    ).first() else "No"

    return render_template(
        'applicationForm.html',
        form=form,
        pos=pos,
        experience=experience,
        sa_experience=sa_experience
    )



@bp_user.route('/replace', methods=['POST'])
def replace():
    print("called replace")
    listOfRelevantPos= []
    facultyCourses = []
    SAPosCourses = []
    isStudent=True
    test=[]
    other=[]
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
    for pos in listOfRelevantPos:
        course = {'major': pos.course_section.course.major,
                  'coursenum': pos.course_section.course.coursenum}
        instructor = {'email': pos.course_section.instructor.email,
                      'first_name': pos.course_section.instructor.first_name,
                      'last_name': pos.course_section.instructor.last_name,
                      }


        courseS={'id': pos.course_section.id,
                 'instructor': pos.course_section.instructor_id,
                 'section_number': pos.course_section.section_number,
                 'term':pos.course_section.term,
                 'instructor': instructor,
                 'course': course
                     }
        test.append({'id': pos.id,
                     'min_gpa': pos.min_gpa,
                     'min_grade': pos.min_grade,
                     'prior_experience': pos.prior_experience,
                     'current_date': pos.current_date,
                     'number_of_sas': pos.number_of_sas,
                     'course_section': courseS,
                     })
       

    for pos in SAPosCourses:
        course = {'major': pos.course_section.course.major,
                  'coursenum': pos.course_section.course.coursenum}
        instructor = {'email': pos.course_section.instructor.email,
                      'first_name': pos.course_section.instructor.first_name,
                      'last_name': pos.course_section.instructor.last_name,
                      }

        courseS={'id': pos.course_section.id,
                 'instructor': pos.course_section.instructor_id,
                 'section_number': pos.course_section.section_number,
                 'term':pos.course_section.term,
                 'instructor': instructor,
                 'course': course
                     }
        other.append({'id': pos.id,
                     'min_gpa': pos.min_gpa,
                     'min_grade': pos.min_grade,
                     'prior_experience': pos.prior_experience,
                     'current_date': pos.current_date,
                     'number_of_sas': pos.number_of_sas,
                     'course_section': courseS
                     })
    return jsonify({'test':test,'other':other})



@bp_user.route('/withdraw_application/<int:application_id>', methods=['POST'])
def withdraw_application(application_id):
    print("AJIOJFA")
    application = SAApplication.query.get(application_id)
    db.session.delete(application)
    db.session.commit()
    test = []

    applications = []
    course_section = []
    studentCourses = db.session.scalars(sqla.select(CourseExperience).where(CourseExperience.has_taken == True)).all()
    SAPosCourses = db.session.scalars(sqla.select(SAPosition)).all()
    applications = db.session.scalars(sqla.select(SAApplication).where(SAApplication.student_id == current_user.id)).all()
    saPosition = {}
    courseS = {}
   
    for appl in applications:
        course = {'major': appl.saPosition.course_section.course.major,
                  'coursenum': appl.saPosition.course_section.course.coursenum}
        instructor = {'email': appl.saPosition.course_section.instructor.email,
                      'first_name': appl.saPosition.course_section.instructor.first_name,
                      'last_name': appl.saPosition.course_section.instructor.last_name,
                      }
        courseS = {'id': appl.saPosition.course_section.id,
                   'instructor': appl.saPosition.course_section.instructor_id,
                   'section_number': appl.saPosition.course_section.section_number,
                   'term': appl.saPosition.course_section.term,
                   'instructor': instructor,
                   'course': course
                  }
        saPosition = {'id': appl.saPosition.id,
                      'course_section': courseS}
        test.append({'id': appl.id,
                     'position ID': appl.position_id,
                     'student ID': appl.student_id,
                     'grade': appl.grade,
                     'year_term_course': appl.year_term_course,
                     'year_term_apply': appl.year_term_apply,
                     'is_assigned': appl.is_assigned,
                     'saPosition': saPosition
                     })
   
    return jsonify(test), 200




@bp_user.route('/faculty/view-applications/<int:pos_id>', methods=['GET'])
@login_required
def view_applications(pos_id):
    if not isinstance(current_user, Faculty):
        flash("Access denied: Only faculty members can view applications.", "danger")
        return redirect(url_for('user.index'))

    sa_position = SAPosition.query.get_or_404(pos_id)
    if sa_position.course_section.instructor_id != current_user.id:
        flash("Access denied: You do not manage this position.", "danger")
        return redirect(url_for('user.index'))

    applications = db.session.query(SAApplication).filter_by(position_id=pos_id).all()
    application_data = []
    for application in applications:
        is_already_hired = db.session.query(SAApplication).filter(
            SAApplication.student_id == application.student_id,
            SAApplication.is_assigned == True
        ).first()
        application_data.append((application, bool(is_already_hired)))

    return render_template(
        'view_applications.html',
        sa_position=sa_position,
        applications=application_data,
        is_faculty=True
    )


@bp_user.route('/faculty/approve_application/<int:app_id>', methods=['POST'])
@login_required
def approve_application(app_id):
    if not isinstance(current_user, Faculty):
        flash("Access denied: Only faculty members can approve applications.", "danger")
        return redirect(url_for('user.index'))

    application = SAApplication.query.get_or_404(app_id)

    # Ensure the faculty member manages the position
    if application.saPosition.course_section.instructor_id != current_user.id:
        flash("Access denied: You do not manage this position.", "danger")
        return redirect(url_for('user.index'))

    # Check if the student is already hired
    is_hired = db.session.query(SAApplication).filter(
        SAApplication.student_id == application.student_id,
        SAApplication.is_assigned == True
    ).first()

    if is_hired:
        flash("This student is already hired for another position.", "warning")
        return redirect(url_for('user.view_applications', pos_id=application.position_id))

    # Ensure the maximum number of SAs hasn't been exceeded
    assigned_count = db.session.query(SAApplication).filter(
        SAApplication.position_id == application.position_id,
        SAApplication.is_assigned == True
    ).count()
    if assigned_count >= application.saPosition.number_of_sas:
        flash("Cannot approve: Maximum number of SAs already assigned.", "danger")
        return redirect(url_for('user.view_applications', pos_id=application.position_id))

    # Approve the application
    application.is_assigned = True
    db.session.commit()

    # Withdraw other applications for the same student
    application.withdraw_other_applications()

    flash("Application approved successfully! All other applications by this student have been withdrawn.", "success")
    return redirect(url_for('user.view_applications', pos_id=application.position_id))
