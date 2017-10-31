"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ILoveMovies"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Index."""

    return render_template("index.html")


@app.route('/users')
def user_list():
    """ Show list of users."""

    users = User.query.all()
    return render_template('user-list.html', users=users)


@app.route('/users/user-login')
def user_form():
    """ Show login/create form to user."""

    return render_template('user-login.html')


@app.route('/users/user-verify')
def user_verify():

    email = request.args.get('email')
    pword = request.args.get('pword')

    user = User.query.filter(User.email == email).first()
    if user:
        if user.password == pword:
            return redirect('/users/<user.user_id>')
    else:
        flash("email or password not found or incorrect")
        return redirect('/users/user-login')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
