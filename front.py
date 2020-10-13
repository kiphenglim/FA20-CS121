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

  return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))

# load the learner
learn = load_learner(path='./models', file='fauvismUkiyoE.pkl')
classes = learn.data.classes

# make prediction and load into json
def predictStyleCategory(img_file):
  # function to take image and return prediction
  prediction = learn.predict(open_image(img_file))
  probs_list = prediction[2].numpy()
  return "Predicted Category: " + str(classes[prediction[1].item()])

def predictStyleProb(img_file):
  prediction = learn.predict(open_image(img_file))
  probs_list = prediction[2].numpy()
  probability = str({c: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)})
  specialChars = ['{', '}', "'"]
  for i in specialChars:
    probability = probability.replace(i, "")
  return "Probabilities: " + probability