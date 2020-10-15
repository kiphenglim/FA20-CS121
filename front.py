import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
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
      return render_template("index.html", uploadedImagePath = fullPath)
    else:
      flash('Please select a file with a .png, .jpg, .jpeg, or .gif extension')
  return render_template("index.html",uploadedImagePath = os.path.join('static', "uploadPH.jpg"))
