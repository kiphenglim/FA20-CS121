"""This file serves as the model for our entire art classifier
website. It holds functionality for uploading/displaying images,
making requests to several fast.ai image classification models, and
defines routes for our index.html and instructions.html pages.

"""

import os
from flask import Flask, flash, request, redirect, render_template
import decimal
from werkzeug.utils import secure_filename
from fastai.basic_train import load_learner
from fastai.vision import open_image
from flask_cors import CORS
import requests

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_PATH = ""

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.debug = True
# Check if the file is an image
# We might have to change this to only 1 type of extension for alpha


def allowed_file(filename):
    """ Given the name of a file, returns True if has an allowed image extension. """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    """ Defines a route to the instructions page. """
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('instructions.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """ Method for uploading and displaying an image back to the user. """
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

        if 'style2' in request.form:
            style_title = "Style"
            style_prediction = predict_style_category(file)
            style_probability = predict_style_prob(file)
            query = style_prediction + 'paintings'
            similar_images += get_images(query)

        if 'genre2' in request.form:
            genre_title = "Genre"
            genre_prediction = predict_genre_category(file)
            genre_probability = predict_genre_prob(file)
            query = genre_prediction + 'paintings'
            similar_images += get_images(query)

        if 'artist2' in request.form:
            artist_title = "Artist"
            artist_prediction = predict_artist_category(file)
            artist_probability = predict_artist_prob(file)
            query = artist_prediction + 'paintings'
            similar_images += get_images(query)

        # Check that the user selected a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Actually upload a file and reload the page with the file displayed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_image_path)
            return render_template("index.html", **locals())

        flash('Please select a file with a .png, .jpg, .jpeg, or .gif extension')
    return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))


def correct_round(arr, num):
  newList = []
  for value in arr:
    d = decimal.Decimal(str(value))
    decimal.getcontext().prec=num
    newList.append(d*1)
  return newList

### Google API helper ###
def get_images(query):
    """ Google API helper. Given a string query, returns a Google image search for that query. """
    results = []
    req = requests.get('https://www.googleapis.com/customsearch/v1?'+
    'key=AIzaSyB_cvfozOcU8r34KrvayV82thQqlAv74PA&cx=354adf1e91b6d54cb&' +
    'searchType=image&num=3&q='+query).json()
    for img in req["items"]:
        results.append(img["link"])

    return results

### STYLE ###
# load the learner
style_learn = load_learner(path='./models', file='style_unfreeze_300.pkl')
style_classes = style_learn.data.classes
style_list = ['Abstract Expressionism', 'Action Painting', 'Analytical Cubism',
            'Art Nouveau', 'Baroque', 'Color Field Painting',
            'Contemporary Realism', 'Cubism', 'Early_Renaissance',
            'Expressionism', 'Fauvism', 'High Renaissance', 'Impressionism',
            'Mannerism Late Renaissance', 'Minimalism',
            'Naive Art Primitivism', 'New Realism', 'Northern Renaissance',
            'Pointillism', 'Pop Art', 'Post Impressionism', 'Realism',
            'Rococo', 'Romanticism', 'Symbolism', 'Synthetic Cubism', 'Ukiyo e']

# make prediction and load into json
def predict_style_category(img_file):
    """ Given an image file, returns the top style prediction. """
    prediction = style_learn.predict(open_image(img_file))
    prediction_key = style_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key)


def predict_style_prob(img_file):
    """ Given an image file, returns the top five style predictions. """
    prediction = style_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    prob_sorted = sorted(prob_list, key=lambda x: float(x), reverse=True)
    prob_rounded = correct_round(prob_sorted, 2)
    percent_dict = {c: str(100*prob_rounded[i]) + "%" for (i, c) in enumerate(style_classes)}
    percent_list = [str(i).replace(',',':') for i in list(percent_dict.items())]

    top_five = str(percentList[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
      top_five = top_five.replace(i, "")

    return "Top 5 Probabilities: " + top_five


### GENRE ###
# load the learner
genre_learn = load_learner(path='./models', file='genreLRChanged.pkl')
genre_classes = genre_learn.data.classes

# make prediction and load into json
def predict_genre_category(img_file):
    """ Given an image file, returns the top genre prediction. """
    prediction = genre_learn.predict(open_image(img_file))
    prediction_key = genre_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key)


def predict_genre_prob(img_file):
    """ Given an image file, returns the top five genre predictions. """
    prediction = genre_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    prob_sorted = sorted(probs_list, key=lambda x: float(x), reverse=True)
    prob_rounded = correct_round(prob_sorted, 2)
    percent_dict = {c: str(100*prob_rounded[i]) + "%" for (i, c) in enumerate(genre_classes)}
    percent_list = [str(i).replace(',',':') for i in list(percent_dict.items())]

    top_five = str(percent_list[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
      top_five = top_five.replace(i, "")

    return "Top 5 Probabilities: " + top_five


### ARTIST ###
# load the learner
artist_learn = load_learner(path='./models', file='artistLR2.pkl')
artist_classes = artist_learn.data.classes

# make prediction and load into json
def predict_artist_category(img_file):
    """ Given an image, returns the top artist prediction. """
    prediction = artist_learn.predict(open_image(img_file))
    prediction_key = artist_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key)


def predict_artist_prob(img_file):
    """ Given an image, returns the top five artist predictions. """
    prediction = artist_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    prob_sorted = sorted(probs_list, key=lambda x: float(x), reverse=True)
    prob_rounded = correct_round(prob_sorted, 2)
    percent_dict = {c: str(100*prob_rounded[i]) + "%" for (i, c) in enumerate(artist_classes)}
    percent_list = [str(i).replace(',',':') for i in list(percent_dict.items())]

    top_five = str(percentList[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
      top_five = top_five.replace(i, "")

    return "Top 5 Probabilities: " + top_five
