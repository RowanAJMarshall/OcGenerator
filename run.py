import os
import sys

from flask import Flask, render_template, request, redirect, flash

from AudioConversion import convert
from Ocgen import ocgen
from Utils.file_utilities import get_file_extension, generate_filename, FileNotRecognisedError

app = Flask(__name__)
app.secret_key = "42"
app.config['DEBUG'] = True
UPLOAD_FOLDER = './uploads/'


# Main transcription function
@app.route("/api/transcript", methods=["POST"])
def upload_file():

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    start = 0
    end = sys.maxsize
    pitch_algorithm = "yin"
    shifting = False

    if "upload" not in request.files:
        print("File not in there")
        flash("No file part")
        return redirect(request.url)

    if request.form['start']: start = int(request.form['start'])
    if request.form['end']: end = int(request.form['end'])
    if request.form['pitch-algorithm']: pitch_algorithm = request.form['pitch-algorithm']
    if request.form['shifting']: shifting = request.form['shifting']

    if start > end:
        return throw_error("Please ensure the start time is before the end time.", "index.html")

    file = request.files['upload']
    if file:
        try:
            new_filename = generate_filename(file.filename) + "." + get_file_extension(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            err, result = ocgen.main(os.path.join(app.config['UPLOAD_FOLDER'], new_filename), start, end,
                                     request.form['instrument'], pitch_algorithm, shifting)
            return get_result(err, result)
        except FileNotFoundError as e:
            return get_result(e.args, None)
    return index()


# Main format conversion function
@app.route("/api/audioconversion", methods=["POST"])
def start_audio_conversion():
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print("Files: " + str(request.files))

    if "upload" not in request.files and "recording" not in request.files:
        flash("No file part")
        return redirect(request.url)

    try:
        file = request.files['upload']
    except KeyError:
        file = request.files['recording']

    if file:
        try:
            new_filename = generate_filename(file.filename) + "." + get_file_extension(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            target_format = request.form['target-format']
            result = convert.convert(os.path.join(app.config['UPLOAD_FOLDER'], new_filename), target_format)

            return render_template('audioconversion.html', converted_file=result, format=get_file_extension(result))
        except FileNotRecognisedError as e:
            return throw_error(e.args[0], "audioconversion.html")
    return render_template('audioconversion.html')


# PDF Manual page
@app.route('/manual.html', methods=["GET"])
def manual():
    return app.send_static_file('manual.pdf')


# Audio format converter page
@app.route('/audioconversion', methods=['GET'])
def audioconversion():
    return render_template('audioconversion.html')


# Application homepage
@app.route('/index.html')
def index():
    return render_template("index.html")


# Metronome webpage
@app.route('/metronome')
def metronome():
    return render_template("metronome.html")


def throw_error(err, page):
    return render_template(page, error=err)


def get_result(err, img):
    if err is None:
        print(img)
        return render_template('result.html',
                               path=img)
    else:
        return render_template('index.html', error=err)
