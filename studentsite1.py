import flask
app = flask.Flask(__name__)
#NEED: navigation bar
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
        lastname = flask.request.form["lastname"]
        password2 = flask.request.form['password2']
        print [email, username, password, password2, name, lastname] #if password and password2 do not match, return html form with error message on top
        return flask.redirect("/")#here, will have to redirect to login page, not homepage
    else:
        return flask.render_template("user_login.html", username_taken = '', password_issue = '')


if __name__=="__main__":
	app.debug = True;
app.run()



@app.route("/form_data", methods=["GET", "POST"])
def user_signin():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        password2 = flask.request.form['password2']
        print [email, username, password, password2] #if password and password2 do not match, return html form with error message on top
        return flask.redirect("/")#here, will have to redirect to login page, not homepage
    else:
        return flask.render_template("user_login.html")


if __name__=="__main__":
	app.debug = True;
app.run()
