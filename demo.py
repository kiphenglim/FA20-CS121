from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/index")

def index():
    return "Hello, cs121 World!"
