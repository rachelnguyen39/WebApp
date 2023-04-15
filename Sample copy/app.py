from flask import Flask, render_template, request, abort, url_for
from flask_socketio import SocketIO
import db
import secrets
import ssl
# import logging

# this turns off Flask Logging, uncomment this to turn off Logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


app = Flask(__name__)

# secret key used to sign the session cookie
app.config['SECRET_KEY'] = secrets.token_hex()
socketio = SocketIO(app)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="./certs/hellfish.test.crt", keyfile="./certs/hellfish.test.key", password='rachelngkey')


# don't remove this!!
import socket_routes



# index page
@app.route("/")
def index():
    return render_template("index.jinja")

# login page
@app.route("/login")
def login():    
    return render_template("login.jinja")

# handles a post request when the user clicks the log in button
@app.route("/login/user", methods=["POST"])
def login_user():
    if not request.is_json:
        abort(404)

    username = request.json.get("username")
    password = request.json.get("password")

    user =  db.get_user(username)
    if user is None:
        return "Error: User does not exist!"
    
    hash_pwd, salt = db.hash_password(password, user.salt)

    if user.password.decode("utf-8") != hash_pwd:
        return "Error: Password does not match!"

    return url_for('home', username=request.json.get("username"))

# handles a get request to the signup page
@app.route("/signup")
def signup():
    return render_template("signup.jinja")

# handles a post request when the user clicks the signup button
@app.route("/signup/user", methods=["POST"])
def signup_user():
    if not request.is_json:
        abort(404)
    username = request.json.get("username")
    password = request.json.get("password")

    if db.get_user(username) is None:
        hashed_word = db.hash_password(password, None)
        hashed_pwd = hashed_word[0].encode()
        salt = hashed_word[1].encode()
        db.insert_user(username, hashed_pwd, salt)
        return url_for('home', username=username)
    return "Error: User already exists!"

# handler when a "404" error happens
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.jinja'), 404

# home page, where the messaging app is
@app.route("/home")
def home():
    if request.args.get("username") is None:
        abort(404)
    return render_template("home.jinja", username=request.args.get("username"))

if __name__ == '__main__':
    socketio.run(app, host='localhost', ssl_context=context)
