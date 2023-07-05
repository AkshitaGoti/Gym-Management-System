from flask import Flask, render_template,request,redirect
import sqlite3
import threading
import smtplib
import pandas as pd
def connect_db():
    conn = sqlite3.connect('Database.db', check_same_thread=False)
    return conn 
def mail(msg1,to):
    ob=smtplib.SMTP("smtp.gmail.com",587)
    ob.starttls()
    ob.login("gym7892@gmail.com","ruadskaelrpaxjlk")  # please mention you email and password here
    subject="Welcome to Stoner Team!"
    body=msg1
    mes="subject:{}\n\n{}".format(subject,body)
    listofadd=[to]
    ob.sendmail("gym7892@gmail.com",listofadd,mes)
    ob.quit()
username=None
admin=False
member=False
trainer=False
app = Flask(__name__)
@app.route("/")
def home():
    global admin,member,trainer
    admin=False
    member=False
    trainer=False
    return render_template("home.html")
@app.route("/discover")
def discover():
    global admin,member,trainer
    return render_template('discover.html',admin=admin,member=member,trainer=trainer)

@app.route("/login",methods=['GET','POST'])
def login():
    global username,admin,member,trainer
    if request.method=="POST":
        email=request.form['email']
        passw=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username,access FROM login WHERE email=? and password=?",(email,passw))
        result=cursor.fetchone()
        if result:
            username=result[0]
            access=result[1]
            if access=='admin':
                admin=True
                member=False
                trainer=False
                return render_template("admin.html",username=username)
            elif access=="trainer":
                trainer=True
                admin=False
                member=False
                return render_template("trainer.html",username=username)
            elif access=="member":
                member=True
                trainer=False
                admin=False
                return render_template("member.html",username=username)
            else:
                return render_template("login.html",msg='login Successfull')
        else:  
            return render_template("login.html",msg="Invalid Credentials !")
    return render_template("login.html")
@app.route("/admin")
def admin():
    global username
    return render_template("admin.html",username=username);
@app.route("/member")
def member():
    return render_template("member.html",username=username)
@app.route("/profile")
def profile():
    global username,admin,member,trainer
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT email,age,height,weight,experience,achivements,intrest FROM profile WHERE username=?",(username,))
    result=cursor.fetchone()
    if result:
        return render_template("profile.html",username=username,email=result[0],age=result[1],height=result[2],weight=result[3],experiece=result[4],achivements=result[5],intrest=result[6],admin=admin,trainer=trainer,member=member)
    else:
        return render_template("profile.html",username=username)
@app.route("/edit_profile",methods=['GET','POST'])
def edit():
    global username,admin,member,trainer
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT email,age,height,weight,experience,achivements,intrest FROM profile WHERE username=?",(username,))
    result=cursor.fetchone()
    if request.method=='POST':
        re_username=request.form['username']
        email=request.form['email']
        age=request.form['age']
        height=request.form['height']
        weight=request.form['weight']
        experience=request.form['experience']
        achivements=request.form['achievements']
        interests=request.form['interests']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username From profile")
        result = []
        for row in cursor.fetchall():
            result.append(row[0])
        if username in result:
            cursor.execute("UPDATE profile SET email=?,age=?,height=?,weight=?,experience=?,achivements=?,intrest=? WHERE username=?",(email,age,height,weight,experience,achivements,interests,username))
            conn.commit()
            return render_template("edit_profile.html",msg="Profile Updated Succesfully")
        else:
            cursor.execute("INSERT INTO profile (username,email,age,height,weight,experience,achivements,intrest)VALUES(?,?,?,?,?,?,?,?)",(re_username, email, age, height, weight, experience, achivements, interests)) 
            conn.commit()   
            return render_template("edit_profile.html",msg="Profile Added Succesfully",admin=admin,trainer=trainer,member=member)
    if result:
        return render_template("edit_profile.html",admin=admin,trainer=trainer,member=member,username=username,email=result[0],age=result[1],height=result[2],weight=result[3],experiece=result[4],achivements=result[5],intrest=result[6])
    else:
        return render_template("edit_profile.html",admin=admin,trainer=trainer,member=member)

@app.route("/add_trainer",methods=["GET","POST"])
def add_trainer():
    if request.method=="POST":
        name=request.form['username']
        email=request.form['email']
        full_name=request.form['name']
        passw=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        acc='trainer'
        msg1=f"Dear {full_name},\n\n Congratulations on joining stoner! Your expertise will enhance our fitness services. Familiarize yourself with our policies and guidelines We're excited to work with you!\nYour login Details are :\nemail:{email}\n password:{passw}\n\nBest regards\nStoner Team "
        email_thread = threading.Thread(target=mail, args=(msg1,email))
        email_thread.start()
        cursor.execute("INSERT INTO login (username,email,Full_name,password,Access)VALUES(?,?,?,?,?)",(name,email,full_name,passw,acc))
        conn.commit()
        return render_template ("add_trainer.html",msg=f"Confirmation send to {name} via mail !")
    return render_template ("add_trainer.html")
@app.route("/delete_trainer",methods=['GET','POST'])
def delete_trainer():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username FROM login WHERE password=?",(password,))
        result=cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM login WHERE username=? and password=?",(name,password))
            conn.commit()
            return render_template("delete_trainer.html",msg="trainer Removed Succesfully!")
        else:
            return render_template("delete_trainer.html",msg="Trainer Not Found ! Check Again")  
    return render_template("delete_trainer.html")  
@app.route("/new_equip",methods=['GET','POST'])
def new_equip():
    if request.method=='POST':
        buy_date=request.form['buy_date']
        equip_name=request.form['equip_name']
        manufacturer=request.form['manufacturer']
        quantity=request.form['quantity']
        price=request.form['price']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO Equipments(buy_date, Equip_name, Manufacturer, Quantity, Price)VALUES(?,?,?,?,?)",(buy_date,equip_name,manufacturer,quantity,price))
        conn.commit()
        return render_template("new_equip.html",msg="New Equipment Added SuccesFully !")
    return render_template("new_equip.html")  

@app.route("/delete_equip",methods=['GET','POST'])
def delete_equip():
    if request.method=="POST":
        equip_name=request.form['equip_name']
        quantity=request.form['quantity']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT Quantity From Equipments WHERE Equip_name=?",(equip_name,))
        result=cursor.fetchone()
        if result:
            total=int(result[0])
            if int(quantity)>total:
                return render_template("delete_equip.html",msg=f"{quantity} are not avilable in Stock!")
            else:
                minus=total-int(quantity)
                cursor.execute("UPDATE Equipments SET Quantity=? WHERE Equip_name=?",(minus,equip_name))
                conn.commit()
                return render_template("delete_equip.html",msg="Removed Successfully")
        else:
            return render_template("delete_equip.html",msg="Equipment not found in database !")    
    return render_template("delete_equip.html")    
@app.route("/add_member",methods=['GET','POST'])
def Add_members():
    global username,admin,trainer,member
    if request.method=="POST":
        name=request.form['username']
        email=request.form['email']
        full_name=request.form['name']
        passw=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        acc='member'
        pay='pending'
        msg1=f"Dear {full_name},\n\nWe are thrilled to inform you that your membership at Sotner has been confirmed! Congratulations and welcome to our fitness community.\nYour Login Credentials are : \n Email:{email}\nPassword: {passw}\nWe are excited to have you on board and look forward to helping you achieve your fitness goals. Our team of experienced trainers and state-of-the-art facilities are ready to assist you every step of the way.\n\n Best Regards \n stoner Staff"
        email_thread = threading.Thread(target=mail, args=(msg1,email))
        email_thread.start()
        cursor.execute("INSERT INTO login (username,email,Full_name,password,Access,Payment)VALUES(?,?,?,?,?,?)",(name,email,full_name,passw,acc,pay))
        conn.commit()
        return render_template ("add_member.html",msg=f"Confirmation send to {name} via mail !",admin=admin,member=member,trainer=trainer)
    return render_template ("add_member.html",admin=admin,member=member,trainer=trainer)
@app.route("/view_equipment")
def view_equipment():
    global admin,member
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT buy_date,Equip_name,Manufacturer,Quantity,Price FROM Equipments")
    results=cursor.fetchall()
    df = pd.DataFrame(results, columns=['buy_date','Equip_name','Manufacturer','Quantity','Price'])
    buy_date=df['buy_date'].tolist()
    equip=df['Equip_name'].tolist()
    mft=df['Manufacturer'].tolist()
    quantity=df['Quantity'].tolist()
    price=df['Price'].tolist()
    return render_template("equip_list.html",buy_date=buy_date,equip=equip,mft=mft,quantity=quantity,price=price,admin=admin,member=member)
@app.route("/view_staff")
def view_staff():
    conn=connect_db()
    cursor=conn.cursor()
    acc='trainer'
    cursor.execute("SELECT username,Full_name,email,password FROM login WHERE Access=?",(acc,))
    results=cursor.fetchall()
    df = pd.DataFrame(results, columns=['username','Full_name','email','password'])
    us_name=df['username'].tolist()
    f_name=df['Full_name'].tolist()
    email=df['email'].tolist()
    passw=df['password'].tolist()
    return render_template("view_staff.html",us_name=us_name,f_name=f_name,email=email,passw=passw,admin=True)
@app.route("/view_member")
def view_member():
    global admin,trainer,member
    conn=connect_db()
    cursor=conn.cursor()
    acc='member'
    cursor.execute("SELECT username,Full_name,email,password,Payment FROM login WHERE Access=?",(acc,))
    results=cursor.fetchall()
    df = pd.DataFrame(results, columns=['username','Full_name','email','password','Payment'])
    us_name=df['username'].tolist()
    f_name=df['Full_name'].tolist()
    email=df['email'].tolist()
    passw=df['password'].tolist()
    pay=df['Payment'].tolist()
    return render_template("view_member.html",us_name=us_name,f_name=f_name,email=email,passw=passw,pay=pay,mem=True,admin=admin,trainer=trainer,member=member)
@app.route("/delete_view_member",methods=['GET','POST'])
def delete_view_member():
    global admin,trainer,member
    if request.method=="POST":
        name=request.form['username']
        passw=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        acc='member'
        cursor.execute("SELECT username FROM login WHERE Access=?",(acc,))
        records=cursor.fetchall()
        username_list = []
        for record in records:
           username = record[0]  # Assuming the username is the first column in the query result
           username_list.append(username)
        if name in username_list:
            cursor.execute("DELETE FROM login WHERE username=? AND password=?",(name,passw))
            conn.commit()
            return render_template("delete_view.html",msg="Merber Removed !",admin=admin,trainer=trainer,member=member)
        else:
            return render_template("delete_view.html",msg="User Not Found !",admin=admin,trainer=trainer,member=member)
    return render_template("delete_view.html",admin=admin,trainer=trainer,member=member)
@app.route("/trainer")
def trainer():
    global username
    return render_template("trainer.html",username=username)
@app.route("/shedule_class",methods=["GET","POST"])
def shedule_class():
    global admin,trainer,member
    if request.method=='POST':
        name=request.form['username']
        shift=request.form['shift']
        date=request.form['date']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        ex1=request.form['exercise1']
        rap1=request.form['raps1']
        ex2=request.form['exercise2']
        rap2=request.form['raps2']
        ex3=request.form['exercise3']
        rap3=request.form['raps3']
        ex4=request.form['exercise4']
        rap4=request.form['raps4']
        ex5=request.form['exercise5']
        rap5=request.form['raps5']
        per=request.form['per']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username FROM class_shedule")
        results=cursor.fetchall()
        user_list=[]
        for result in results:
            user_list.append(result[0])
        if name in user_list:
            cursor.execute("UPDATE class_shedule SET shift=?,date=?,start_time=?,end_time=?,exercise_1=?,exercise_1_raps=?,exercise_2=?,exercise_2_raps=?,exercise_3=?,exercise_3_raps=?,exercise_4=?,exercise_4_raps=?,exercise_5=?,exercise_5_raps=?,Performance=? WHERE username=?",(shift,date,start_time,end_time,ex1,rap1,ex2,rap2,ex3,rap3,ex4,rap4,ex5,rap5,per,name))
            conn.commit()
            return render_template("shedule_class.html",msg=f"Class Update sent to {name}",admin=admin,trainer=trainer,member=member)
        else:
            cursor.execute("INSERT INTO class_shedule(username,shift,date,start_time,end_time,exercise_1,exercise_1_raps,exercise_2,exercise_2_raps,exercise_3,exercise_3_raps,exercise_4,exercise_4_raps,exercise_5,exercise_5_raps,Performance)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name,shift,date,start_time,end_time,ex1,rap1,ex2,rap2,ex3,rap3,ex4,rap4,ex5,rap5,per))
            conn.commit()
            return render_template("shedule_class.html",msg=f"Class Update sent to {name}",admin=admin,trainer=trainer,member=member)
    return render_template("shedule_class.html",admin=admin,trainer=trainer,member=member)


@app.route("/show_my_schedule")
def show_my_shedule():
    global username
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT shift,date,start_time,end_time,exercise_1,exercise_1_raps,exercise_2,exercise_2_raps,exercise_3,exercise_3_raps,exercise_4,exercise_4_raps,exercise_5,exercise_5_raps,performance FROM class_shedule WHERE username=?",(username,))
    result=cursor.fetchone()
    if result:
        shift=result[0]
        date=result[1]
        start_time=result[2]
        end_time=result[3]
        ex1=result[4]
        rp1=result[5]
        ex2=result[6]
        rp2=result[7]
        ex3=result[8]
        rp3=result[9]
        ex4=result[10]
        rp4=result[11]
        ex5=result[12]
        rp5=result[13]
        performance=result[14]
        return render_template("my_shedule.html",shift=shift,date=date,start_time=start_time,end_time=end_time,ex1=ex1,rp1=rp1,ex2=ex2,rp2=rp2,ex3=ex3,rp3=rp3,ex4=ex4,rp4=rp4,ex5=ex5,rp5=rp5,performance=performance)
    else:
        return render_template("my_shedule.html",msg="schedule Not Set Yet !")
@app.route("/feedback",methods=['GET','POST'])
def feedback():
    if request.method=='POST':
        name=request.form['name']
        mess=request.form['message']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO feedback(name,message)VALUES(?,?)",(name,mess))
        conn.commit()
        return render_template("feedback.html",msg='Thankyou for your feedback !')
    return render_template("feedback.html")
@app.route("/payment",methods=['GET','POST'])
def payment():
    global username
    if request.method=='POST':
        name=request.form['username']
        email=request.form['email']
        doular=request.form['amount']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("UPDATE login SET Payment='Succesfull' WHERE username=?",(username,))
        conn.commit()
        msg1=f"Dear {name}\n\n  Your payment has been successfully received by us. Thank you for your payment.\n\n Regards\nStoner Team"
        email_thread = threading.Thread(target=mail, args=(msg1,email))
        email_thread.start()
        return render_template("payment.html",msg="A Confirmation message is sent to you mail")
    return render_template("payment.html")

@app.route("/add_trainer_shedule",methods=['GET','POST'])
def trainer_shedule():
    if request.method=='POST':
        name=request.form['name']
        shift=request.form['shift']
        date=request.form['date']
        to_date=request.form['to_date']
        start_time=request.form['start_time']
        end_time=request.form['end_time'] 
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username FROM trainer_shedule")
        results=cursor.fetchall()
        user_list=[]
        for result in results:
            user_list.append(result[0])
        cursor.execute("SELECT email FROM login WHERE username=?",(name,))
        result=cursor.fetchone()
        email=result[0]
        if name in user_list:
            cursor.execute("UPDATE trainer_shedule SET shift=?,date=?,To_date=?,start_time=?,end_time=? WHERE username=?",(shift,date,to_date,start_time,end_time,name))
            conn.commit()
            msg1=f"Dear {name} \n\n Hope you are doing well\n This is inform to you that your Shedule is updated and details are given below Please read Carefully !\n\n From date:{date}\nTo Date:{to_date}\nShift: {shift}\n From Time: {start_time} \n To Time:{end_time}\n Thankyou"
            email_thread = threading.Thread(target=mail, args=(msg1,email))
            email_thread.start()
            return render_template("trainer_shedule.html",msg="shedule Updated Succesfully!")
        else:
            cursor.execute("INSERT INTO trainer_shedule(username,shift,date,To_date,start_time,end_time)VALUES(?,?,?,?,?,?)",(name,shift,date,to_date,start_time,end_time))
            conn.commit()
            msg1=f"Dear {name} \n\n Hope you are doing well\n This is inform to you that your Shedule is set and details are given below Please read Carefully !\n\n From date:{date}\nTo Date:{to_date}\nShift: {shift}\n From Time: {start_time} \n To Time:{end_time}\n Thankyou"
            email_thread = threading.Thread(target=mail, args=(msg1,email))
            email_thread.start()
            return render_template("trainer_shedule.html",msg="shedule Set !")
    return render_template("trainer_shedule.html")

@app.route("/trainer__shedule")
def my_trainer_shedule():
    global username
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT shift,date,To_date,start_time,end_time FROM trainer_shedule WHERE username=?",(username,))
    result=cursor.fetchone()
    if result:
        shift=result[0]
        date=result[1]
        to_date=result[2]
        start_time=result[3]
        end_time=result[4]
        return render_template("my_trainer_shedule.html",username=username,shift=shift,date=date,to_date=to_date,start_time=start_time,end_time=end_time)
    else :
        return render_template("my_trainer_shedule.html",msg=True,username=username)
if __name__=="__main__":
    app.run(debug=True,port="9999")