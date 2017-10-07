import flask
import db_interaction
app = flask.Flask(__name__)
#NEED: navigation bar
#TODO: add email verification

class User:
    def __init__(self, name):
        self.name = "Guest" if name is None else name



user = User(None)
@app.route("/")
def home_page():
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
    pass


@app.route("/form_data", methods=["GET", "POST"])
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

        if db_interaction.check_user(email):
            return flask.render_template("user_login.html", username_taken = '', email_taken = "email already taken", password_issue = '', age_issue="", incomplete="")
        db_interaction.add_user(*full_listing1)
        #print [email, username, password, password2, name, lastname] #if password and password2 do not match, return html form with error message on top
        return flask.redirect("/")#here, will have to redirect to login page, not homepage
    else:
        return flask.render_template("user_login.html", username_taken = '', email_taken = '', password_issue = '')


if __name__=="__main__":
	app.debug = True;
app.run()
