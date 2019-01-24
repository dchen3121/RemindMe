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


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.route('/auth/login', methods=['POST'])
def login_verification():
    username = request.form['username']
    password = request.form['password']
    if User.isvalid_login_username(username, password):
        User.login(username)
        return render_template('login_welcome.html', username=session['username'], text="logged in")
    else:
        session['username'] = None
        return render_template('login.html')


@app.route('/auth/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    User.signup_with_username(username, password)
    return render_template('login_welcome.html', username=session['username'], text="registered")


@app.route('/home', methods=['POST', 'GET'])  # basically list of classes
def homescreen_template():
    user = User.get_user_by_username(session['username'])
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_class = Class(title, description, "active", user.get_username())
        new_class.save_class_to_mongo()
    classes = user.get_classes_of_user()
    return render_template('homescreen.html', classes=classes, username=session['username'])


@app.route('/home/newsubject')  # creating new subject
def create_new_subject():
    return render_template('createsubject.html', username=session['username'])


@app.route('/home/subject/<string:class_id>', methods=['POST'])
def subject_template(class_id):
    subject = Class.get_class_by_id(class_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['description']
        date = request.form['date']
        due_date = request.form['due-date']
        new_note = Note(title, content, due_date, class_id, date)
        new_note.save_note_to_mongo()
    notes = subject.get_notes_from_class()
    return render_template('view_subject.html', notes=notes, username=session['username'], subject=class_id)



@app.route('/home/subject/newnote/<string:class_id>')  # creating new note inside a class
def create_new_note(class_id):
    return render_template('createnote.html', username=session['username'], subject=class_id)



# requirement to run our app
if __name__ == '__main__':
    app.run(port=4999)
