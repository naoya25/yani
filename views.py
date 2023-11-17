from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from forms import LoginForm, InputForm
from models import User, Record

@app.route('/')
@login_required
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input():
    form = InputForm()
    if form.validate_on_submit():
        record = Record(user_id=current_user.id, count=form.count.data)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('view'))
    return render_template('input.html', form=form)

@app.route('/view')
@login_required
def view():
    records = Record.query.filter_by(user_id=current_user.id).all()
    return render_template('view.html', records=records)
