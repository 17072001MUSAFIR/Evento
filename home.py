import time
import glob
import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template,session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import db
import requests
import json
from time import sleep  

app.secret_key ='hello'

app.config['MYSQL_HOST'] = db.mysql_host
app.config['MYSQL_USER'] = db.mysql_user
app.config['MYSQL_PORT'] = db.mysql_port
app.config['MYSQL_PASSWORD'] = db.mysql_password
app.config['MYSQL_DB'] = db.mysql_db


mysql = MySQL(app)

@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        u = details['unm']
        p = details['pwd']
        cur = mysql.connection.cursor()
        r=cur.execute("select * from login where uname='"+u+"' and pass='"+p+"'")
        if r>0:
            d=cur.fetchall()
            r1=cur.execute("select * from user where email='"+u+"'")
            if r1>0:
                d=cur.fetchall()
                session['nlog']=d[0][1]
                session['emlog']=d[0][2]
                session['id']=d[0][0]
                return render_template("main_base.html")
            else:
                flash("Complete the profile")
                return render_template("bio.html",a=d)
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    error=None
    if request.method == "POST":
        details = request.form
        n=details['name']
        em=details['email']
        p = details['psw']
        cp = details['psw-repeat']
        st = 1
        if p!=cp:
            error = "Password is not matching"
        else:
            cur = mysql.connection.cursor()
            r=cur.execute("select * from login where uname='"+em+"'")
            if r>0:
                error = "Email is already exist"
            else:
                cur.execute("INSERT INTO login(name,uname,pass) VALUES (%s,%s,%s)", (n,em,p))
                mysql.connection.commit()
                cur.close()
                flash("You are succesfully registered")
                return render_template("login.html")
    return render_template('register.html',error=error)

@app.route('/bio', methods=['GET', 'POST'])
def bio():
    if request.method == "POST":
        details = request.form
        nm1 = details['nm']
        em1 = details['em']
        mob1 = details['mob']
        dob1 = details['dob']
        addr1 = details['addr']
        st1 = details['st']
        ct1 = details['ct']
        pin1 = details['pin']
        cur = mysql.connection.cursor()
        r=cur.execute("INSERT INTO user(name,email,mob,dob,address,state,city,pin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (nm1,em1,mob1,dob1,addr1,st1,ct1,pin1))
        mysql.connection.commit()
        r=cur.execute("select * from user where name='"+nm1+"' and email='"+em1+"'")
        if r>0:
            d=cur.fetchall()
            return render_template("bio1.html",res=d)
    return render_template('bio.html')

@app.route('/bio1', methods=['GET', 'POST'])
def bio1():
    if request.method == "POST":
        details = request.form
        id2 = details['id1']
        cou1 = details['cou']
        bch1 = details['bch']
        colnm1 = details['colnm']
        pl1 = details['pl']
        yog1 = details['yog']
        ia1 = details['ia']
        cur = mysql.connection.cursor()
        r=cur.execute("INSERT INTO user1(userid,cou,brn,conm,place,yog,intar) VALUES (%s,%s,%s,%s,%s,%s,%s)", (id2,cou1,bch1,colnm1,pl1,yog1,ia1))
        mysql.connection.commit()
        return render_template("main_base.html")
    return render_template('bio1.html')

@app.route('/bio2')#, methods=['GET', 'POST'])
def bio2():
    nlog1=session['nlog']
    emlog1=session['emlog']
    cur = mysql.connection.cursor()
    r=cur.execute("select * from user where name='"+nlog1+"' and email='"+emlog1+"'")
    if r>0:
        d=cur.fetchall()
        r=cur.execute("select * from user a,user1 b where a.id=b.userid and a.id='"+str(d[0][0])+"'")
        d1=cur.fetchall()
        print(d1)
        return render_template("bio2.html",res=d1)
    #return render_template('bio.html')

@app.route('/updatebio', methods=['GET', 'POST'])
def updatebio():
    nlog1=session['nlog']
    emlog1=session['emlog']
    cur = mysql.connection.cursor()
    r=cur.execute("select * from user where name='"+nlog1+"' and email='"+emlog1+"'")
    if r>0:
        d=cur.fetchall()
        r=cur.execute("select * from user a,user1 b where a.id=b.userid and a.id='"+str(d[0][0])+"'")
        d1=cur.fetchall()
        print(d1)
        return render_template("updatebio.html",res=d1)

@app.route('/bioupdate1', methods=['GET', 'POST'])
def bioupdate1():
    if request.method == "POST":
        details = request.form
        nm1 = details['nm']
        em1 = details['em']
        mob1 = details['mob']
        dob1 = details['dob']
        addr1 = details['addr']
        st1 = details['st']
        ct1 = details['ct']
        pin1 = details['pin']
        id2 = details['id1']
        cou1 = details['cou']
        bch1 = details['bch']
        colnm1 = details['colnm']
        pl1 = details['pl']
        yog1 = details['yog']
        ia1 = details['ia']
        cur = mysql.connection.cursor()
        r=cur.execute("update user set name=%s,email=%s,mob=%s,dob=%s,address=%s,state=%s,city=%s,pin=%s where id=%s", (nm1,em1,mob1,dob1,addr1,st1,ct1,pin1,id2))
        r=cur.execute("update user1 set cou=%s,brn=%s,conm=%s,place=%s,yog=%s,intar=%s where userid=%s", (cou1,bch1,colnm1,pl1,yog1,ia1,id2))
        mysql.connection.commit()
        return redirect("/bio2")
    return render_template("updatebio.html")

@app.route('/event_main')
def event_main():
    id1 = session['id']
    cur = mysql.connection.cursor()
    r=cur.execute("select * from event where uid='"+str(id1)+"'")
    if r>0:
        d=cur.fetchall()
        print(d)
        return render_template("event_main.html",res=d)
    return render_template("event_main.html")
    

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        details = request.form
        id1 = session['id']
        title1 = details['title']
        sdt1 = details['sd']
        edt1 = details['ed']
        sdt2 = details['st']
        edt2 = details['et']
        moe1 = details['moe']
        loc1 = details['loc']
        maxp1 = details['maxp']
        desc1 = details['desc']
        file = request.files['ban']
        filename = secure_filename(file.filename)
        f=filename
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO event(uid,title,dts,dte,mode,location,mp,des,banner,ts,te) VALUES ('"+str(id1)+"','"+title1+"','"+sdt1+"','"+edt1+"','"+moe1+"','"+loc1+"','"+maxp1+"','"+desc1+"','"+f+"','"+sdt2+"','"+edt2+"')")
        mysql.connection.commit()
        cur.close()
        if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                f=filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f))
                flash('File successfully uploaded')
                return render_template("event_main.html")
        else:
                flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                return redirect(request.url)
    return render_template("event.html")

@app.route('/register_main')
def register_main():
    id1 = session['id']
    cur = mysql.connection.cursor()
    r=cur.execute("SELECT * FROM event where uid!='"+str(id1)+"'")
    if r>0:
        d=cur.fetchall()
        return render_template("register_main.html",res=d)
    return render_template("register_main.html")

@app.route('/event_des/<string:id>')
def event_des(id):
    cur = mysql.connection.cursor()
    r=cur.execute("select * from event where id='"+str(id)+"'")
    if r>0:
        d=cur.fetchall()
        return render_template("event_des.html",res=d)
        print(l)
    return render_template("event_des.html")

@app.route('/register_des/<string:id>')
def register_des(id):
    cur = mysql.connection.cursor()
    r=cur.execute("select * from event where id='"+str(id)+"'")
    if r>0:
        d=cur.fetchall()
        return render_template("register_des.html",res=d)
    return render_template("register_des.html")

@app.route('/register_event/<string:id10>')
def register_event(id10):
    id1=session['id']
    cur = mysql.connection.cursor()
    r=cur.execute("insert into reg_eve(uid,eid) values('"+str(id1)+"','"+str(id10)+"')")
    r1=cur.execute("update event set mp=mp-1 where id='"+str(id10)+"'")
    mysql.connection.commit()
    flash("Successfully Registered")
    return render_template("main_base.html")
    #return render_template("register_event.html")

@app.route('/dashboard')
def dashboard():
    id1 = session['id']
    cur = mysql.connection.cursor()
    r=cur.execute("SELECT * FROM reg_eve where uid='"+str(id1)+"'")
    if r>0:
        d=cur.fetchall()
        print(d)
        for i in d:
            print(i)
            r=cur.execute("SELECT * FROM event where id='"+str(i[2])+"'")
            d1=cur.fetchall()
            return render_template("dashboard.html",res=d1)
    return render_template("dashboard.html")

@app.route('/dashboard_des/<string:id>')
def dashboard_des(id):
    cur = mysql.connection.cursor()
    r=cur.execute("select * from event where id='"+str(id)+"'")
    if r>0:
        d=cur.fetchall()
        return render_template("dashboard_des.html",res=d)
    return render_template("dashboard_des.html")

@app.route('/dashboard_cancel/<string:id10>')
def dashboard_cancel(id10):
    id1=session['id']
    cur = mysql.connection.cursor()
    r=cur.execute("delete from reg_eve where uid='"+str(id1)+"' and eid='"+str(id10)+"'")
    r1=cur.execute("update event set mp=mp+1 where id='"+str(id10)+"'")
    mysql.connection.commit()
    flash("Succesfully unregistered the event")
    return redirect("dashboard.html")

if __name__ == '__main__':
    app.run()
