from flask import Flask, render_template, request, session, make_response

from src.common.database import Database
from src.models.note import Note
from src.models.class_ import Class
from src.models.user import User



app = Flask(__name__)  # '__main__'
# secret key: to make sure the data we send in the form of a cookie is secure
app.secret_key = "dchen"



@app.before_first_request
def initialize_database():
    Database.initialize()



@app.route('/')
def home_template():
    session['username'] = None
    return render_template('home.html')



@app.route('/login')
def login_template():
    return render_template('login.html')



@app.route('/logout', methods=['POST'])
def logout_template():
    session['username'] = None
    return render_template('logout.html')



@app.route('/register')
def register_template():
    return render_template('register.html')



@app.route('/auth/login', methods=['POST'])
def login_verification():
    username = request.form['username']
    password = request.form['password']
    if User.isvalid_login_username(username, password):
        User.login(username)
        return render_template('success.html', username=session['username'], text="You have successfully logged in", extend_url="?")
    else:
        session['username'] = None
        return render_template('login.html')



@app.route('/auth/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    User.signup_with_username(username, password)
    return render_template('success.html', username=session['username'], text="You have successfully registered", extend_url="?")



@app.route('/auth/new_subject', methods=['POST'])
def new_subject_success():
    user = User.get_user_by_username(session['username'])
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_class = Class(title, description, "active", user.get_username())
        new_class.save_class_to_mongo()
    return render_template('success.html', username=session['username'], text="Edit successful", extend_url="?")



@app.route('/home', methods=['POST', 'GET'])  # basically list of classes
def homescreen_template():
    user = User.get_user_by_username(session['username'])
    classes = user.get_classes_of_user()
    return render_template('homescreen.html', classes=classes, username=session['username'])



@app.route('/home/newsubject')  # creating new subject
def create_new_subject():
    return render_template('createsubject.html', username=session['username'])



@app.route('/home/<string:class_id>', methods=['POST', 'GET'])
def subject_template(class_id):
    subject = Class.get_class_by_id(class_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']
        due_date = request.form['due-date']
        new_note = Note(title, content, due_date, class_id, date)
        new_note.save_note_to_mongo()
    notes = subject.get_notes_from_class()
    return render_template('view_subject.html', notes=notes, username=session['username'], subject=subject)


'''
@app.route('/home/subject/<string:class_id>/edit', methods=['POST', 'GET'])
def edit_subject(class_id):
    render_template()'''

@app.route('/auth/new_note/<class_id>', methods=['POST'])
def new_note_success(class_id):
    subject = Class.get_class_by_id(class_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']
        due_date = request.form['due-date']
        new_note = Note(title, content, due_date, class_id, date)
        new_note.save_note_to_mongo()
    return render_template('success.html', username=session['username'], text="Edit successful", extend_url=class_id)



@app.route('/home/subject/newnote/<string:class_id>')  # creating new note inside a class
def create_new_note(class_id):
    return render_template('createnote.html', username=session['username'], subject_id = class_id)



@app.route('/home/editclass/<string:class_id>') # editing a class
def edit_subject(class_id):
    subject = Class.get_class_by_id(class_id)
    return render_template('editsubject.html', username=session['username'], subject=subject)



@app.route('/auth/edit_subject', methods=['POST'])
def edit_subject_success():
    user = User.get_user_by_username(session['username'])
    old_class_id = request.form['subject-id']
    old_class = Class.get_class_by_id(old_class_id)
    title = request.form['title']
    description = request.form['description']
    new_class = Class(title, description, "active", user.get_username(), _id=old_class_id)
    old_class.update_class(new_class.json())
    return render_template('success.html', username=session['username'], text="Edit successful", extend_url="?")



@app.route('/home/<string:class_id>/editnote/<string:note_id>') # editing a class
def edit_note(class_id, note_id):
    subject = Class.get_class_by_id(class_id)
    note = Note.get_note_by_id(note_id)
    return render_template('editnote.html', username=session['username'], subject=subject, note=note)



@app.route('/auth/edit_note', methods=['POST'])
def edit_note_success():
    user = User.get_user_by_username(session['username'])
    old_note_id = request.form['note-id']
    old_note = Note.get_note_by_id(old_note_id)
    title = request.form['title']
    date = request.form['date']
    due_date = request.form['due-date']
    content = request.form['content']
    new_note = Note(title=title, due_date=due_date, class_id=old_note.get_class_id(),
                    content=content, date=date, _id=old_note_id)
    old_note.update_note(new_note.json())
    return render_template('success.html', username=session['username'], text="Edit successful",
                           extend_url="/" + old_note.get_class_id())



# requirement to run our app
if __name__ == '__main__':
    app.run(port=4991, debug=True)
