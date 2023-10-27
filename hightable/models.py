from hightable import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Personal(db.Model):
  __tablename__ = "personal"

  idpersonal = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(100), nullable=False)
  lastname = db.Column(db.String(100), nullable=False)
  dob = db.Column(db.Date)
  gender = db.Column(db.String(6))
  email = db.Column(db.String(100), nullable=False)
  phone = db.Column(db.String(45))
  mailing = db.Column(db.String(100))
  user_id = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)


class Academic(db.Model):
  __tablename__ = "academic"

  idacademic = db.Column(db.Integer, primary_key=True)
  gradyear = db.Column(db.Integer, nullable=False)
  degrees = db.Column(db.String(150), nullable=False)
  institution = db.Column(db.String(150), nullable=False)
  faculty = db.Column(db.String(45), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)


class Employement(db.Model):
  __tablename__ = "employement"

  idemployement = db.Column(db.Integer, primary_key=True)
  jobtitle = db.Column(db.String(100), nullable=False)
  company = db.Column(db.String(100), nullable=False)
  workaddress = db.Column(db.String(150), nullable=False)
  workemail = db.Column(db.String(100), nullable=False)
  linkedin = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)


class Bio(db.Model):
  __tablename__ = "bio"

  idbio = db.Column(db.Integer, primary_key=True)
  pic = db.Column(db.String(100), nullable=False)
  customuser = db.Column(db.String(45), unique=True, nullable=False)
  description = db.Column(db.String(250), nullable=False)
  achievements = db.Column(db.String(150), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)


class User(db.Model, UserMixin):
  __tablename__ = "user"

  iduser = db.Column(db.Integer, primary_key=True)
  password = db.Column(db.String(45), nullable=False)
  username = db.Column(db.String(45), nullable=False)

  joblistings = db.relationship('Joblistings')
  personal = db.relationship('Personal')
  academic = db.relationship('Academic')
  employement = db.relationship('Employement')
  bio = db.relationship('Bio')

  def is_active(self):
    return True

  def get_id(self):
    return self.email

  def is_authenticated(self):
    return self.authenticated

  def is_anonymous(self):
    return False


class Verification(db.Model):
  __tablename__ = "verification"

  idverification = db.Column(db.Integer, primary_key=True)
  question1 = db.Column(db.String(100), nullable=False)
  question2 = db.Column(db.String(1100), nullable=False)
  hint = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)


class Joblistings(db.Model):
  __tablename__ = "joblistings"

  idjoblistings = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True),
                   default=func.now(),
                   nullable=False)
  jobtitle = db.Column(db.String(100), nullable=False)
  company = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(250), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
