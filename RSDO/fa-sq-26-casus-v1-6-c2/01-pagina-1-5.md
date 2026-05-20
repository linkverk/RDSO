---
title: "Pagina 1-5"
book: "FA_SQ_26_casus_V1_6_C2"
tags:
  - boek
  - fa-sq-26-casus-v1-6-c2
created: 2026-05-20
chapter: 1
total_chapters: 3
---


[[02-pagina-6-10|Pagina 6-10]] →

---

# Pagina 1-5

You may need to refresh the page multiple times if all pages are not properly displayed
Final Assignment (Version 1.6)
ANALYSIS 8: SOFTWARE QUALITY
(INFSWQ01-A | INFSWQ21-A)
Resit Assignment [2026]
DECLARATIEAPP backend system
To ensure that this assessment is feasible within the scope of the course, the following scenario has
been designed to verify that students have achieved at least the minimum level of the intended
learning outcomes, as defined in the course manual. Please note that this scenario may differ from
real-world situations, which typically involve additional quality requirements. In practice, such a
system would include many more requirements and components; however, for the purposes of this
assessment, you should focus solely on the description provided.
Learning Objectives
The learning objectives of the assignment and mapping to the intended learning outcome of the
course are listed below:
1. To understand the common mistakes of coders in input validation and communications with
subsystems (LO2, LO3).
2. To apply the knowledge of input validation, SQL injection, and cryptography (LO1, LO4).
3. To partially build a secure system against various attacks initiated by user input (LO4).
Assignment
Introduction
Your company CoreStaff Solutions operates an internal DeclaratieApp that allows employees to
submit expense claims for travel kilometers and home office days. Managers can approve or reject
these claims. In this assignment, you will design and implement a secure backend system that
handles:
• User authentication
• Claim registration and approval workflow
• Employee and manager profiles
• Logging and monitoring of activities
PAGE 1 of 12

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
The focus of this assignment is software security. Your system must follow best practices in:
• Input validation
• Encryption
• Logging
• Secure role-based access
• Separation of concerns (e.g. distinct layers for User Interface, Validation, Authorization, Data
storage, etc.).
You will implement a console-based interface in Python 3 for this backend system. The system
should use SQLite3 as the local database.
Overview of the User Roles
Users of the backend system are the employees of CoreStaff Solutions. In the system there are three
User Roles, which are categorized in Table 1 User Roles.
User role Created by Remark
Super Hard-coded A Super Administrator has full control of the system.
Administrator In practice, their main role is to create and manage
Manager accounts.
Manager Super Administrator A Manager approves or rejects claims. Can view
employee profiles.
Employee Super Administrator or Manager An Employee submits claims for travel or home office
days.
Table 1 User Roles
The Super Administrator account is Hard-coded
For assessment purposes, the backend system must include a hard-coded Super Administrator
account with a fixed username and password.
The fixed username must be: super_admin
The fixed password must be: Admin_123?
This approach is intentionally insecure and would not be acceptable in a real-world application.
However, it simplifies access for instructors during the assessment process.
Note: The customers of CoreStaff Solutions are not users of the backend system. The users of
the backend system and their corresponding Use Cases can be found in the following pages.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 2

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
The data stored in the backend system
Employee data
When a new employee joins the company, their information should be entered into the backend
system. A new employee can be registered in the backend system by a Super Administrator and by
the Manager. The backend system then needs to automatically add the registration date and assign
a unique employee ID to every new employee. The registration date is the current time at the
moment of entering the employee data.
See Table 2 for the employee data that should be entered into the backend system. For some
employee data attributes specific syntax rules are defined in the column ‘Format’. The letter D means
a digit (0-9), the letter X means an uppercase letter (A-Z).
Traveller data attribute Description Format
First Name The employee’s given name.
Last Name The employee’s family name or
surname.
Birthday The employee’s date of birth, used for
identity verification.
Gender The employee’s gender, male or female.
Street name The name of the street where the
employee lives.
House Number The number of the employee’s residence
on the street.
Zip Code The postal code corresponding to the DDDDXX
traveller’s address.
City The city where the employee resides. The system should generate a list
of 10 predefined city names of
your choice.
Email Address The employee’s email address, used for
communication and account
management.
Mobile Phone The employee’s mobile phone number, +31-6-DDDDDDDD
used for account verification and
notifications. Only DDDDDDDD to be entered
by the user.
Identity Document Type The Identity document type (Passport /
ID-Card).
Identity Document The unique number of the employee’s XXDDDDDDD or XDDDDDDDD
number identity documents.
BSN number A unique identifier used for Tax and Nine digits.
Social Security purposes. DDDDDDDDD
Table 2 Employee Data
Claim data
The backend system stores information about the travel and home office days claims. An employee
can add new claims. An employee can also modify and delete existing ones as long as the Claim is
not yet processed in a salary-batch. The Manager can mark a Claim as approved or not approved. If
a Manager marks a Claim as approved, he will also enter the corresponding salary-batch
identification.
See Table 3 for the Claim data that should be entered into the backend system. For some data
attributes specific syntax rules are defined in the column ‘Description.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 3

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
Claim data Only enter Description Attribute can be edited by
attribute data if …
Super Employee
Administrator &
Manager
Claim Date The date of this claim. A date older then 2 months in the past or a
date 14 days in the future is not allowed. This is relative to the
current system date.
Format:
ISO 8601 format: YYYY-MM-DD
Project-number The project number corresponding to this claim.
Format:
2 to 10 digits characters.
Employee-ID The ID of the employee. This should be set by the application
itself based upon the currently logged in Employee.
Format:
2 to 10 digits characters.
Claim type Either ‘Travel’ or ‘Home Office’. If chosen for ‘Travel‘ the
Employee must also enter data for the attributes which are
marked as ‘Claim type is Travel’ in column ‘Only enter data if ….’,
otherwise not. If chosen for ‘Home Office’ no additional
information is required.
Travel distance ‘Claim type’ is The number of kilometers travelled.
in km’s ‘Travel’
Format:
Digits
From ZIP-code ‘Claim type’ is The ZIP code from where the travel started.
‘Travel’
Format:
DDDDXX
From house- ‘Claim type’ is The house number from where the travel started.
number ‘Travel’
Format:
Only digits.
To ZIP-code ‘Claim type’ is The ZIP code of the destination from the travel.
‘Travel’
Format:
DDDDXX
To house- ‘Claim type’ is The house number of the destination from the travel.
number ‘Travel’
Format:
Only digits.
Approved The approval status of this claim (Pending/Approved/Rejected).
Approved by The manager-ID who approved or rejected this claim. This should
be set by the application itself, based upon the currently logged in
Manager.
Salary-batch The salary batch on which this Claim will be settled. This is the
identification year and month as digits. For example: ‘2026-07’
Format:
YYYY-MM
Table 3 Claim data
The column ‘Attribute can be edited by’ in Table 3 indicates which attribute can be edited by which
user role. When there is a checkmark in the appropriate cell it indicates that the corresponding
attribute can be edited by the corresponding user role. If there is no checkmark then the
corresponding attribute cannot be edited the corresponding user role. For instance, the attribute
‘Approved’ can only be edited by the Super Administrator and the Manager, not by the Employee.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 4

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
User Interface
The backend system must have a user-friendly interface (easy, efficient, and enjoyable) that allows
users (Super Administrator, Managers, and Employees) to perform their functions easily and smoothly.
A console-based interface is the sufficient requirement; however, a graphical user interface (GUI) is
optional and allowed, but not necessary, provided that it also meets the usability expectations.
Ensure that your user interface provides sufficient information for the user to work with it. For example, if
you have a menu “1. Add new claim” which should be chosen by pressing ‘A’ or ‘a’ or entering ‘1’, this
should be clearly displayed to the user on the menus screen. Do not suppose that the user (and your
teacher when testing and grading your assignment) should guess how to work with the user interface.
Note that the user interface would not be graded for flexibility or efficiency of use, but if your teachers
cannot properly work with the system, it might not be possible for them to correctly assess your work.
Data (DB) File
The main functionality of the backend system is to store and manage the information of employees and
claims in the system. In addition, the system needs to store information of the users of the backend
system. For this purpose, you need to implement the database using SQLite library in Python “sqlite3”.
Note that the sensitive data, including usernames, employees’ data and claims data must be encrypted
in the database. Passwords must be handled and stored in accordance with the security practices
covered in the course.
Stakeholders, Users, Authorization, Functions and Accessibility Levels
More details about the stakeholders of the system are explained below:
1. Customers of CoreStaff Solutions
Customers of CoreStaff Solutions are not the users of the concerned backend system and
have no role or interaction with this part of the application. The only (indirect) relationship
between these customers and the backend system is that the travel information of the employees
to the locations of these customers is registered and stored in the backend system.
2. Employees
Employees of CoreStaff Solutions are involved in projects of the customers of CoreStaff
Solutions. Hence, they need to be able to claim their travel expenses or declare a fixed fee when
they work from home. So, the minimum required functions of an Employee in the system are
summarized as below:
• To update their own password
• To add new claims
• To update their own existing claims as long as the claim is not linked to a salary-batch
• To search for and retrieve the information of their own existing claims
3. Manager
A Manager is a person who is responsible for a group of employees. They must be able to
approve or disapprove claims of Employees and register on which salary-batch a claim is settled.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 5

---
[[02-pagina-6-10|Pagina 6-10]] →