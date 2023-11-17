from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, InputForm, RegistrationForm
from config import Config
from datetime import datetime
import json


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    count = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "<Record {}>".format(self.count)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def home():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/input", methods=["GET", "POST"])
@login_required
def input():
    form = InputForm()
    if form.validate_on_submit():
        record = Record(user_id=current_user.id, count=form.count.data)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for("view"))
    return render_template("input.html", form=form)


@app.route("/view")
@login_required
def view():
    records = Record.query.filter_by(user_id=current_user.id).all()
    labels = [record.date.strftime("%Y/%m/%d %H:%M") for record in records]
    data = [str(record.count) for record in records]
    return render_template("view.html", records=records, n=len(records), labels=labels, data=data)


if __name__ == "__main__":
    app.run(debug=True)
