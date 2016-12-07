# Synopsis

For the AB credit bank of Hong Kong which supports staff development by offering in-house courses on a range of subjects, the Staff Development Platform is a standard platform for course delivery  that will help in managing courses, maintaining course websites and distributing course materials more efficiently. Unlike the current traditional methods, the SDP will be independent of location and also accessible at any point in time within a permissible timeslot.

# Configuration

**Step 1:** Install Python and Django (please refer to API Reference section for details of installation and setup)
**Step 2:** Install apps and dependencies.
`pip install django-cors-headers`
**Step 3:** Clone/download the project and run the server on the directory where the project is located.
`python manage.py runserver`
**Step 4:** Access the system via:
SDP Login: http://localhost:8000/staff or http://localhost:8000/staff/loginPage
SDP Dashboard: http://localhost:8000/staff/home
SDP Database: http://localhost:8000/admin
Default SDP application and database account:
	Username: root
	Password: root

# API Reference

Python v3.5: https://docs.python.org/3/
Pip 9.0.1: https://pypi.python.org/pypi/pip
Django v1.10.2: https://pypi.python.org/pypi/pip
Django-cors-header: https://github.com/ottoyiu/django-cors-headers

# Specification

## 1. Major functionalities
For instructor
View, create, update, remove, and publish a course.
		[ Limitation: Course Code should not have any space(s) ]
View, create, update and remove modules of a course
View, create, update and remove components of a module
For participant
View, filter by category, and enroll in a course
View, complete or drop a course he/she is currently enrolled in
Revise or retake a completed course
For administrator
Grant permissions to users (instructor, human resources or administrator)
Add or remove a category
For human resource department
View a list of courses completed by a participant
View a list of participants who have completed a certain course

## 2. Restrictions met by the SDP
### Login
Allow registration of new users
Require new users to use a 8-character username

### Enrollment
Each participant can only enroll in one course at a time
A staff cannot enroll in a course created by him/herself
Course completion
A participant has to complete the modules in an order specified by the instructor
The course is marked as completed once all modules and components have been completed by the participant.

### Course management
Instructor cannot remove, update or add modules to a course that has already been published
Instructor cannot remove, update or reorder modules of a course that has already been published
Instructor cannot update or remove a published course.
Instructor cannot publish a course that has no component
Required categories
Required categories have been added and they cannot be removed from the system
Content type
Components must be of type text, file, image or video; file and image require upload	
Texts, images and videos will be viewed directly within the SDP; files must be downloaded

## 3. Highlighted features
Change the order of modules and components easily with drag-and-drop feature
Simple, intuitive and easy-to-use interface

# Limitations

##1. With respect to stakeholders’ needs and requirements
Currently our application allows users to autonomously register for an account, which does not comply with the security requirement of AB Credit. In the future, the registration system will be linked to AB Credit user database to verify credentials of the registering user.
Other than that, The system has implemented all the functionalities needed to meet the needs, requirements and constraints proposed by the stakeholders.

##2. With respect to the design ideas and additional features proposed by the project team
The system has not been able to deal with cases where the system or database fails, such as it has not implemented a good scheme for system recovery and data loss prevention. This can be resolved by using a different robust server than the development server provided by Django such as Amazon Web Services (AWS).
Also, the system does not take into account a browser's auto expiring cookie policy. The user has to login into the system again to continue using it. Moreover, the user has to logout off the system to exit the login session.
