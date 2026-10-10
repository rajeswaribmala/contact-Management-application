from flask import Flask,render_template,request,redirect
import sqlite3
import re
app=Flask(__name__)
def get_db():
    conn=sqlite3.connect("contacts.db")
    conn.row_factory=sqlite3.Row
    return conn
def init_db():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL, address TEXT,email TEXT UNIQUE,phone TEXT UNIQUE)""")
    conn.commit()
    conn.close()
init_db()
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+",email)
def is_valid_phone(phone):
    return phone.isdigit() and len(phone)==10
@app.route("/")
def index():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT*FROM contacts")
    contacts=cursor.fetchall();
    conn.close()
    return render_template("index.html",contacts=contacts)
@app.route("/add",methods=["GET","POST"])
def add_contact():
    if request.method=="POST":
        first=request.form["first_name"]
        last=request.form["last_name"]
        address=request.form["address"]
        email=request.form["email"]
        phone=request.form["phone"]
        if not is_valid_email(email):
            return "invalid email format"
        if not is_valid_phone(phone):
            return "invalid phone number"
        conn=get_db()
        cursor=conn.cursor()
        try:
            cursor.execute("""INSERT INTO contacts(first_name,last_name,address,email,phone)
                           VALUES(?,?,?,?,?)""",(first,last,address,email,phone))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email or phone already exists!"
        finally:
            conn.close()
        return redirect("/")
    return render_template("add.html")
@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit_contact(id):
    conn=get_db()
    cursor=conn.cursor()
    if request.method=="POST":
        first=request.form["first_name"]
        last=request.form["last_name"]
        address=request.form["address"]
        email=request.form["email"]
        phone=request.form["phone"]
        if not is_valid_email(email):
            return "Invalid email format"
        if not is_valid_phone(phone):
            return "Invalid phone number"
        cursor.execute(""" UPDATE contacts SET first_name=?,last_name=?,address=?,email=?,phone=? 
                       WHERE id=?""",(first,last,address,email,phone,id))
        conn.commit()
        conn.close()
        return redirect("/")
    cursor.execute("SELECT *FROM contacts WHERE id=?",(id,))
    contact=cursor.fetchone()
    conn.close()
    return render_template("edit.html",contact=contact)
@app.route("/delete/<int:id>")
def delete_contact(id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)



    
