"""This file serves as the model for our entire art classifier
website. It holds functionality for uploading/displaying images,
making requests to several fast.ai image classification models, and
defines routes for our index.html and instructions.html pages.

"""

from flask import Flask, flash, request, redirect, render_template
from flask_cors import CORS
import imghdr
from make_predictions import predict_artist_category, predict_artist_prob, \
predict_genre_category, predict_genre_prob, predict_style_category, \
predict_style_prob
import os
from PIL import Image
import requests
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
IMAGE_PATH = ""

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.debug = True


def valid_image_extension(filename):
    """ Given the name of a file, returns True if has an allowed image extension. """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def valid_image_contents(filename):
    """ Given the name of a file, returns True if the contents are valid. """
    return imghdr.what(filename) in ALLOWED_EXTENSIONS


@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    """ Defines a route to the instructions page. """
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('instructions.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """ Method for uploading and displaying an image back to the user. """
    uploaded_image_path = os.path.join('static', "uploadPH.jpg")
    if request.method == 'POST':
        # check if the post request has the file part
        style_prediction = ""
        style_probability = ""
        genre_prediction = ""
        genre_probability = ""
        artist_prediction = ""
        artist_probability = ""
        style_title = ""
        genre_title = ""
        artist_title = ""
        similar_images = []

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # Check that the user selected a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Actually upload a file and reload the page with the file displayed
        if file and valid_image_extension(file.filename):
            filename = secure_filename(file.filename)
            uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_image_path)

            if valid_image_contents(uploaded_image_path):
                if 'style2' in request.form:
                    style_title = "Style"
                    style_prediction = predict_style_category(file)
                    style_probability = predict_style_prob(file)
                    query = style_prediction.split(' ')[2] + ' paintings'
                    similar_images += get_images(query)

                if 'genre2' in request.form:
                    genre_title = "Genre"
                    genre_prediction = predict_genre_category(file)
                    genre_probability = predict_genre_prob(file)
                    query = genre_prediction.split(' ')[2] + ' paintings'
                    similar_images += get_images(query)

                if 'artist2' in request.form:
                    artist_title = "Artist"
                    artist_prediction = predict_artist_category(file)
                    artist_probability = predict_artist_prob(file)
                    query = artist_prediction.split(' ')[2] + ' paintings'
                    similar_images += get_images(query)

                return render_template("index.html", scroll="results", **locals())
            else:
                flash('Please check that your file has not been corrupted.')
        else:
            flash('Please select a file with a .png, .jpg, or .jpeg extension')
    return render_template("index.html", **locals())


### Google API helper ###
def get_images(query):
    """ Google API helper. Given a string query, returns a Google image search for that query. """
    results = []
    req = requests.get('https://www.googleapis.com/customsearch/v1?'+
    'key=AIzaSyAiQj6ucyXTGM8hbKfCQJ-39s5M8qPZrLQ&cx=23cebd78935069e14&' +
    'searchType=image&num=3&q='+query).json()

    if 'searchInformation' in req and req["searchInformation"]["totalResults"] != "0":
        for img in req["items"]:
            results.append(img["link"])

    return results
