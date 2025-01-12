# Software Requirements and Use Cases

## SA Connect: "Streamlining the Student Assistant Recruitment Process"
--------
Prepared by:

* `Harleen Kaur`,`BME & RBE>`
* `Julian Kreis`,`CS`
* `Jed Geoghegan`,`CS & DS`
* `Jacob Lu`,`IMGD & CS`

---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-07 |Initial draft | 1.0        |
|      |      |         |         |
|      |      |         |         |


----
# 1. Introduction

To provide a user friendly interface for students and faculty to find and promote SA job vacancies for the upcoming year autonomously. 
Students will enter contact information and course preferences which will automatically enter them for job listings and intructors can choose from a 
generated list of applicants who are interested in their course. 


----
# 2. Requirements Specification

In the student section:
1. Allow students to create a student account and enter their profile information, containing:
  a. A username (that is their WPI email) and a password
  b. Their contact information (first name, last name, WPI ID, email, phone)
  c. Other account information (major, cumulative GPA, expected graduation date)
  d. The courses that they have been an SA for before
2. Students should be able to login through two methods:
  a. Using their WPI email and password. 
  b. Using the WPI SSO service.
3. Students can view open SA positions. In addition to seeing a list of all open SA positions, there will be a seperate "Recommended SA Positions" section to display recommended positions in ranked order based on specified criteria. Positions under this tab should be sorted based on how many conditions in this criteria the student has met. The criteria is open-ended, but must include: 
  a. If the student already served as an SA for the course
  b. If the student took the course and received A
4. Each SA position should have this information displayed
  a. course number, section, and title (e.g., 'CS3733-02 Software Engineering')
  b. term (e.g. '2024B')
  c. instructor's name and contact information
  d. qualifications needed for the SA position
5. Applying for positions: Students can apply to multiple SA positions. For each application, a student must enter
  a. The grade they earned when they took the course
  b. The year and term they took the course
  c. The year and term they are applying for SAship
6. View the SA positions they have already applied to and check the statuses of their application
  a. When submitted, the status will appear as "Pending"
  b. When an instructor accepts their application, the status will change to "Assigned".
7. Withdraw applications that have the status of "pending"

In the faculty section:
1. Allow faculty to create an instructor account and enter their profile information, containing:
  a. A username (that is their WPI email) and a password
  b. Their contact information (first name, last name, WPI ID, email, phone)
2. Faculty should be able to login through two methods. Incorrect login data is not accepted.
  a. Using their WPI email and password. 
  b. Using the WPI SSO service.
3. Instructors should be able to create the new course sections that they will be teaching
  a. Each course offering will contain a course number, section, and term. At least one of those datapoints should differ from those each other course offering, allowing the course section to be uniquely identified
  b. The SA positions will be associated with these course offerings
4. Faculty should be able to create SA positions for each course offering they have made. When creating the position, they should be able to choose
  a. Choose the course section for SAship from among the sections they have created
  b. Enter the number of SAs needed for the course section
  c. Enter the qualifications needed for the SAship such is min GPA, min grade in course, or prior SA experience
5. Faculty should be able to see the list of students that applied to each of their sections and if the applicants have already been assigned to a different course
6. Additionally, faculty hsould be able to see the qualifications of each student such as GPA, earned grade in the class, and previous courses they've been SA in
7. The instructor of the course should be able to select applicant that has not already been assigned a position to an SAship position they have created
8. One student can be assigned to a single SA position
9. There can be multiple SAs in a single course, but no more than the maximum number of SAs set by the instructor

----
## 2.1 Customer, Users, and Stakeholders

Customer: 
- WPI Computer Science Department

Users: 
- Student Users: Undergraduate Students interested in applying for SA positions
- Faculty Users: Faculty in the CS Department responsible for teaching undergrad courses 

Stakeholders:
- WPI Computer Science Department
a. Students: Those who want to apply to be SA's will create accounts, apply, and interact with system by viewing their applications
b. Faculty: Will use the platform to create and manage SA positions for their courses
c. Students(General body): While they are not directly interaacting with the system unless applying for a SA position,  
   the system is designed to improve their experience 
d. Admin Users: responsible for maintaining the web application, ensuring it runs smoothly

----
## 2.2 User Stories

1. As a student, I want to create an account using my WPI credentials so that I can log in an apply for SA positions.  
2. As a student, I want to login with username and password provided during create account
3. As a student, I want to view all SA positions so that I can choose positions of interest.  
4. As a student, I want to view a list of recommended positions so that I can find relevant opportunities.  
5. As a student, I want to view a detailed description of a position so that I can understand the requirements for each course.  
6. As a student, I want to apply to SA positions so that I can get a job.  
7. As a student, I want to view the status of my applications so that I can track my SA application progress. 
8. As a student, I want to withdraw my application for a SA position so that I can change my decision to be a SA.  
9. As a student, I want to have "assigned" SA positions be disabled for withdrawal so I can't withdraw from "assigned" positions.
10. As a student, I want to edit my profile so that I can change my personal information 
11. As faculty, I want to create an account using my WPI credentials so that I can log in and hire students. 
12. As faculty, I want to login with username and password provided during create account
13. As faculty, I want to add courses with open SA positions so that I can add positions.  
14. As faculty, I want to add open SA positions for my courses so that I can begin the hiring process.  
15. As faculty, I want to view student applications so that I can review qualifications and hire applicants.  
16. As faculty, I want to assign SA positions based on student applications and qualifications, ensuring each student is only assigned to a single position. 
17. As faculty, after interviewing a student, I would like to update the status of their application from “Pending” to "Assigned" so that I can hire them for the position. 
18. As a faculty, I want to edit my profile so that I can change my personal information

----
## 2.3 Use Cases

Actors Involved:
- Student: A student interested in applying for Student Assistant (SA) positions within the Computer Science Department. 
           The student can create an account, log in, view open SA positions, view recommended SA positions, apply for SA positions, 
           track application statuses, and withdraw applications if needed.

- Faculty: A faculty member in the Computer Science Department responsible for managing Student Assistant (SA) positions for their courses. 
           The faculty member can create an account, log in, add course sections, create SA positions, review student applicants,
           view student qualifications, and assign students to open SA positions.

- Administrator: The system administrators are responsible for overseeing the web application. 
                 The administrator manages user accounts (both students and faculty), monitors system activity, resolves issues, and ensures that 
                 the system runs efficiently. The administrator has control over user permissions and can make necessary adjustments to the system.

- System: The web application platform that manages student and instructor accounts, stores and displays available SA positions, 
          handles the application process, and updates application statuses. The system interacts with students to retrieve, display, and 
          manage data related to SA recruitment.


| Use case # 1      |   |
| ------------------ |--|
| Name              | Student Account Creation  |
| Participating actor  | student  |
| Entry condition(s)     | The student has not created an account yet |
| Exit condition(s)           | The Student account is created  |
| Flow of events | 1. The student navigates to account registration page
                   2. The system displays the registration form
                   3. The student enters their WPI information, password, and contact details
                   4. The system validates the provided information, stores the account details, and confirms the account creation and notifies the student
                   5. The student confirms account creation
                   6. The system stores the account details and sends a confirmation message to the student of the creation of the account |
| Alternative flow of events    | - If the email is already registered, the system notifies the student, who may try again or exit.
                                  - If the password is too weak, the system prompts the student to enter a stronger password.  |
| Iteration #         | Sprint 1  |


| Use case # 2      |   |
| ------------------ |--|
| Name              | Student Login  |
| Participating actor  | student  |
| Entry condition(s)     | The student has an existing account |
| Exit condition(s)           | The student is logged into their account  |
| Flow of events | 1. The student navigates to the login page.
                   2. The system displays the login form.
                   3. The student enters their WPI email and password and submits the form.
                   4. The system validates the login credentials notifies the student if login is successful and redirects them to their dashboard.  |
| Alternative flow of events    | - If the credentials are incorrect, the system notifies the student, who may retry or reset their password  |
| Iteration #         | Sprint 1  |


| Use case # 3      |   |
| ------------------ |--|
| Name              | Viewing open SA Positions  |
| Participating actor  | Student  |
| Entry condition(s)     | The student is logged in and navigates to the SA positions page  |
| Exit condition(s)           | The system displays a list of open SA positions to the student  |
| Flow of events | 1. The student navigates to the SA positions page.
                   2. The system fetches the list of open SA positions and displays the list to the student, including recommendations based on qualifications. |
| Alternative flow of events    | - If no SA positions are available, the system displays a message indicating that no positions are currently open  |
| Iteration #         | Sprint 2  |


| Use case # 4      |   |
| ------------------ |--|
| Name              | Viewing Detailed Description of a SA Position  |
| Participating actor  | Student  |
| Entry condition(s)     |The student is logged in and has navigated to the SA positions list  |
| Exit condition(s)           | The system displays the detailed description of a selected SA position, including the course title, section, term, instructor contact information, and required qualifications  |
| Flow of events | 1. The student views the list of available SA positions and selects a specific SA position from the list.
                   2. The system retrieves and displays the detailed description of the selected SA position, including course number, section, title, term, instructor’s contact information, and required qualifications |
| Alternative flow of events    | - If the system is unable to retrieve details for the selected position (e.g., data not available), the system displays an error message indicating that the details are unavailable  |
| Iteration #         | Sprint 2  |


| Use case # 5     |   |
| ------------------ |--|
| Name              | Apply for SA position  |
| Participating actor  | Student  |
| Entry condition(s)     | The student is logged in and viewing an open SA position  |
| Exit condition(s)           | The application is submitted, and the status is set to "Pending."  |
| Flow of events | 1. The student selects an SA position to apply for.
                   2. The system displays an application form for the position.
                   3. The student enters the necessary details (school year, term completed).
                   4. The system validates the application information and prompts for confirmation upon validation.
                   5. The student confirms
                   6. The system submits the application as "Pending." |
| Alternative flow of events    | - If required information is missing, the system prompts the student to fill in missing details.
                                  - If the student has already applied for the position, the system notifies them of the duplicate application. |
| Iteration #         | Sprint 2  |


| Use case # 6     |   |
| ------------------ |--|
| Name              | View Application Status  |
| Participating actor  | Student  |
| Entry condition(s)     | The student is logged in and has applied for at least one SA position |
| Exit condition(s)           | The student can view the status of each application (Pending, Assigned, or Withdrawn)  |
| Flow of events | 1. The student navigates to the "My Applications" page
                   2. The system retrieves the list of applications and their statuses
                   3. The student clicks on a specific application 
                   4. The system shows the student's application status |
| Alternative flow of events    |  If no applications exist, the system displays a message indicating no applications found  |
| Iteration #         | Sprint 2  |


| Use case # 7     |   |
| ------------------ |--|
| Name              | Withdraw Application  |
| Participating actor  | Student  |
| Entry condition(s)     | The student has an application in "Pending" status and is logged in |
| Exit condition(s)           | The selected application is withdrawn, and the status changes to "Withdrawn."  |
| Flow of events | 1. The student navigates to "My Applications" and selects a pending application to withdraw.
                   2. The system displays a confirmation prompt for withdrawal
                   3. The student confirms the withdrawal
                   4. The system changes the application status to "Withdrawn" and updates the application list view |
| Alternative flow of events    |  - If the application status is not "Pending," the system prevents withdrawal and notifies the student.
                                   - If the student cancels, the application status remains unchanged.  |
| Iteration #         | Sprint 3  |


| Use case # 8      |   |
| ------------------ |--|
| Name              | Faculty Account Creation  |
| Participating actor  | Faculty  |
| Entry condition(s)     | The faculty member has not created an account yet |
| Exit condition(s)           | The faculty account is created  |
| Flow of events | 1. The user navigates to account registration page
                   2. The system displays the registration form
                   3. The user enters their WPI information, password, and contact details
                   4. The system validates the provided information, stores the account details, and confirms the account creation and notifies the user
                   5. The user confirms account creation
                   6. The system stores the account details and sends a confirmation message to the user of the creation of the account |
| Alternative flow of events    | - If the email is already registered, the system notifies the user, who may try again or exit.
                                  - If the password is too weak, the system prompts the user to enter a stronger password.  |
| Iteration #         | Sprint 1  |


| Use case # 9      |   |
| ------------------ |--|
| Name              | Faculty Login  |
| Participating actor  | Faculty  |
| Entry condition(s)     | The faculty user has an existing account |
| Exit condition(s)           | The faculty user is logged into their account  |
| Flow of events | 1. The user navigates to the login page.
                   2. The system displays the login form.
                   3. The user enters their WPI email and password and submits the form.
                   4. The system validates the login credentials.
                   5. The system notifies the user if login is successful and redirects them to their dashboard.  |
| Alternative flow of events    | - If the credentials are incorrect, the system notifies the user, who may retry or reset their password  |
| Iteration #         | Sprint 1  |


| Use case # 10     |   |
| ------------------ |--|
| Name              |  Add course with SA positions |
| Participating actor  | Faculty  |
| Entry condition(s)     | The faculty user has logged in and selected to add a course  |
| Exit condition(s)           | A new course is created and associated with the faculty user, and positions can be added to the course. |
| Flow of events | 1. The user navigates to "manage courses" and selects the option to add a
                   new course section 
                   2. System displays a form with a drop down menu of a list of availible courses.
                   3. The faculty user selects a course from the drop down menu and enters the section number and term
                   4. the user submits the form
                   5. The system validates the information, and ensures that the course section is unique and saves the new course section under the user's profile.  |
| Alternative flow of events    | - if the course section already exists for the term,
                                    system will alert user and promt an adjusted entry of the form
                                  - if faculty cancels, no course is added and user is
                                    returned to manage courses page
 |
| Iteration #         | Sprint 1  |

| Use case # 11     |   |
| ------------------ |--|
| Name              |  Add Open SA positions to Course |
| Participating actor  | Faculty  |
| Entry condition(s)     | The faculty user has logged in and has previously added a course  |
| Exit condition(s)           | A new position is created and associated with the selected course section, and is visible to students on SA positions page. |
| Flow of events | 1. The user navigates to "manage courses" and selects an existing course 
                   2. The user selects option to add SA position
                   3. System displays a form to specify number of SAs needed and required qualifications
                   4. The user fills the form and submits
                   5. The system validates the informtion, and saves the SA position information, linking it to the course section.  |
| Alternative flow of events    | - if course section has reached max SA positions system
                                    will display error message 
                                  -  if user cancels no positions will be added and user will be returned to course section page. |
| Iteration #         | Sprint 1  |


| Use case # 12     |   |
| ------------------ |--|
| Name              |  View Student Applications |
| Participating actor  | Faculty  |
| Entry condition(s)     | The faculty user is logged in and has created open SA positions
                           for one or more course sections  |
| Exit condition(s)           | The faculty user views the list of student applications for one or more SA positions. |
| Flow of events | 1. user navigates to "manage SA application" page
                   2. system displays a list of all SA positions that were created by the user  
                   3. user selects a course section to view 
                   4. System displays a table with all the student applications and profile information 
                   5. The faculty reviews the qualifications of each applicant   |
| Alternative flow of events    | - if there are no applications for a position system will
                                   display a message to inform user
                                  - if user exits page they will be redirected to dashboard |
| Iteration #         | Sprint 2  |


| Use case # 13     |   |
| ------------------ |--|
| Name              |  Assign SA Position to Student |
| Participating actor  | Faculty  |
| Entry condition(s)     | The faculty user has logged in and has reviewed student
                           applications, and has determined the students eligible for assignment.  |
| Exit condition(s)           | The selected student is assigned to the SA position, and the system updates the student's application status to "Assigned." |
| Flow of events | 1. The user navigates to "manage SA applications" and selects student
                     application
                   2. system displays the student's details and assignment options
                   3. user selects the option to assign the student to the SA postion
                   4. system verifies student hasn't been assigned to another position
                   5. system updates application status to "Assigned" and sends a     notification to the student.    |
| Alternative flow of events    | - if student is already assigned to another position
                                    system will send an error message and notifies user
                                  -  if user cancels no changes are made to the student's application status 
 |
| Iteration #         | Sprint 3  |



----
# 3. User Interface

UI Pages needed:

Staff:
Main page shows courses they've created, can open dropdown under each course that shows applicants and applicant info. Each course also has an edit button to go to an edit course form
Create course page
Edit course form

Student:
Main page shows courses they can apply to, including a separate relevant courses section
Separate page to view application status

Both:   
Login Page
Profile creation page
Edit Profile (Student will need more info)

  <kbd>
      <img src="images/FigmaMockup.png"  border="2">
  </kbd>
  
----
# 4. Product Backlog

Here you should include a link to your GitHub repo issues page, i.e., your product backlog. Make sure to create an issue for each user story.  
https://github.com/WPI-CS3733-2024B/termproject-gitgurus/issues 

----
# 5. References

CS 3733 Instructor(s). "CS 3733 – 2024 B Term Project PDF". 11/6/2024
