from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/job-listings')
def joblistings():
    return render_template("job_listings.html")