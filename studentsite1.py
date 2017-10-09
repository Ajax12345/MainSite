import flask
import db_interaction
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import datetime
import re
app = flask.Flask(__name__)
#SkillHost
#NEED: navigation bar
#TODO: add regular login bar
#TODO: make better homepage
#TODO: Create 404 page
#TODO: create "change password" route
#TODO: add control to check if a user is already verified in the "confirm_email" function
#TODO: style user confirmation email body
class User:
    def __init__(self, name):
        self.name = 3424245 if name is None else name
        self.email = None
        


    def __getitem__(self, token):
        if token in self.__dict__:
            return self.__dict__[token]

        raise KeyError("Please check variable '{}'".format(token))

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __str__(self):
        return self.name if "name" in self.__dict__ else self.username



user = User(None)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'jpetullo14@gmail.com',
    MAIL_PASSWORD = 'Gobronxbombers2',
))
mail = Mail(app)
ts = URLSafeTimedSerializer("secretkey")
#mail.init_app(app)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)


        #print "confired!!!, welcome", email
        #BUG: redirecting to account_issue.html when "login" is preceeded with forward slash
    except:
        return flask.render_template("account_issue.html")
    db_interaction.set_verified(email)

    return flask.redirect(flask.url_for("login"))



    #db_interaction.set_verified(email)


def send_confirmation_email(name, email, user_linkup):

    print "here"
    msg = Message(subject="Studenthost Account Confirmation", sender="jpetullo14@gmail.com", recipients=[email])
    msg.html = flask.render_template("account_confirmation.html", confirm_url=user_linkup)
    mail.send(msg)

@app.route("/")
def home_page():
    print user
    return flask.render_template('home.html')

@app.route("/login_with_google", methods=["GET", "POST"])
def google_login():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        username = flask.request.form["username"]
        print "google credentials", [email, username]

        return flask.redirect("/")

    else:
        return flask.render_template("google_login.html")
@app.route("/login_with_facebook", methods=["GET", "POST"])
def facebook_login():
    if flask.request.method == "POST":
        print "here"

    else:
        return flask.render_template("facebook_login.html")

@app.route("/login_with_twitter", methods=["GET", "POST"])
def twitter_login():
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        user_login_attempt = db_interaction.get_user_name(email, password)
        if not db_interaction.check_user(email):
            return flask.render_template("login.html", invalid_form='Account not created', account_confirmed = '')
        if not db_interaction.is_verified(email):
            return flask.render_template("login.html", invalid_form='', account_confirmed = '', not_verified="Your account has not been confirmed")

        if not user_login_attempt:
            return flask.render_template("login.html", invalid_form='Invalid email or password', account_confirmed = '')
        else:
            global user
            user["name"] = user_login_attempt[0]
            user["email"] = email
            user["username"] = db_interaction.get_username(email, password)[0]
            return flask.redirect("/")
    else:
        return flask.render_template("login.html", invalid_form='', account_confirmed = '')

@app.route("/signup", methods=["GET", "POST"])
def user_signin():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        name = flask.request.form["name"]
        age = flask.request.form["age"]
        lastname = flask.request.form["lastname"]
        password2 = flask.request.form['password2']
        full_listing = [email, username, password, password2, name, lastname]
        full_listing1 = [name, lastname, email, password, username, "no"]
        if not age.isdigit():
            return flask.render_template("user_login.html", username_taken = '',email_taken='', password_issue = '', age_issue="Please enter a number", incomplete="")
        if len([i for i in full_listing if i]) != len(full_listing):
            return flask.render_template("user_login.html", username_taken = '', email_taken = '', password_issue = '', age_issue="", incomplete="Some forms are not filled out")

        if int(age) < 13 or int(age) > 19:
            return flask.render_template("user_login.html", username_taken = '', email_taken = '', password_issue = '', age_issue="You must be older than 13 years", incomplete="")

        if password != password2:
            return flask.render_template("user_login.html", username_taken = '', email_taken = '', password_issue = 'Passwords do not match', age_issue="", incomplete="")
        if not re.findall("[\w\W]+@[a-zA-Z]+\.[a-zA-Z]+", email):
            return flask.render_template("user_login.html", username_taken = '', invalid_email = "incorrect email format", email_taken = '', password_issue = '', age_issue="", incomplete="")
        if len(password) < 8 or len([i for i in password if i.isdigit()]) < 1 or len([i for i in password if i.isupper()]) < 1:
            return flask.render_template("user_login.html", username_taken = '', invalid_email = "", complexity="Password must consist of at least One uppercase letter, one digit, and be at least 8 characters long",email_taken = '', password_issue = '', age_issue="", incomplete="")

        if db_interaction.check_user(email):
            return flask.render_template("user_login.html", username_taken = '', email_taken = "email already taken", password_issue = '', age_issue="", incomplete="")
        db_interaction.add_user(*full_listing1)

        token = ts.dumps(email, salt='email-confirm-key')
        print "token", token
        confirm_url = flask.url_for('confirm_email', token=token, _external=True)
        send_confirmation_email(name, email, confirm_url)
        return flask.render_template("/prompt_email_confirm.html")
    else:
        return flask.render_template("user_login.html", username_taken = '', email_taken = '', password_issue = '')


if __name__=="__main__":
	app.debug = True;
app.run()
