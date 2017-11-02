"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.sql import func

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
    button = request.args.get('submit')

    user = User.query.filter(User.email == email).first()

    if user and not (user.password == pword):
        flash("A user with that email exists. Please login or choose a different email.")
        return redirect('/users/user-login')
    elif user:
        session['userid'] = user.user_id
        return redirect('/users/' + str(user.user_id))

    # not user
    if button == "Register":
        # add user to db
        user = User(email=email, password=pword)
        db.session.add(user)
        db.session.commit()
        session['userid'] = user.user_id
        return redirect('/users/' + str(user.user_id))
    else:
        flash("That email doesn't exist. Please register or choose a different email.")
        return redirect('/users/user-login')


@app.route('/users/<user_id>')
def user_page(user_id):
    """Display users page"""

    flash("Logged In! Yay!")
    user = User.query.filter(User.user_id == session['userid']).one()
    return render_template('user-page.html', user=user)


@app.route('/users/log-out')
def log_out():
    """Log user out"""

    del session['userid']

    flash("Logged out.")
    return redirect('/')


@app.route('/movies')
def movie_list():

    movies = Movie.query.order_by(Movie.title).all()
    return render_template('movie-list.html', movies=movies)


@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    """ Display details from individual movie"""

    movie = Movie.query.filter(Movie.movie_id == movie_id).first()
    avg_rating = db.session.query(func.avg(Rating.score)).filter(
                                Rating.movie_id == movie.movie_id).one()
    avg_rating = '{:.2f}'.format(avg_rating[0])
    if session.get('userid'):
        userid = session.get('userid')
        u_rating = (db.session.query(Rating.score)
                              .filter(Rating.movie_id == movie_id,
                                      Rating.user_id == userid).first()
                   ) # end query
    return render_template('movie-page.html', movie=movie,
                                              rating=avg_rating,
                                              u_rating=u_rating)


@app.route('/movies/rating', methods=["POST"])
def rate_movie():
    movie_id = request.form.get("movie_id")
    user_id = request.form.get("user_id")
    score = request.form.get("score")

    u_rating = Rating.query.filter(Rating.movie_id == movie_id,
                                   Rating.user_id == user_id).first()
    if u_rating:
        u_rating.score = score
    else:
        new_rating = Rating(movie_id=movie_id, user_id=user_id, score=score)
        db.session.add(new_rating)

    db.session.commit()
    # success = 'yay'
    # return 'yay'



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
