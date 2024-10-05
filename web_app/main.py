from flask import Flask, redirect, send_file, url_for, render_template, request, session, jsonify
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session



import os, shutil
import binascii
import sys
import base64

# import model stuff
sys.path.insert(1, '/model')


app = Flask(__name__)
app.secret_key = "1234"
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'


Session(app)


def run():
    # run all the model stuff
    # scale the analagous, complementary, and split scores, give it out of 100%
    # drip: at least 1 category is >0.8
    # mid: somewhere in between
    # skip: every category <0.5
    pass


    

@app.route("/")
def home():
    """
    This is the home/default page. ok
    """

    return render_template("home.html")

# save image
@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json['image']
    image_data = data.split(',')[1]  # Get the base64 part
    output_file_path = os.path.join('web_app','static','images', 'canvas_image.png')
    
    with open(output_file_path, 'wb') as f:  # Open file in binary write mode
        f.write(base64.b64decode(image_data))  # Write the decoded image data to file
        

    # run AI to rate photo 

    return jsonify(success=True)

# @app.route('/download')
# def download_file():
#     print("in download file func")
#     # Specify file path
#     return send_file('static/images/canvas_image.png', as_attachment=True)




if __name__ == "__main__":
    app.run(debug=True, use_reloader = False, host="0.0.0.0", port=8000) # Set debug = True for live changes in development