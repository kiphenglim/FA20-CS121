import os
from flask import Flask, flash, jsonify, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from fastai.basic_train import load_learner
from fastai.vision import open_image
from flask_cors import CORS,cross_origin

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
      return render_template("index.html", uploadedImagePath = fullPath)

  return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))

# load the learner
learn = load_learner(path='./models', file='fauvismUkiyoE.pkl')
classes = learn.data.classes

# makre prediction and load into json
def predict_single(img_file):
    # function to take image and return prediction
    prediction = learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    return {
        'category': classes[prediction[1].item()],
        'probs': {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)}
    }

# route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    print("hello")
    return jsonify(predict_single(request.files['image']))