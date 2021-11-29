# Microsoft Engage Mentorship program'21 project
# education_easy2
A Portal to provide online interaction between faculty and students.

This is a project under Microsoft Engage mentorship program '21 by Preethi Paripally

# Problem Statement:
Build a functional prototype of a platform that gives students an array of digital academic and social tools to stay engaged with their studies, peers, and broader university community during pandemic.

# HOW TO RUN THIS PROJECT

Install Python(3.7.6) (Dont Forget to Tick Add to Path while installing Python)
Open Terminal and Execute Following Commands :

python -m pip install -r requirements. txt

Download This Project Zip Folder and Extract it /clone the project
Move to project folder in Terminal. Then run following Commands :

py manage.py makemigrations
py manage.py migrate
py manage.py runserver

Now enter following URL in Your Browser Installed On Your Pc

http://127.0.0.1:8000/


# Website url:
https://educationeasy.herokuapp.com/

I have hosted this web application in Heroku but the uploaded pdf files can’t be opened since I have used Cloudinary free cloud service for media storage and it has a restriction of opening files others than images. However, the github repository has the all functional features including opening files. The website at above url works completely fine except the opening of files.


# FEATURES 

1.  Home Page
2.	Two level Authorization System.
3.	Profile
4.	Courses and Assignments.
5.	Schedular
6.	Calendar
7.	Autograding Examination System
8.	Discussion Forum for each Course
9.	A General Networking Education Blog



## Home page
![Screenshot (966)](https://user-images.githubusercontent.com/77268350/143836634-ac88bf72-cd82-4e36-bc02-647b7f48b63d.png)
## Register page
![Screenshot (967)](https://user-images.githubusercontent.com/77268350/143836653-df966036-0023-4e69-8a23-f9c37e235444.png)
## login page
![Screenshot (968)](https://user-images.githubusercontent.com/77268350/143836661-46e7dcd0-4a29-4df0-85e7-1cdba9c8d8ca.png)




# Faculty View
## All Courses
![Screenshot (969)](https://user-images.githubusercontent.com/77268350/143836667-d61a9ea1-4ce1-4998-b7c1-87cbbc8f9d19.png)
## Courses creted by Faculty
![Screenshot (970)](https://user-images.githubusercontent.com/77268350/143836674-805c544d-4307-4e2b-b4b7-a7b0138dc591.png)
## Course detail
![Screenshot (971)](https://user-images.githubusercontent.com/77268350/143836681-df1ec034-66eb-4e1b-8d1f-4fa7b562ceef.png)



## Schedules
![Screenshot (972)](https://user-images.githubusercontent.com/77268350/143836687-f2704328-d8da-4564-889b-b013cae7a816.png)
## View Bookings
![Screenshot (973)](https://user-images.githubusercontent.com/77268350/143836697-bce51242-b3ac-4437-8f4a-2e722cb0aa49.png)
## Add Schedule
![Screenshot (974)](https://user-images.githubusercontent.com/77268350/143836704-6728204d-af68-46f9-bc58-ddd1dc51b838.png)
## Clashing schedule list
![Screenshot (975)](https://user-images.githubusercontent.com/77268350/143836713-5e8c2a28-192b-434c-9d21-ac317f374d09.png)



## View Assignment Submissions
![Screenshot (977)](https://user-images.githubusercontent.com/77268350/143836727-0139acf6-4db0-44db-a39d-d3e42e344662.png)


## Resources
![Screenshot (978)](https://user-images.githubusercontent.com/77268350/143836745-f610443b-7f47-42f5-bc8e-23c608353f6b.png)


## Exams
![Screenshot (979)](https://user-images.githubusercontent.com/77268350/143836756-b554ea9a-597d-437b-bf51-91f42f9aef74.png)
## View Exam
![Screenshot (980)](https://user-images.githubusercontent.com/77268350/143836765-6c1bc7a5-6ccd-40c2-8771-64c8748079b2.png)


## All Posts
![Screenshot (982)](https://user-images.githubusercontent.com/77268350/143836780-454b0a74-f1c0-48a8-a9d5-0b69050c9a87.png)
## My Posts
![Screenshot (983)](https://user-images.githubusercontent.com/77268350/143836789-553fbf84-a227-4d5f-88ed-4bfa2dfb03c2.png)

## Post detail
![Screenshot (981)](https://user-images.githubusercontent.com/77268350/143836773-accf1fbe-23c4-4aa5-8fa5-1364c7fcc04b.png)



## My Schedule list
![Screenshot (984)](https://user-images.githubusercontent.com/77268350/143836795-896961ed-cd69-480b-88be-e6a447315d8d.png)
## Calendar
![Screenshot (985)](https://user-images.githubusercontent.com/77268350/143836814-012ae2d0-a799-42f4-8442-484bca568009.png)



## All Students
![Screenshot (986)](https://user-images.githubusercontent.com/77268350/143836826-b1546e96-a1c6-404e-b7de-8d684636aea9.png)
## All Faculty
![Screenshot (987)](https://user-images.githubusercontent.com/77268350/143836831-ee2fb258-d972-490c-ab6a-5b025f81030a.png)





# Student View


## Unregistered Course view
![Screenshot (988)](https://user-images.githubusercontent.com/77268350/143836841-a121d771-6ecd-4cfd-aa1a-c37070070b50.png)
## registered Course view
![Screenshot (989)](https://user-images.githubusercontent.com/77268350/143836855-acd0e352-dd05-4961-892c-ae8ef42d9ddd.png)



## Schedule view
![Screenshot (990)](https://user-images.githubusercontent.com/77268350/143836865-42f8180e-1195-456b-a801-dbce6fd34f27.png)
## Booking Scehdule
![Screenshot (991)](https://user-images.githubusercontent.com/77268350/143836873-88128504-b27b-47f9-807c-cdbefed03688.png)
## Not eligible
![Screenshot (992)](https://user-images.githubusercontent.com/77268350/143836927-6b060b53-c891-41b6-84e0-501e1d2abfd8.png)
## is eligible
![Screenshot (993)](https://user-images.githubusercontent.com/77268350/143836880-53f5e535-851a-4fa8-a38d-472cd7d98f43.png)
## seating arrangement
![Screenshot (994)](https://user-images.githubusercontent.com/77268350/143836891-44d0fe7b-56e4-4bf4-bb53-0a3fa542bd1d.png)
## select seat
![Screenshot (995)](https://user-images.githubusercontent.com/77268350/143839818-821c3ac9-303d-4c91-ba8f-25f614ecca91.png)
## confirm booking
![Screenshot (996)](https://user-images.githubusercontent.com/77268350/143839812-239e687b-2fcf-4a1c-b4ab-4b39aff38c15.png)
## after booking the seat
![Screenshot (997)](https://user-images.githubusercontent.com/77268350/143839851-7de877d7-d122-4f39-9cdf-3820841823e7.png)



## View booking history
![Screenshot (1004)](https://user-images.githubusercontent.com/77268350/143839950-fcc05423-b375-4579-8654-4a7c5058adab.png)

## TO Download Slot Deatils
![Screenshot (1005)](https://user-images.githubusercontent.com/77268350/143839959-e220fe9b-ebe1-4677-b437-4f2b4c9fe1ae.png)

## Download Slot Deatils
![Screenshot (1006)](https://user-images.githubusercontent.com/77268350/143839968-554b334c-2da4-4966-ad1b-a4bff8364176.png)

## Calendar showing bookings
![Screenshot (1007)](https://user-images.githubusercontent.com/77268350/143839976-47fbb43b-96eb-4685-9610-6eeb08abb1ac.png)




## Exams
![Screenshot (998)](https://user-images.githubusercontent.com/77268350/143839890-a5e4477c-f3d8-4119-a1b4-f986099ff9a7.png)

## Take exam
![Screenshot (1001)](https://user-images.githubusercontent.com/77268350/143839925-e3a2df85-d26e-4284-882f-2a7adb3bdce3.png)

## Entering into examination
![Screenshot (1002)](https://user-images.githubusercontent.com/77268350/143839931-e9e2f87d-1b23-4462-8754-010d96c8665d.png)

## submit exam
![Screenshot (1003)](https://user-images.githubusercontent.com/77268350/143839942-991135c0-aeb8-4852-a05d-9fbad8a9ebae.png)

## results of exam
![Screenshot (1000)](https://user-images.githubusercontent.com/77268350/143839912-ae610d9d-81a8-422c-9cfe-6800fc0c8b44.png)

## After attempting exam for once
![Screenshot (999)](https://user-images.githubusercontent.com/77268350/143839895-2996adcc-061c-487c-b04e-6dfe36f3a9fe.png)




## Assignments
![Screenshot (1009)](https://user-images.githubusercontent.com/77268350/143839991-ba2159e3-2c91-4547-8b1d-900cad7c5fcd.png)

## View Assignment before assignment submission
![Screenshot (1008)](https://user-images.githubusercontent.com/77268350/143839984-5c8a793e-8d92-4506-9524-b663d84b7bff.png)


## View Assignment after assignment submission
![Screenshot (1010)](https://user-images.githubusercontent.com/77268350/143840000-fd81a174-1de9-4263-8121-09f54ae8d704.png)

## View assignment submission
![Screenshot (1011)](https://user-images.githubusercontent.com/77268350/143840007-76864528-3ace-4abd-a11a-13a117f5ab45.png)


## View Resources
![Screenshot (1012)](https://user-images.githubusercontent.com/77268350/143840045-1723fdd9-e792-4379-ae38-4a6f8dea8a05.png)


## View Course Discussions
![Screenshot (1013)](https://user-images.githubusercontent.com/77268350/143840056-bc895948-7bf1-4f67-b851-764c4b7e7671.png)

## Search query
![Screenshot (1014)](https://user-images.githubusercontent.com/77268350/143840064-74f11481-4904-453e-ad6e-ab082ea48fc1.png)


## Student Navbar
![Screenshot (1015)](https://user-images.githubusercontent.com/77268350/143840076-5c66ab42-4519-4d10-aaa9-a2d62b046ca5.png)



