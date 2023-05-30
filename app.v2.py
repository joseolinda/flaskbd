from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length, Regexp
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200)) 
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

class Professor(db.Model):
    id = db.Column('professor_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subjects = db.Column(db.String(150))
    education = db.Column(db.String(100))
    hire_date = db.Column(db.Date())

    def __init__(self, name, subjects, education, hire_date):
        self.name = name
        self.subjects = subjects
        self.education = education
        self.hire_date = hire_date

class NewStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=50)])
    addr = StringField('Address', validators=[DataRequired(), Length(max=200)])
    pin = StringField('PIN', validators=[DataRequired(), Length(max=10)])

class NewProfessorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    subjects = StringField('Subjects', validators=[DataRequired(), Length(max=150)])
    education = StringField('Education', validators=[DataRequired(), Length(max=100)])
    hire_date = DateField('Hire Date', validators=[DataRequired()])

@app.route('/')
def show_all():
    students = Student.query.all()
    return render_template('show_all.html', students=students)

@app.route('/new', methods=['GET', 'POST'])
def new_student():
    form = NewStudentForm()
    if form.validate_on_submit():
        existing_student = Student.query.filter_by(name=form.name.data).first()
        if existing_student:
            flash('Student already exists', 'error')
        else:
            student = Student(form.name.data, form.city.data, form.addr.data, form.pin.data)
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully')
            return redirect(url_for('show_all'))
    return render_template('new.html', form=form)

@app.route('/new_professor', methods=['GET', 'POST'])
def new_professor():
    form = NewProfessorForm()
    if form.validate_on_submit():
        existing_professor = Professor.query.filter_by(name=form.name.data).first()
        if existing_professor:
            flash('Professor already exists', 'error')
        else:
            professor = Professor(form.name.data, form.subjects.data, form.education.data, form.hire_date.data)
            db.session.add(professor)
            db.session.commit()
            flash('Professor added successfully')
            return redirect(url_for('show_all'))
    return render_template('new_professor.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
