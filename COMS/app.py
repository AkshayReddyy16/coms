from flask import Flask, render_template,request
import smtplib
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import sqlite3 as sql
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
basedir = os.path.abspath(os.path.dirname(__file__))
currentdirectory=os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rollnumber = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True, nullable=False)
    course=db.Column(db.String(100))
    phonenumber=db.Column(db.Integer)
    parentphno=db.Column(db.Integer)
    hostelname=db.Column(db.String(100))
    roomno=db.Column(db.Integer)
    outime=db.Column(db.String(100))
    intime=db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def __repr__(self):
        return f'<Student {self.firstname}>'
class Student2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rollnumber = db.Column(db.String(100))
    place=db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    course=db.Column(db.String(100))
    phonenumber=db.Column(db.Integer)
    parentphno=db.Column(db.Integer)
    hostelname=db.Column(db.String(100))
    roomno=db.Column(db.Integer)
    outime=db.Column(db.String(100))
    intime=db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def __repr__(self):
        return f'<Student {self.firstname}>'


class std(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Student {self.firstname}>'
class time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outime=db.Column(db.DateTime)
    intime=db.Column(db.DateTime)
    def __repr__(self):
        return f'<Student {self.firstname}>'
@app.route('/')
def home():
   return render_template('index.html')
@app.route('/login1',methods=['POST'])
def login1():
    name=request.form['username']
    password=request.form['password']
    con = sql.connect("data.db")
    cur = con.cursor()
    statement = f"SELECT username from std WHERE username='{name}' AND Password = '{password}';"
    cur.execute(statement)
    if not cur.fetchone():
        print("Login failed")
    else:
        return render_template('index1.html')
    if(name=="Hostelwarden" and password=="warden123"):
        return render_template('admin.html')
@app.route('/guess')
def guess():
   return render_template('index1.html')
@app.route('/set')
def set():
   return render_template('home.html')
@app.route('/outing')
def outing():
   return render_template('outing.html')
@app.route('/leave')
def leave():
   return render_template('leave.html')
@app.route('/rules')
def rules():
    return render_template('rules.html')
@app.route('/login',methods=['POST'])
def recieve_data():
   name=request.form['name']
   rollnumber=request.form['Rollnumber']
   place=request.form['place']
   course=request.form['coursem']
   hostelname=request.form['hostel']
   roomno=request.form['roomno']
   phno=request.form['phonenumber']
   parentphno = request.form['parentphoneNumber']
   email=request.form['email']
   outime=request.form['outtime']
   intime=request.form['intime']
   sendemail(name,rollnumber,place,course,hostelname,roomno,phno,parentphno,email,outime,intime)
   user1 = Student2(name=name, rollnumber=rollnumber,place=place, course=course, hostelname=hostelname, roomno=roomno, phonenumber=phno,
                parentphno=parentphno, email=email,outime=outime,intime=intime)
   db.session.add(user1)
   db.session.commit()
   return render_template('granted.html',name=name,rollnumber=rollnumber,place=place,course=course,hostelname=hostelname,roomno=roomno,phno=phno,parentphno=parentphno,email=email,outime=outime,intime=intime)
@app.route('/leave',methods=['POST'])
def recieves_data():
   name=request.form['name']
   rollnumber=request.form['Rollnumber']
   course=request.form['coursem']
   hostelname=request.form['hostel']
   homeaddress=request.form['homeaddress']
   roomno=request.form['roomno']
   phno=request.form['phonenumber']
   parentphno = request.form['parentphoneNumber']
   email=request.form['email']
   purpose=request.form['purposeof']
   noofdays=request.form['noofdays']
   fromdate=request.form['From']
   todate=request.form['To']
   outime=request.form['outtime']
   intime=request.form['intime']
   # global sendadmin
   sendadmin=dict(name=name,rollnumber=rollnumber,course=course,hostelname=hostelname,homeaddress=homeaddress,roomno=roomno,phno=phno,parentphno=parentphno,email=email,purpose=purpose,
             noofdays=noofdays,fromdate=fromdate,todate=todate,outime=outime,intime=intime
             )
   approveadmin(sendadmin=sendadmin)

#    sendemail(name,rollnumber,place,course,hostelname,roomno,phno,parentphno,email,outime,intime)

@app.route('/admin')
def admin():
   return render_template('admin.html')
@app.route('/outingadmin')
def outingadmin():
   students=Student2.query.all()
   return render_template('outingadmin.html',students=students)
@app.route('/leaveadmin')
def leaveadmin():
   students=Student.query.all()
   return render_template('leaveadmin.html',students=students)
@app.route('/approveadmin')
def approveadmin(**sendadmin):
    return render_template('approveadmin.html',sendadmin=sendadmin)
@app.route('/homeadmin')
def homeadmin():
    return render_template('homeadmin.html')
def sendemail(name,rollnumber,place,course,hostelname,roomno,phno,parentphno,email,outime,intime):
   my_email = "iiitkottayamcoms@gmail.com"
   password = "qwyxksuejdmsglin"
   with smtplib.SMTP('smtp.gmail.com') as connection:
      connection.starttls()
      connection.login(user=my_email, password=password)
      email_message = f"Subject:college outing management system(coms)\n\n" \
                      f"Dear {name},\nYour leave for some reason has been apporved by our institution head\nName: {name}\nRollNumber:{rollnumber}\nplace to visit:{place}\nCourse and semester:{course}\n Hostel:{hostelname}\nRoomNo:{roomno}\nphonenumber:{phno}\nparent phonenumber:{parentphno}\noutime:{outime}\nIntime:{intime}"
      connection.sendmail(from_addr=my_email, to_addrs=email, msg=email_message)
if __name__ == '__main__':
   app.run(debug=True)

