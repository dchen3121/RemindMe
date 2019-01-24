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
    return render_template('home.html')

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')



# requirement to run our app
if __name__ == '__main__':
    app.run(port=4999)