import json
from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_BINDS']= {'notes':"sqlite:///notes.db"}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        

    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
  
@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
   

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
         title=request.form['title']
         desc=request.form['desc']
         todo=Todo.query.filter_by(sno=sno).first()
         todo.title = title
         todo.desc=desc
         db.session.add(todo)
         db.session.commit()
         return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")   


class Notes(db.Model):
    __bind_key__ = 'notes'
    sno1=db.Column(db.Integer,primary_key=True)
    title1=db.Column(db.String(200),nullable=False)
    date_created1=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno1} - {self.title1}"

@app.route("/notes/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title1=request.form['title1']
        note=Notes(title1=title1)
        db.session.add(note)
        db.session.commit()
        

    allnote=Notes.query.all()
    return render_template('notes.html',allnote=allnote)
  
@app.route("/shownote")
def show():
    allnote=Notes.query.all()
    print(allnote)
   

@app.route("/updatenotes/<int:sno1>", methods=['GET', 'POST'])
def updatenote(sno1):
    if request.method=='POST':
        title1=request.form['title1']
        
        note=Notes.query.filter_by(sno1=sno1).first()
        note.title1 = title1
         
        db.session.add(note)
        db.session.commit()
        return redirect("/notes/")

    note=Notes.query.filter_by(sno1=sno1).first()
    return render_template('updatenotes.html',note=note)

@app.route("/deletenotes/<int:sno1>")
def deletenote(sno1):
    note=Notes.query.filter_by(sno1=sno1).first()
    db.session.delete(note)
    db.session.commit()
    return redirect("/notes/")   

@app.route("/login")
def login():
     return render_template('login.html')

   
if __name__=="__main__":
    app.run(debug=True)    

        