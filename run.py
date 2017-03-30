from flask import Flask, render_template, request, redirect, flash, url_for
import os

from flask import send_file

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
    start = 0
    end = -1

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
        result = ocgen.main(os.path.join(app.config['UPLOAD_FOLDER'], filename), start, end, request.form['ocarina-holes'])
        print(str(result))
        return get_result(result)
    return index()


def get_result(result):
    if result is None: return send_file('/home/roan/Diss/ocgen/app/static/result.png')
    else: return render_template('index.html', error=result)


