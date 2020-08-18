from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

chosenclass ='107i pm'
                  
app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ray:''@localhost/reports'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    studentid = db.Column(db.String(20))
    name = db.Column(db.String(100))    
    classroom = db.Column(db.String(100))
    classtime = db.Column(db.String(20))
    pacomment = db.Column(db.String(255))
    pbcomment = db.Column(db.String(255))
    pccomment = db.Column(db.String(255))

    def __init__(self, name, studentid, classroom, classtime):
        self.studentid = studentid
        self.name = name        
        self.classroom = classroom
        self.classtime = classtime
        self.pacomment = pacomment
        self.pbcomment = pbcomment
        self.pccomment = pccomment


#This is the index route where we are going to
#query on all our student data
@app.route('/' , methods = ["GET", "POST"])
def Index():
    all_data = Data.query.filter_by(classroom=chosenclass).all()
    return render_template("index.html", students = all_data)

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        studentid = request.form['studentid']
        classroom = request.form['classroom']
        classtime = request.form['classtime']
        pacomment = request.form['pacomment']
        pbcomment = request.form['pbcomment']
        pccomment = request.form['pccomment']

        my_data = Data(name, studentid, classroom, classtime, pacomment, pbcomment, pccomment)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")
        return redirect(url_for('Index'))


#this is our update route where we are going to update our students
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.studentid = request.form['studentid']
        my_data.classroom = request.form['classroom']
        my_data.classtime = request.form['classtime']
        my_data.pacomment = request.form['pacomment']
        my_data.pbcomment = request.form['pbcomment']
        my_data.pccomment = request.form['pccomment']
        

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))

#This route is for deleting our students
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)