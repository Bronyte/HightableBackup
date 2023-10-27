from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from hightable.db import db
from hightable.models import User, Joblistings, Personal
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['Get', 'Post'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
      if check_password_hash(user.password, password):
        flash('You have been logged in!')
        login_user(user, remember=True)
      return redirect(url_for('views.home'))
    else:
      flash('Invalid username or password')
  return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    username = request.form.get('username')

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    dateOfBirth = request.form.get('dataOfBirth')
    email = request.form.get('email')
    phone = request.form.get('phone')
    mailing = request.form.get('mailing')

    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    max_iduser = db.session.query(db.func.max(User.iduser)).scalar()
    max_idpersonal = db.session.query(db.func.max(
        Personal.idpersonal)).scalar()

    new_iduser = max_iduser + 1 if max_iduser is not None else 1
    new_idpersonal = max_idpersonal + 1 if max_idpersonal is not None else 1

    existing_user = User.query.filter_by(username=username).first()

    if password1 == password2:
      flash("Passwords match")
      password = password1
      if existing_user:
        flash("Username already exists")
      else:
        
        new_user = User(iduser=new_iduser,
                        username=username,
                        password=generate_password_hash(password1,
                                                        method='sha256'))
        
        db.session.add(new_user)

        user_id = new_user.iduser

        new_personal = Personal(idpersonal=new_idpersonal,
                                firstname=firstname,
                                lastname=lastname,
                                dob=dateOfBirth,
                                email=email,
                                phone=phone,
                                mailing=mailing,
                                user_id=user_id)

        db.session.add(new_personal) 
        db.session.commit()
        flash("Registration successful. You can now log in.")
        return render_template("auth.login")
    else:
      flash("Passwords do not match!")
  return render_template("auth.sign_up")


@auth.route('/mail', methods=['GET', 'POST'])
@login_required
def mail():
  return render_template("mail.html")


@auth.route('/news', methods=['GET', 'POST'])
def news():
  return render_template("news.html")


@auth.route('/career', methods=['GET', 'POST'])
@login_required
def career():
  return render_template("career.html")


@auth.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
  return render_template("calendar.html")


@auth.route('/job-listing', methods=['GET', 'POST'])
@login_required
def joblisting():
  if request.method == 'POST':
    jobtitle = request.form.get('jobtitle')
    description = request.form.get('description')
    company = request.form.get('company')

    max_idjoblistings = db.session.query(db.func.max(Joblistings.idjoblistings)).scalar()

    new_idjoblistings = max_idjoblistings + 1 if max_idjoblistings is not None else 1

    user_id = current_user.id
    
    if len(jobtitle) < 1 or len(description) < 1 or len(company) < 1:
      flash("Please fill in all fields")
    else:
      new_job = Joblistings(idjoblistings=new_idjoblistings,
                            jobtitle=jobtitle,
                           description=description,
                           company=company,
                           user_id=user_id)
      db.session.add(new_job)
      db.session.commit()
  return render_template("views.job")
