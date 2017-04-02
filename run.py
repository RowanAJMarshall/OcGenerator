import sys
from flask import Flask, render_template, request, redirect, flash, url_for
import os

from flask import send_file

from Ocgen import ocgen

app = Flask(__name__)
app.secret_key = "42"
app.config['DEBUG'] = True


@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    UPLOAD_FOLDER = './uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    start = 0
    end = sys.maxsize
    pitch_algorithm = "yin"

    if "upload" not in request.files:
        print("File not in there")
        flash("No file part")
        return redirect(request.url)

    if request.form['start']: start = int(request.form['start'])
    if request.form['end']: end = int(request.form['end'])
    if request.form['pitch-algorithm']: pitch_algorithm = request.form['pitch-algorithm']

    file = request.files['upload']

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        result = ocgen.main(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), start, end,
                            request.form['instrument'], pitch_algorithm)
        return get_result(result)
    return index()


def get_result(result):
    if result is None:
        return render_template('result.html')  # return send_file('/home/roan/Diss/ocgen/app/static/result.png')
    else:
        return render_template('index.html', error=result)
