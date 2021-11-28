# education_easy2
A Portal to provide online interaction between faculty and students 

FEATURES 
1.	Home page
2.	Two level Authorization System.
3.	Profile
4.	Courses and Assignments.
5.	Schedular
6.	Calendar
7.	Autograding Examination System
8.	Discussion Forum for each Course
9.	A General Networking Education Blog


HOW TO RUN THIS PROJECT

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


Website url:
https://educationeasy.herokuapp.com/

I have hosted this web application in Heroku but the uploaded pdf files can’t be opened since I have used Cloudinary free cloud service for media storage and it has a restriction of opening files others than images. However, the github repository has the all functional features including opening files. The website at above url works completely fine except the opening of files.
