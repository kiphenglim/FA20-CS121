import os
from flask import Flask, flash, jsonify, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from fastai.basic_train import load_learner
from fastai.vision import open_image
from flask_cors import CORS, cross_origin
import requests

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_PATH = ""

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.debug = True
# Check if the file is an image (we might have to change this to only 1 type of extension for alpha)


def allowedFile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('instructions.html')


@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        # check if the post request has the file part
        stylePrediction = ""
        styleProbability = ""
        genrePrediction = ""
        genreProbability = ""
        artistPrediction = ""
        artistProbability = ""
        styleTitle = ""
        genreTitle = ""
        artistTitle = ""
        similarImages = []

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if 'style2' in request.form:
        styleTitle = "Style"
        stylePrediction = predictStyleCategory(file)
        styleProbability = predictStyleProb(file)
        query = stylePrediction + 'paintings'
        similarImages += getImages(query)
    
    if 'genre2' in request.form:
        genreTitle = "Genre"
        genrePrediction = predictGenreCategory(file)
        genreProbability = predictGenreProb(file)
        query = genrePrediction + 'paintings'
        similarImages += getImages(query)
    
    if 'artist2' in request.form:
        artistTitle = "Artist"
        artistPrediction = predictArtistCategory(file)
        artistProbability = predictArtistProb(file)
        query = artistPrediction + 'paintings'
        similarImages += getImages(query)

    # Check that the user selected a file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # Actually upload a file and reload the page with the file displayed
    if file and allowedFile(file.filename):
        filename = secure_filename(file.filename)
        uploadedImagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploadedImagePath)
        return render_template("index.html", **locals())
    else:
        flash('Please select a file with a .png, .jpg, .jpeg, or .gif extension')
      
  return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))

### Google API helper ###
def getImages(query):
    results = []
    req = requests.get('https://www.googleapis.com/customsearch/v1?key=AIzaSyB_cvfozOcU8r34KrvayV82thQqlAv74PA&cx=354adf1e91b6d54cb&searchType=image&num=3&q='+query).json()
    for img in req["items"]:
        results.append(img["link"])
  
    return results

### STYLE ###
# load the learner
styleLearn = load_learner(path='./models', file='style_unfreeze_300.pkl')
styleClasses = styleLearn.data.classes
styleList = ['Abstract Expressionism', 'Action Painting', 'Analytical Cubism', 'Art Nouveau', 'Baroque', 'Color Field Painting', 'Contemporary Realism', 'Cubism', 'Early_Renaissance', 'Expressionism', 'Fauvism', 'High Renaissance', 'Impressionism',
             'Mannerism Late Renaissance', 'Minimalism', 'Naive Art Primitivism', 'New Realism', 'Northern Renaissance', 'Pointillism', 'Pop Art', 'Post Impressionism', 'Realism', 'Rococo', 'Romanticism', 'Symbolism', 'Synthetic Cubism', 'Ukiyo e']

# make prediction and load into json


def predictStyleCategory(img_file):
    # function to take image and return prediction
    prediction = styleLearn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    predictionKey = styleClasses[prediction[1].item()]
    return "Predicted Category: " + str(predictionKey)


def predictStyleProb(img_file):
    # function to take in image and return top 5 predictions
    prediction = styleLearn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    probabilityRaw = {c: round(float(probs_list[i]), 5) for (
        i, c) in enumerate(styleClasses)}

    probabilitySorted = sorted(
        probabilityRaw.items(), key=lambda x: x[1], reverse=True)

    topFiveProb = str(probabilitySorted[:5])
    specialChars = ['[', ']', "'"]
    for i in specialChars:
        topFiveProb = topFiveProb.replace(i, "")

    return "Top 5 Probabilities: " + topFiveProb


### GENRE ###
# load the learner
genreLearn = load_learner(path='./models', file='genreLRChanged.pkl')
genreClasses = genreLearn.data.classes

# make prediction and load into json


def predictGenreCategory(img_file):
    # function to take image and return prediction
    prediction = genreLearn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    predictionKey = genreClasses[prediction[1].item()]
    return "Predicted Category: " + str(predictionKey)


def predictGenreProb(img_file):
    # function to take in image and return top 5 predictions
    prediction = genreLearn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    probabilityRaw = {c: round(float(probs_list[i]), 5) for (
        i, c) in enumerate(genreClasses)}

    probabilitySorted = sorted(
        probabilityRaw.items(), key=lambda x: x[1], reverse=True)

    topFiveProb = str(probabilitySorted[:5])
    specialChars = ['[', ']', "'"]
    for i in specialChars:
        topFiveProb = topFiveProb.replace(i, "")

    return "Top 5 Probabilities: " + topFiveProb


### ARTIST ###
# load the learner
artistLearn = load_learner(path='./models', file='artistLR2.pkl')
artistClasses = artistLearn.data.classes

# make prediction and load into json


def predictArtistCategory(img_file):
    # function to take image and return prediction
    prediction = artistLearn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    predictionKey = artistClasses[prediction[1].item()]
    return "Predicted Category: " + str(predictionKey)


def predictArtistProb(img_file):
    # function to take in image and return top 5 predictions
    prediction = artistLearn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    probabilityRaw = {c: round(float(probs_list[i]), 5) for (
        i, c) in enumerate(artistClasses)}

    probabilitySorted = sorted(
        probabilityRaw.items(), key=lambda x: x[1], reverse=True)

    topFiveProb = str(probabilitySorted[:5])
    specialChars = ['[', ']', "'"]
    for i in specialChars:
        topFiveProb = topFiveProb.replace(i, "")

    return "Top 5 Probabilities: " + topFiveProb
