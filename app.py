from flask import Flask, render_template, redirect, url_for, request
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
        return redirect(url_for("home"))
    return render_template("input.html", form=form)


@app.route("/")
@login_required
def home():
    user_id = request.args.get("user_id")
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        records = Record.query.filter_by(user_id=user.id).all()
    else:
        records = Record.query.filter_by(user_id=current_user.id).all()
    labels = [record.date.strftime("%Y/%m/%d %H:%M") for record in records]
    data = [str(record.count) for record in records]
    return render_template("index.html", records=records, n=len(records), labels=labels, data=data, user=User.query.get(user_id))


@app.route("/usage")
def usage():
    return render_template("usage.html")


@app.route("/ranking")
def ranking():
    user_counts = (
        db.session.query(Record.user_id, db.func.sum(Record.count)).group_by(Record.user_id).all()
    )
    sorted_counts = sorted(user_counts, key=lambda x: x[1], reverse=True)

    # ユーザーのRecordが存在しない場合は、本数を0としてランキングに追加する
    user_ids = [user_id for user_id, _ in sorted_counts]
    users_without_records = User.query.filter(User.id.notin_(user_ids)).all()
    for user in users_without_records:
        sorted_counts.append((user.id, 0))
    ranked_counts = [
        (rank, user_id, count) for rank, (user_id, count) in enumerate(sorted_counts, start=1)
    ]

    return render_template("ranking.html", ranked_counts=ranked_counts, User=User)


if __name__ == "__main__":
    app.run(debug=True)
