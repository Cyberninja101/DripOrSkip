from flask import Flask, redirect, url_for, render_template, request
from flask_session import Session
import os
import base64
import sys

# import model stuff
path = os.getcwd()
sys.path.insert(1, os.path.join(path, "model"))
from helper import drip


app = Flask(__name__)
app.secret_key = "1234"
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['TEMPLATES_AUTO_RELOAD'] = True
Session(app)


@app.route("/cam")
def cam():
    return render_template("cam.html")

@app.route("/")
def home():
    return redirect(url_for("cam"))



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=8000)
