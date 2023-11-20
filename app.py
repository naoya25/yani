from flask import Flask, request, render_template, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth
import os

cred = credentials.Certificate("service-account-key.json")
firebase_admin.initialize_app(cred)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", msg="")

    email = request.form["email"]
    password = request.form["password"]
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session["usr"] = email
        return redirect(url_for("index"))
    except:
        return render_template("users/login.html", msg="メールアドレスまたはパスワードが間違っています。")


@app.route("/", methods=["GET"])
def index():
    usr = session.get("usr")
    if usr == None:
        return redirect(url_for("login"))
    return render_template("yanis/index.html", usr=usr)


@app.route("/logout")
def logout():
    del session["usr"]
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
