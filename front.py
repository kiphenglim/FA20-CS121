import os
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

@app.route('/', methods=['GET', 'POST'])
def uploadFile():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # Check that the user selected a file
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    # Actually upload a file and reload the page with the file displayed
    if file and allowedFile(file.filename):
      filename = secure_filename(file.filename)
      fullPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(fullPath)
      return render_template("index.html", uploadedImagePath = fullPath, stylePrediction=predictStyleCategory(file), styleProbability=predictStyleProb(file))
    else:
      flash('Please select a file with a .png, .jpg, .jpeg, or .gif extension')
      
  return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))

# load the learner
learn = load_learner(path='./models', file='allStylesBasic.pkl')
classes = learn.data.classes
styleList = ['Abstract Expressionism', 'Action Painting', 'Analytical Cubism', 'Art Nouveau', 'Baroque', 'Color Field Painting', 'Contemporary Realism', 'Cubism', 'Early_Renaissance', 'Expressionism', 'Fauvism', 'High Renaissance', 'Impressionism', 'Mannerism Late Renaissance', 'Minimalism', 'Naive Art Primitivism', 'New Realism', 'Northern Renaissance', 'Pointillism', 'Pop Art', 'Post Impressionism', 'Realism', 'Rococo', 'Romanticism', 'Symbolism', 'Synthetic Cubism', 'Ukiyo e']

# make prediction and load into json
def predictStyleCategory(img_file):
  # function to take image and return prediction
  prediction = learn.predict(open_image(img_file))
  probs_list = prediction[2].numpy()
  predictionKey = int(classes[prediction[1].item()])
  return "Predicted Category: " + styleList[predictionKey]

def predictStyleProb(img_file):
  # function to take in image and return top 5 predictions
  prediction = learn.predict(open_image(img_file))
  probs_list = prediction[2].numpy()
  probabilityRaw = {styleList[c]: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)}
  
  print(type(probabilityRaw))
  probabilitySorted = sorted(probabilityRaw.items(), key=lambda x: x[1], reverse=True)

  topFiveProb = str(probabilitySorted[:5])
  specialChars = ['[', ']', "'"]
  for i in specialChars:
    topFiveProb = topFiveProb.replace(i, "")
  
  return "Top 5 Probabilities: " + topFiveProb
