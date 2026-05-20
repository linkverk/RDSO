---
title: "Pagina 6-10"
book: "FA_SQ_26_casus_V1_6_C2 1"
tags:
  - boek
  - fa-sq-26-casus-v1-6-c2-1
created: 2026-05-20
chapter: 2
total_chapters: 3
---


← [[01-pagina-1-5|Pagina 1-5]]   [[03-pagina-11-12|Pagina 11-12]] →

---

# Pagina 6-10

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
• To update their own password.
• To modify some parts of a claim (project-number and travel-distance).
• To approve or disapprove a claim
• To register on which salary-batch a claim will be settled.
• To search for and retrieve the information of a claim (check note 2 below)
• To search for and retrieve the information of a employees (check note 2 below).
• To add a new Employee to the system.
• To update an existing Employee.
• To delete an existing Employee
• To reset an existing Employee password (a temporary password).
• To update his own account.
• To delete his own account.
• To make a backup of the backend system.
• To restore a specific backup of the backend system. For this purpose, the Super
Administrator has generated a specific ‘one-use only’ code to restore a specific backup.
• To see the logs file(s) of the backend system.
4. Super Administrator
Super Administrator is simply the owner or the General Manager of CoreStaff Solutions. The
main function of the Super Administrator is to add Managers and leave the system to them;
however, they should be able to perform all possible functionalities of a Manager.
The minimum required functions of a Super Administrator are listed below:
• To modify some parts of a claim (project-number and travel-distance).
• To approve or disapprove a claim.
• To register on which salary-batch a claim will be settled.
• To search for and retrieve the information of a claim (check note 2 below)
• To search for and retrieve the information of a employees (check note 2 below).
• To add a new Employee to the system.
• To update an existing Employee.
• To delete an existing Employee
• To reset an existing Employee password (a temporary password).
• To add a new Manager to the system.
• To update an existing Manager.
• To delete an existing Manager
• To reset an existing Manager password (a temporary password).
• To make a backup of the backend system.
• To restore a backup of the backend system.
• To see the logs file(s) of the backend system.
• To allow a specific Manager to restore a specific backup. For this purpose, the Super
Administrator should be able to generate a restore-code linked to a specific backup and
Manager. The restore-code is one-use-only.
• To revoke a previously generated restore-code for a Manager.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 6

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
Please note: The credentials of the Super Administrator are hard-coded. Therefore, it is not
required that he should be able to update his own password. The Super Administrator does not
need a password change option in the user interface.
Please note: The Super Administrator should not be able to restore a specific backup on behalf of
a Manager (using a restore-code). The Super Administrator can only generate a restore-code,
but only the intended Manager is allowed to use this restore-code to perform the actual restore.
Note 1: Employees and Managers should have profiles, in addition to their usernames and passwords.
Their profiles contain only first name, last name and registration date.
Note 2: The search function must accept reasonable data fields as a search key. It must also accept
partial keys. For example, a user can search for a Claim with a ZIP-code “1218 AK” by entering any of
these keys: “1218”, “18 A”, or “AK”, etc.
Logging
The system should log all activities. All suspicious activities must be flagged, and the system needs to
produce an alert/notification for unread suspicious activities once a Manager or Super Administrator is
logged in to the system. The content of the log file(s) must be encrypted and should be only readable
through the system interface, by the Manager or Super Administrator. It means that it should not be
readable by any other tool, such as file explorer, browser or text editor.
A log should be structured similar to the following sample:
No. Date Time Username Description of activity Additional Information Suspicious
1 12-05-2021 15:51:19 john_m_05 Logged in No
2 12-05-2021 18:00:20 superadmin New admin user is created username: mike12 No
3 12-05-2021 18:05:33 … Unsuccessful login username: “mike12” is used for a login No
attempt with a wrong password
4 12-05-2021 18:07:10 … Unsuccessful login Multiple usernames and passwords are Yes
tried in a row
5 12-05-2021 18:08:02 superadmin User is deleted User “mike12” is deleted No
... ... ... ... ... ... ...
Note that the structure above is just a sample. You may choose your own desired format, but the
information given above are the minimum information needed in the log file.
The OWASP Logging Cheat Sheet could be used for further reading.
Encryption of sensitive data
As mentioned before, all sensitive data in the database, including usernames, and claim and employee
data, as well as log data must be encrypted. For this encryption, you must use a symmetric algorithm.
Additional Clarification: At any point in time, whether the application is running or not running, any user
with any text editor (outside of the application) must not be able to see any meaningful data in the
database or log file [unless they can decrypt the file(s)]. So, decryption and encryption of the files on
start and exit is not an acceptable solution.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 7

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
Passwords
Note that any form of password (encrypted or unencrypted) is not allowed to be stored in the database or
any other data file in the backend system. Instead, you must only store hash of passwords in the system.
For this purpose, you are allowed to use a third-party library.
Backup
The Manager and Super Administrator should be able to create a backup of the backend system. The
Super Administrator can restore the backend system from any backup, the Manager only from a specific
backup.
The backup must include the database (users, employees and claims information). The backup should
be in zip format. Note that the sensitive data in the DB file must already be encrypted. Thus, no
additional encryption is needed when you are creating the backup zip file. The system must support
multiple backups.
Usernames and Passwords
All Usernames and Passwords (except for the Super Administrator which is hardcoded) must follow the
rules given below:
● Username:
○ must be unique and have a length of at least 8 characters
○ must be no longer than 10 characters
○ must be started with a letter or underscores (_)
○ can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)
○ no distinction between lowercase and uppercase letters (case-insensitive)
● Password:
○ must have a length of at least 12 characters
○ must be no longer than 50 characters
○ can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%&_-
+=`|\(){}[]:;'<>,.?/
○ must have a combination of at least one lowercase letter, one uppercase letter, one digit,
and one special character
Grading
The assignment will be evaluated as either PASS or FAIL. To successfully pass the course, students
must pass the assignment together with passing the exam. Students will receive feedback from the
teachers during the presentation.
Your assignment will be assessed according to the following marking Scheme. To successfully pass the
assignment you need to meet the following assessment criteria:
● You must get C1 and C2 at least as Satisfactory (L2 or L3), and
● You must get C3 and C6 at least as Satisfactory (L1), and
● You must get C4 and C5 at least as L1, and
10
● You must get a minimum of points in total.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 8

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
Grading Table
Does the functionality of the submitted code match the assignment description? Result
Functionality of the system as described.
● If unsatisfactory, the assignment is FAIL and could not be evaluated for
(Unsatisfactory/Satisfactory)
grading.
● If satisfactory, then the table below will be used for grading.
Criteria and Points Unsatisfactory Satisfactory
Authentication and Authorization for users are properly
C1 L0 L1 L2 L3
implemented (Users access level)
C2 All inputs are properly validated. L0 L1 L2 L3
C3 The system is secured against SQL injection. L0 L1
C4 Invalid inputs are properly handled. L0 L1 L2 L3
C5 All activities are properly logged and backed up. L0 L1 L2 L3
Students can properly demonstrate and explain the
C6 L0 L1
system.
C1, C2, C4, and C5:
● L0: Not implemented / very basic attempts [0 point]
● L1: Poor implementation / Major problems [1 point]
● L2: Minimum requirements are implemented / Minor problems [2 points]
● L3: Meet the requirements / Good implementation [3 points]
C3:
● L0: Not implemented / Poor implementation / Major problems [0 point]
● L1: Minimum requirements are implemented / Minor problems [1 point]
C6:
● L0: presentation is not satisfactory [0 point]
● L1: presentation is satisfactory [1 point]
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 9

Analysis 8: Software Quality (INFSWQ01-A | INFSWQ21-A) OP4 | 2023-2024 CMI | HR
Marking Scheme
An example of criteria and marking scheme is given in the table below. Please note that not all criteria
are written in this table, but you can find all requirement and criteria in the assignment description which
are already explained in detail. This table is to give you an idea of how the assessment procedure is.
Unsatisfactory Satisfactory
Criteria
L0 (0 point) L1 (1 point) L2 (2 point) L3 (3 points)
Authentication is based on
Authentication has proper error Authentication has a secure
username and passwords.
Authenticating does not messages. Authentication data are recovery mechanism. It is
Usernames and PWs do not
exist, or it is not working stored in an encrypted file using protected against multiple
conform the given format and are
properly. proper mechanism. Passwords are wrong tries.
C1 not hashed. Application code has
Authorization is not hashed. Authorization is implemented Authorization is fully
hard-coded role checks.
implemented or at a based on user roles and is implemented based on the
Lack of centralized access
very basic level. centralized. No bugs or major user's actions, without bugs or
control logic. There are some
problems. major problems.
bugs or major problems.
Input Validation is not Input Validation is fully
Input Validation is implemented,
implemented or at a Input Validation is complete for all implemented and there are
but not for all input types, or
very trivial level. There input types and does not allow signs of following good
contains few bugs and errors.
C2 are many bugs or bypassing. Whitelisting is used for all practices in validation, such as
Input Validation can be still
errors, which let Input inputs without any flaw. There is no checking for NULL-Byte, range
bypassed. Blacklisting or mixed
Validation be bypassed bug or error. and length, Validation
mechanism is used.
easily. Functions, etc.
There are some attempts of Invalid inputs are properly handled, Invalid inputs are very well
Invalid inputs are not
invalid input handling but not without bugs or major problems. handled, and there is evidence
handled, or at very
C4 correctly implemented. The However, there might be very few of following good practices in
basic level, with many
reactions to different types of improper reactions or minor response to different types of
bugs or errors.
inputs are not suitable. improvements needed. inputs.
Logging, Backup and Logging, Backup and Restore are Logging, Backup and Restore
Logging, Backup and Restore
restore are not fully implemented. All suspicious are complete and well
C5 are partially implemented. There
implemented, or there incidents are logged. However, it formatted, and there is
are some bugs or shortcomings.
are major issues. could be still improved. evidence of good practices.
Unsatisfactory Satisfactory
Criteria
L0 (0 point) L1 (1 point)
The system is not secure (or partially) against SQL Injection. The system is fully secure against SQL Injection. Appropriate
C3 The SQL queries are not consistent throughout the code. mechanism and coding practices are used. SQL queries and codes
There are coding bugs or issues. are consistent in the final product.
Students cannot properly run and demonstrate the system, Students can properly run and demonstrate the system and provide
or cannot explain it, or answer the technical questions. relevant answers to the majority of the technical questions.
C6
There is no evidence of original work or satisfactory The work is evidently original, and there is evidence of sufficient
contribution by the student. contribution by the student.
FINAL ASSIGNMENT: Urban Mobility Backend System PAGE 10

---
← [[01-pagina-1-5|Pagina 1-5]]   [[03-pagina-11-12|Pagina 11-12]] →