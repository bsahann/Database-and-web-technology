import flask 
from flask import render_template, redirect , url_for ,request,session
from flask_restful import Resource, Api
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json
import random
DB = "Database.db"

conn = sqlite3.connect(DB)

# Create our app
app = flask.Flask(__name__)
app.secret_key="secret"
# Create an API for our app
api = Api(app)

@app.route("/login", methods = ["POST","GET"])
def home():
    #Reset session
    session.pop("ID",None)
    session.pop("userID",None)
    session.pop("teacherID",None)
    session.pop("adminID",None)
    session.pop("teacherName",None)
    session.pop("userName",None)
    session.pop("adminName",None)
    #Preparation of data for login
    conn = sqlite3.connect(DB)
    d1 = conn.execute("SELECT * FROM Teacher ")
    d2 = conn.execute("SELECT * FROM User ")
    d3 = conn.execute("SELECT * FROM Admin ")

    teacherid = {}
    userid = {}
    adminid = {}    
    
    
    
    if request.method == "POST":#When button is pressed
        try:
            #Get input data
            who = request.form["who"]    
            ID = request.form["username"]
            password = request.form["password"]
            #
            if(who == "Teacher"):#Check if teacher logs in

                x=0
                for row in d1:#Further preparation of data for password inspection and passing data
                    teacherid[x] = {"TeacherID":row[0],"Password":row[1],"FirstName":row[2],"LastName":row[3]}
                    x +=1 

                if ID.isdigit():#Check if entered data is digit
                    ID = int(ID)
                    if ID-1 in teacherid:#Because of ID starting from 1 and the dictionary from 0 we do ID-1 to check ID exist in the dictionary teacherid
                        if(teacherid[ID-1]["TeacherID"]!=ID or teacherid[ID-1]["Password"]!=password ):#If password or id false   
                            text = "incorrect id or password"
                            return render_template("Login.html",text=text)
                        else: #if password and id true they will be redirected to the teacermainpage
                            session["teacherID"] = ID
                            session["teacherName"] = teacherid[ID-1]["FirstName"]
                            conn.close()
                            return redirect(url_for("TeacherMainPage")) 
                    else:
                        text = "incorrect id or password"
                        return render_template("Login.html",text=text)
                    
                else:
                    text = "enter a valid ID number please"
                    return render_template("Login.html",text=text)
            if(who == "User"):#Check if user logs in
                x=0
                for row in d2:#Further preparation of data for password inspection and passing data
                    userid[x] = {"UserID":row[0],"Password":row[1],"FirstName":row[2],"LastName":row[3]}
                    x +=1 

                if ID.isdigit():#Check if entered data is digit
                    ID = int(ID)

                    if ID-1 in userid:#Because of ID starting from 1 and the dictionary from 0 we do ID-1 to check ID exist in the dictionary userid
                        if(userid[ID-1]["UserID"]!=ID or userid[ID-1]["Password"]!=password ):#If password or id false   
                            text = "incorrect id or password"
                            return render_template("Login.html",text=text)
                        else: #if password and id true they will be redirected to the usermainpage
                            session["userID"] = ID
                            session["userName"] = userid[ID-1]["FirstName"]
                            conn.close()
                            return redirect(url_for("UserMainPage"))
                    else:
                        text = "incorrect id or password"
                        return render_template("Login.html",text=text)
                else:
                    text = "enter a valid ID number please"
                    return render_template("Login.html",text=text)
            if(who == "Admin"):#Check if admin logs in
                x=0
                for row in d3:#Further preparation of data for password inspection and passing data
                    adminid[x] = {"AdminID":row[0],"Password":row[1],"FirstName":row[2],"LastName":row[3]}
                    x +=1 
                if ID.isdigit():#Check if entered data is digit
                    ID = int(ID)
                    if ID-1 in adminid:#Because of ID starting from 1 and the dictionary from 0 we do ID-1 to check ID exist in the dictionary adminid
                        if(adminid[ID-1]["AdminID"]!=ID or adminid[ID-1]["Password"]!=password ):#If password or id false  
                            text = "incorrect id or password"
                            return render_template("Login.html",text=text)
                        else: #if password and id true they will be redirected to the usermainpage
                            session["adminID"] = ID
                            session["adminName"] = adminid[ID-1]["FirstName"]
                            conn.close()
                            return redirect(url_for("AdminMainPage"))
                    else:
                        text = "incorrect id or password"
                        return render_template("Login.html",text=text)
                else:
                    text = "enter a valid ID number please"
                    return render_template("Login.html",text=text)
        except:
            text = "Please fill in all the requirements"
            return render_template("Login.html",text=text)
    text = "insert id and password"
    return render_template("Login.html",text=text)
@app.route("/logout",methods=['GET', 'POST'])
def Logout():
    session.pop("ID",None)
    session.pop("userID",None)
    session.pop("teacherID",None)
    session.pop("adminID",None)
    session.pop("teacherName",None)
    session.pop("userName",None)
    session.pop("adminName",None)
    return redirect(url_for("home"))
@app.route("/UserPage",methods=['GET', 'POST'])
def UserMainPage():
    if "userID" in session:#Checking here if the user logged out or left the website
        ID = session["userID"]
        Name = session["userName"]
        conn = sqlite3.connect(DB)

    
        courseuser=conn.execute("SELECT * FROM CourseUser WHERE UserID=?",str(ID))
   
        classes=[]#this array will be returned to html template to create a html table
        classes1 = {}

        #In these nested for loops we are going add data to our array where our user has classes for his courses
        for row in courseuser:#row[0]=courseName row[1]=UserID
    
            r=conn.execute("SELECT * FROM Class WHERE courseName=?",(row[0],))
            for row in r:
                classes.append({"className":row[1],"date":row[2],"location":row[3],"courseName":row[4],"TeacherID":row[5]})
    
        if request.method =="POST":#button pressed for registering user presence with specific code
            codeEntered = request.form["randomcode"]
    
            absence = conn.execute("SELECT * FROM Absent WHERE RandomCode=? AND UserID=?",(codeEntered,ID))
    
    
            x=0
            
            for row in absence:#put data in dictionary
                classes1[x]=({"RandomCode":row[0],"UserID":row[1]})
                x+=1 
            
            x=0  
    
            for row in classes1:
                if str(classes1[x]["RandomCode"])==str(codeEntered):#check given code
                    conn.execute("INSERT INTO Present (RandomCode,UserID) VALUES (?,?)",(codeEntered,ID),)#add their presence
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect(DB)
                    conn.execute("DELETE FROM Absent WHERE Randomcode=? AND UserID=?",(codeEntered,ID))#delete their absent
                    conn.commit()      
                    conn.close()
                    text="Succesfully registered"
                    return render_template("UserMainPage.html",Name=Name,classes=classes,text=text)
                x+=1
            if not classes1:
                text = "This code does not exist or you are already registered"
                return render_template("UserMainPage.html",Name=Name,classes=classes,text=text) 
            return render_template("UserMainPage.html",Name=Name,classes=classes)
        return render_template("UserMainPage.html",Name=Name,classes=classes)
    else:
        return redirect(url_for("home"))
randomcodearray = []
@app.route("/TeacherPage",methods=['GET', 'POST'])
def TeacherMainPage():

    if "teacherID" in session:#Checking here if the teacher logged out or left the website
        ID = session["teacherID"]
        Name = session["teacherName"]
        conn = sqlite3.connect(DB)
        courseteacher = conn.execute("SELECT * FROM CourseTeacher WHERE TeacherID=? ",str(ID),)
    
        courseteacherarray = []#this array will be returned to html template to create a html select
        for row in courseteacher:
            if row[0] not in courseteacherarray:
                courseteacherarray.append(row[0])
        if request.method =="POST":#button pressed
            try:
    
                classfor = request.form["showcoursesforclass"]

                classname = request.form["classname"]

                date = request.form["datee"]

                location = request.form["location"]

    
                if request.form["Create"]=="Create":#button create

    
                    rndcode = random.randint(1000,1000000)#generate randomcode
                    if rndcode not in randomcodearray:#making sure no duplicate

                        randomcodearray.append(rndcode)
                        conn.execute("INSERT INTO Class (RandomCode,className,date,location,courseName,TeacherID) VALUES (?,?,?,?,?,?)",(rndcode,classname,date,location,classfor,ID),)#creating class with given input data
    
                        conn.commit()
                        conn.close()
                        conn= sqlite3.connect(DB)
                        courseuser=conn.execute("SELECT * FROM CourseUser WHERE courseName=?",(classfor,))#getting data with the same coursename of class created
                        for row in courseuser:#putting all of the user to absent they have to register code for present
                            conn.execute("INSERT INTO Absent (RandomCode,UserID) VALUES (?,?)",(rndcode,row[1],))
                            conn.commit()
                        conn.close()
                        text = "Succesfully created. Give the following code to the students for registering their presenece. code :"
                        return render_template("TeacherMainPage.html",Name=Name,courses=courseteacherarray,text=text,rndcode=rndcode)
                    else:
                        text = "try again"
                        return render_template("TeacherMainPage.html",Name=Name,courses=courseteacherarray,text=text)                
                else:
                     return render_template("TeacherMainPage.html",Name=Name,courses=courseteacherarray)
            except:         
                if request.form["View"] == "View":#button view
                    codegiven = request.form["entercode"] 
    
                    checkcodegiven = conn.execute("SELECT RandomCode FROM Class WHERE RandomCode=? ",(codegiven,))
                    
                    checkcode = []
                    for row in checkcodegiven:#put data from checkcodegiven
                        checkcode.append(row[0])
                    if str(codegiven) in str(checkcode):
                        session["codegiven"]= codegiven#this is for passing data to other templates
                        conn.close()
                        return redirect(url_for("PresencePage"))
                    else:
                        text1 = "This code does not exist or you are not part of the class"
                        return render_template("TeacherMainPage.html",Name=Name,courses=courseteacherarray,text1=text1)
                return render_template("TeacherMainPage.html",Name=Name,courses=courseteacherarray)
            
        return render_template("TeacherMainPage.html",Name=Name,courses=courseteacherarray)
    else:

        return redirect(url_for("home"))
@app.route("/PresencePage",methods=['GET', 'POST'])
def PresencePage():
    if "teacherID" in session:#Checking here if the teacher logged out or left the website
 
        codegiven = session["codegiven"]
        conn = sqlite3.connect(DB)
    
        absentdata = conn.execute("SELECT Absent.RandomCode,User.FirstName,User.LastName FROM Absent INNER JOIN User ON Absent.UserID=User.UserID WHERE Absent.RandomCode = ? ",(codegiven,))
    
    
        presentdata = conn.execute("SELECT Present.Randomcode,User.FirstName,User.LastName FROM Present INNER JOIN User ON Present.UserID=User.UserID WHERE Present.RandomCode = ?",(codegiven,))
    
    
        presence=[]
    
        for row in presentdata:#appending array to show it in html table
            presence.append({"FirstName":row[1],"LastName":row[2],"Presence":"Present"})
        for row in absentdata:
            presence.append({"FirstName":row[1],"LastName":row[2],"Presence":"Absent"})
        conn.close()
        print(presence)
        return render_template("PresencePage.html",presence=presence,codegiven=codegiven)
    else:
        return redirect(url_for("TeacherMainPage"))
@app.route("/AdminPage",methods=['GET', 'POST'])
def AdminMainPage():
    if "adminID" in session:#Checking here if the admin logged out or left the website
        ID = session["adminID"]
        Name = session["adminName"]
        conn = sqlite3.connect(DB)
        #getting and preparing courses to show them in select html
        coursesdata1 = conn.execute("SELECT * FROM CourseTeacher ")
    
        coursesdata2 = conn.execute("SELECT * FROM CourseUser ")
    
        coursesdata3 = conn.execute("SELECT * FROM CourseAdmin ")
    
        courses = []
        for row in coursesdata1:
            if row[0] not in courses:
                courses.append(row[0])
            
        for row in coursesdata2:
            if row[0] not in courses:
                courses.append(row[0])
        for row in coursesdata3:
            if row[0] not in courses:
                courses.append(row[0])
        if request.method == "POST":#button pressed
            try:
                
                if request.form["Assign"]=="Assign": #assign button pressed
                    try:
                        idnumber = request.form["idassign"]
                        who = request.form["who"]
                        coursetoassign = request.form["showcoursesassign"]
                        if (who=="Teacher"):
                            x=0
                            conn.close()
                            conn = sqlite3.connect(DB)
                            d1 = conn.execute("SELECT * FROM Teacher ")
    
                            teacherid={}
                            for row in d1:
                                teacherid[x] = {"TeacherID":row[0]}
                                x +=1 
                            idnumber=int(idnumber)
                            if idnumber-1 in teacherid:    
                                conn.execute("INSERT INTO CourseTeacher (courseName,TeacherID) VALUES (?,?)",(coursetoassign,idnumber),)
                                conn.commit()
                                conn.close()
                                text = "Succesfully assigned"
                                return render_template("AdminMainPage.html",courses=courses,text=text)
                            else:
                                 text = "Try again. ID already registered to course or ID does not exist"
                                 return render_template("AdminMainPage.html",courses=courses,text=text)
                        if (who=="User"):
                            x=0
                            d2 = conn.execute("SELECT * FROM User ")
                            userid={}
                            for row in d2:
                                userid[x] = {"TeacherID":row[0]}
                                x +=1
                            idnumber=int(idnumber)
                            if idnumber-1 in userid:
    
                                conn.execute("INSERT INTO CourseUser (courseName,UserID) VALUES (?,?)",(coursetoassign,idnumber),)
                                conn.commit()
                                conn.close()
                                text = "Succesfully assigned"
                                return render_template("AdminMainPage.html",courses=courses,text=text)
                            else:
                                 text = "Try again. ID already registered to course or ID does not exist"
                                 return render_template("AdminMainPage.html",courses=courses,text=text)
                    except:

                        text = "Try again. ID already registered to course or ID does not exist"
                        return render_template("AdminMainPage.html",courses=courses,text=text)
                if request.form["Delete"]=="Delete":
                    coursedelete = request.form["showcoursesdelete"]
                    conn.execute("DELETE FROM CourseAdmin WHERE courseName=?",(coursedelete,))
                    conn.execute("DELETE FROM CourseUser WHERE courseName=?",(coursedelete,))
                    conn.execute("DELETE FROM CourseTeacher WHERE courseName=?",(coursedelete,))
                    conn.execute("DELETE FROM Absent WHERE RandomCode IN (SELECT RandomCode FROM Class WHERE courseName=?)",(coursedelete,))
                    conn.execute("DELETE FROM Present WHERE RandomCode IN (SELECT RandomCode FROM Class WHERE courseName=?)",(coursedelete,))
                    conn.execute("DELETE FROM Class WHERE courseName=?",(coursedelete,))
                    conn.commit()      
                    conn.close()
                    text1="Succesfully deleted"
                    return render_template("AdminMainPage.html",courses=courses,text1=text1)
                                            
            except:
                try:
                    if request.form["Create"]=="Create":
                        newcourse = request.form["coursecreate"]

    
                        conn.execute("INSERT INTO CourseAdmin (courseName,AdminID) VALUES (?,?)",(newcourse,ID),)
                        conn.commit()

                        conn.close()

                        text1="Succesfully created. Refresh page to see the course in assignment category."
                        return render_template("AdminMainPage.html",courses=courses,text1=text1)
                except:
                    text1 = "Try again. Course already exists"
                    return render_template("AdminMainPage.html",courses=courses,text1=text1) 
                    
    
    
        return render_template("AdminMainPage.html",Name=Name,courses=courses)   
    else:
        return redirect(url_for("home"))
    
    


# Add the resources to the API and specify the path



# Start the application
if __name__ == '__main__':
   app.run(port=8080)
#requests.get('localhost:8080/User')


