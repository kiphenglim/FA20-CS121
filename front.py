import os
import decimal
from flask import Flask, flash, jsonify, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from fastai.basic_train import load_learner
from fastai.vision import open_image
from flask_cors import CORS,cross_origin

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
    style = False
    genre = False
    artist = False
    predictStyle = ""
    probStyle = ""
    predictGenre = ""
    probGenre = ""
    predictArtist = ""
    probArtist = ""
    styleh3 = ""
    genreh3 = ""
    artisth3 = ""

    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)

    file = request.files['file']

    if 'style2' in request.form:
      style = True
      styleh3 = "Style"
      predictStyle = predictStyleCategory(file)
      probStyle = predictStyleProb(file)
    
    if 'genre2' in request.form:
      genre = True
      genreh3 = "Genre"
      predictGenre = predictGenreCategory(file)
      probGenre = predictGenreProb(file)
    
    if 'artist2' in request.form:
      artist = True
      artisth3 = "Artist"
      predictArtist = predictArtistCategory(file)
      probArtist = predictArtistProb(file)

    # Check that the user selected a file
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    # Actually upload a file and reload the page with the file displayed
    if file and allowedFile(file.filename):
      filename = secure_filename(file.filename)
      fullPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(fullPath)
      #return render_template("index.html", uploadedImagePath = fullPath, styleTitle=styleh3, genreTitle=genreh3, artistTitle=artisth3)
      return render_template("index.html", uploadedImagePath = fullPath, stylePrediction=predictStyle, styleProbability=probStyle, genrePrediction=predictGenre, genreProbability=probGenre, artistPrediction=predictArtist, artistProbability=probArtist, styleTitle=styleh3, genreTitle=genreh3, artistTitle=artisth3)
    else:
      flash('Please select a file with a .png, .jpg, .jpeg, or .gif extension')
      
  return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))

def correctRound(arr, num):
  newList = []
  for value in arr:
    d = decimal.Decimal(str(value))
    decimal.getcontext().prec=num
    newList.append(d*1)
  return newList

### STYLE ###
#load the learner
styleLearn = load_learner(path='./models', file='style_unfreeze_300.pkl')
styleClasses = styleLearn.data.classes
styleList = ['Abstract Expressionism', 'Action Painting', 'Analytical Cubism', 'Art Nouveau', 'Baroque', 'Color Field Painting', 'Contemporary Realism', 'Cubism', 'Early_Renaissance', 'Expressionism', 'Fauvism', 'High Renaissance', 'Impressionism', 'Mannerism Late Renaissance', 'Minimalism', 'Naive Art Primitivism', 'New Realism', 'Northern Renaissance', 'Pointillism', 'Pop Art', 'Post Impressionism', 'Realism', 'Rococo', 'Romanticism', 'Symbolism', 'Synthetic Cubism', 'Ukiyo e']

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
  probList = prediction[2].numpy()
  probSorted = sorted(probList, key=lambda x: float(x), reverse=True)
  probRounded = correctRound(probSorted, 2)
  percentDict = {c: str(100*probRounded[i]) + "%" for (i, c) in enumerate(styleClasses)}
  percentList = [str(i).replace(',',':') for i in list(percentDict.items())]

  topFive = str(percentList[:5])
  specialChars = ['[', ']', "'", '"']
  for i in specialChars:
    topFive = topFive.replace(i, "")
  
  return "Top 5 Probabilities: " + topFive


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
  probList = prediction[2].numpy()
  probSorted = sorted(probList, key=lambda x: float(x), reverse=True)
  probRounded = correctRound(probSorted, 2)
  percentDict = {c: str(100*probRounded[i]) + "%" for (i, c) in enumerate(genreClasses)}
  percentList = [str(i).replace(',',':') for i in list(percentDict.items())]

  topFive = str(percentList[:5])
  specialChars = ['[', ']', "'", '"']
  for i in specialChars:
    topFive = topFive.replace(i, "")
  
  return "Top 5 Probabilities: " + topFive

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
  probList = prediction[2].numpy()
  probSorted = sorted(probList, key=lambda x: float(x), reverse=True)
  probRounded = correctRound(probSorted, 2)
  percentDict = {c: str(100*probRounded[i]) + "%" for (i, c) in enumerate(artistClasses)}
  percentList = [str(i).replace(',',':') for i in list(percentDict.items())]

  topFive = str(percentList[:5])
  specialChars = ['[', ']', "'", '"']
  for i in specialChars:
    topFive = topFive.replace(i, "")
  
  return "Top 5 Probabilities: " + topFive
