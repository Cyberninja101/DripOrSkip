from flask import Flask, redirect, url_for, render_template, request
from flask_session import Session
import os
import base64
import sys
import json


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


# Global analagous
# analogous_score = 0

@app.route("/")
def home():
    """
    This is the home/default page.
    """
    # Retrieve the analogous_score from the query parameters
    analogous_score = request.args.get('analogous_score', default=0, type=float)
    complimentary_score = request.args.get('complimentary_score', default=0, type=float)
    split_score = request.args.get('split_score', default=0, type=float)
    message = request.args.get('message', default="", type=str)
    promColorArray = request.args.get('promColorArray', default=json.dumps(["", ""]), type=str)
    promColorArray = json.loads(promColorArray) 

    print("This is right before entry: ", promColorArray)
    # print("Retrieved analogous score in home:", analogous_score)  # Debug output
    return render_template("home.html", message=message,analogous_score=analogous_score, complimentary_score=complimentary_score, split_score=split_score, promColorArray=promColorArray)


# Save image
@app.route('/save_image', methods=['POST'])
def save_image():
    # global analogous_score

    data = request.json['image']
    image_data = data.split(',')[1]  # Get the base64 part
    output_file_path = os.path.join('web_app', 'static', 'images', 'canvas_image.png')
    
    with open(output_file_path, 'wb') as f:
        f.write(base64.b64decode(image_data))  # Write the decoded image data to file

    # Run AI to rate photo
    everything = drip("/static/images/canvas_image.png")

    # Unpacking everything
    num_colors, analogous_score, complimentary_score, split_score = everything[0]
    promColorArray = everything[1]
    analogous_score = analogous_score/(num_colors - 1)
    complimentary_score = complimentary_score/num_colors
    split_score = split_score/num_colors

    print("analogous score: ", analogous_score)
    print("complimentary score: ", complimentary_score)
    print("split score: ", split_score)

    
    print("HIIII, this is save_image")
    # Redirect with the updated analogous score

    message = ""
    # Calculate drip mid or skip
    if (analogous_score >= 0.5 or complimentary_score >= 0.5 or split_score >= 0.5):
        message = "Drip"
    elif (analogous_score >= 0.2 or complimentary_score >= 0.2 or split_score >= 0.2):
        message = "Mid"
    else:
        message = "Skip"

    # set color shit

    
    print(promColorArray)


    return redirect(url_for("home", message=message, analogous_score=analogous_score, complimentary_score=complimentary_score, split_score=split_score, promColorArray=json.dumps(promColorArray)))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=8000)



