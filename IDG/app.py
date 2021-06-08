import hashlib
import sqlite3
import cv2 as cv

from flask import Flask, request, make_response, redirect, url_for, session, Response
from flask import render_template
from time import sleep

app = Flask(__name__)
app.secret_key = b'\x13\x86#\xe6\xe4d\xeb\x7f\xe2 a\xff\xddY\xbf\x92'


@app.route("/overview")
def overview():
    if checkCookies():
        print("cookies ok")
        return render_template("overview.html", username=session["username"])

    print("cookie not ok")
    return redirect(url_for("login"))


@app.route("/homeDefence", methods=["GET", "POST"])
def homeDefence():


    return render_template("homeDefence.html")


@app.route("/moveup")
def moveup():
    print("go up")
    return ("nothing")


@app.route("/moveleft")
def moveleft():
    print("go left")
    return ("nothing")


@app.route("/moveright")
def moveright():
    print("go right")
    return ("nothing")


@app.route("/movedown")
def movedown():
    print("go down")
    return ("nothing")


def gen():
    i = 0
    while True:

        img = cv.imread(f"static/images/hedda{i}.jpg")
        img = cv.resize(img, (0, 0), fx=0.25, fy=0.25)
        frame = cv.imencode(".jpg", img)[1].tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # print("next img")
        i += 1
        if i >= 2:
            i = 0

        sleep(0.1)


@app.route("/getVideoFeed")
def getVideoFeed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def login(submit_response=0):
    resp = make_response(render_template("index.html"))

    if checkCookies() or submit_response == 1:
        if submit_response:
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]

        resp = make_response(redirect(url_for("overview")))


    elif submit_response == -1:
        resp = make_response(
            render_template("index.html", response="Invalid password or username", username=request.form["username"]))

    return resp


@app.route("/login", methods=["POST"])
def loginHandler():
    conn = sqlite3.connect("brukere.db")
    c = conn.cursor()

    if valid_login(request.form["username"], request.form["password"]):
        return login(1)
    return login(-1)


@app.route("/logout")
def logout():
    print("logging out")
    session.pop("username")
    session.pop("password")
    return redirect(url_for("login"))


def valid_login(username, password):
    encPassword = hashlib.pbkdf2_hmac('sha512', bytes(password, "utf-8"), b'salt', 100_000).hex()

    with sqlite3.connect("databases/brukere.db") as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM brukere WHERE username = :username AND password = :password",
                  {"username": username, "password": encPassword})

        user = c.fetchone()

        if user == None:
            return False

        if username == user[0] and encPassword == user[1]:
            return True
    return False


def checkCookies():
    cookie_username = None
    cookie_password = None

    try:
        cookie_username = session["username"]
        cookie_password = session["password"]
    except KeyError:
        pass

    if cookie_username is not None and cookie_password is not None:
        if valid_login(cookie_username, cookie_password):
            return True
    return False


if __name__ == '__main__':
    app.run()
