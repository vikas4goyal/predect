from flask import Flask, render_template, request, flash, redirect, url_for
from main import detect
from path import Path
from PIL import Image
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

WIDTH = 1000
HEIGHT = 800
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def predict_placement():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and text detected below')
        path = Path(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        detected_str = detect(path)
        return render_template('index.html', result=detected_str[0], filename=filename)
        # return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
