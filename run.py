from flask import Flask, render_template, request, redirect, flash, url_for
import os
from Ocgen import ocgen


app = Flask(__name__)
app.secret_key = "42"
app.config['DEBUG'] = True


@app.route('/', methods=["GET"])
def index(filename=None):
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    UPLOAD_FOLDER = './uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if "upload" not in request.files:
        print("File not in there")
        flash("No file part")
        return redirect(request.url)

    file = request.files['upload']
    start = request.form['start']
    end = request.form['end']
    print("Start " + str(start))
    print("End " + str(end))
    print(request.form)
    filename = file.filename

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ocgen.main(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("result.html")
    return index()

