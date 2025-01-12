from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from app.user.user_models import Student
from app.application.application_models import SAPosition, SAApplication
from app.course.course_models import Course, CourseExperience

# How the relevant positions works:
# - The relevant positions is made up of all the positions for which the student matches ALL the required qualifications
#     - Meets the gpa requirement
#     - Meets the grade requirement
#       - If there is no grade requirement, the student must have either taken the course or passed a course in the same major with a higher course number
#     - If the position requires experience, the student must have previously SA'd ANY course
#     - THIS MEANS A COURSE MAY NOT BE RECOMENDED EVEN IF THE STUDENT PREVIOUSLY GOT AN 'A' OR SA'D THE COURSE IF THEY DON'T MEET ALL THE OTHER REQUIREMENTS
#
# - Both the relevant positions and the other positions are sorted based on an algorithm counting weight.
# - Things that affect weight include:
#   - If the student has previously SA'd this course
#   - If the student has taken the course
#   - How good of a grade the student earned when taking the course
#   - If the course is in the student's major
#   - The number of courses in the same major as the given course the student has taken, up to a certain point
#   - The ratio of applicants to available slots, affects the weight positively or negatively, up to a certain point

def get_weight(student, sa_position):
    # weights of different conditions
    prev_sa = 100
    taken_course = 20
    high_grade = 30
    mid_grade = 10
    in_major = 15
    per_related_course = 3 
    max_related_courses_counted = 5
    per_applications_openings_difference = 5 # Gives additional weight for more open slots or removes weight for having more applications than slots
    max_difference_counted = 5

    weight = 0
    experience = CourseExperience.query.filter_by(course = sa_position.course_section.course, user = student).first()
    if experience.been_sa:
        weight += prev_sa
    if experience.has_taken:
        weight += taken_course
        if experience.grade == "A":
            weight+=high_grade
        elif experience.grade == "B":
            weight+=mid_grade
    if student.major == experience.course.major:
        weight+=in_major
    num_apps = len(SAApplication.query.filter_by(saPosition = sa_position).all())
    num_openings = sa_position.number_of_sas
    if num_apps < num_openings:
        weight += min(num_openings - num_apps, max_difference_counted) * per_applications_openings_difference
    elif num_openings < num_apps:
        weight -= min(num_apps - num_openings, max_difference_counted) * per_applications_openings_difference
    num_related_courses = len(CourseExperience.query.join(CourseExperience.course).filter(Course.major == sa_position.course_section.course.major).all())
    weight += min(num_related_courses, max_related_courses_counted) * per_related_course

    return weight

def meets_requirements(student, sa_position):
    if student.cum_gpa <= sa_position.min_gpa - 0.00001: # account for float variance
        return False
    if sa_position.prior_experience:
        if CourseExperience.query.filter(CourseExperience.user == student, CourseExperience.been_sa == True).first() is None:
            return False
    if sa_position.min_grade != 'None':
        experience = CourseExperience.query.filter_by(course = sa_position.course_section.course, user = student).first()
        if not experience.has_taken:
            return False
        grade = CourseExperience.query.filter(CourseExperience.user == student, CourseExperience.course == sa_position.course_section.course).first().grade
        if not grade_equal_or_greater(grade, sa_position.min_grade):
            return False
    elif int(highest_coursenum(student, sa_position.course_section.course.major)) < int(sa_position.course_section.course.coursenum):
        return False

    return True

def grade_equal_or_greater(grade1, grade2):
    grade_value = {'A': 4, 'B': 3, 'C': 2, '?': 0}
    if grade_value[grade1] >= grade_value[grade2]:
        return True
    return False

def highest_coursenum(student, major):
    highest_course = CourseExperience.query.join(CourseExperience.course).filter(
            CourseExperience.user == student, CourseExperience.has_taken == True, Course.major == major
        ).order_by(Course.coursenum.desc()).first()
    if highest_course:
        return highest_course.course.coursenum
    return 0