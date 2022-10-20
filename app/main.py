import os
from app import app
from flask import flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
import pandas as pd
from datetime import datetime


CONTRACTS = ['Electricity', 'Gas', 'Water']

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MEASUREMENTS_PATH = '../measurements.csv'
DEVICES = {
    "eb680530-a698-45de-a445-8d8f9dc10b4e": "Kar39EGThermostat"
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_image_ai():
    if 'X-Device-Id' not in request.headers:
        return 'No X-Device-Id header present.', 400
    device_id = request.headers['X-Device-Id']

    if 'imageFile' not in request.files:
        return 'No file part', 400
    file = request.files['imageFile']
    if file.filename == '':
        return 'No image selected for uploading', 400
    if not (file and allowed_file(file.filename)):
        return 'Allowed image types are -> png, jpg, jpeg, gif', 400

    filename = secure_filename(file.filename)
    current_time = datetime.now()
    new_filename = str(current_time) + "." + filename.split(".", 1)[1]

    device_name = DEVICES[device_id]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'] + 'devices/' + device_name + "/photos/", new_filename)
    file.save(filepath)
    # img = Image.open(filepath)
    # exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}

    return "Successful upload", 200


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if not (file and allowed_file(file.filename)):
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)
    if 'measurement' not in request.form:
        flash('No measurement provided')
        return redirect(request.url)
    try:
        measurement = float(request.form['measurement'])
    except ValueError:
        flash('The provided measurement not a number')
        return redirect(request.url)

    if 'contract' not in request.form:
        flash('No contract provided')
        return redirect(request.url)

    contract = request.form['contract']
    if contract not in CONTRACTS:
        flash('The selected contract is not in the allowed contracts')
        return redirect(request.url)

    contract_name = ''
    measure_unit = ''
    if contract == 'Electricity':
        contract_name = 'StromKar39-22'
        measure_unit = 'kWh'
    if contract == 'Gas':
        contract_name = 'GasKar39-22'
        measure_unit = 'm3'

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = Image.open(filepath)
    exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}

    created_time = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')

    measurements_df = pd.read_csv(MEASUREMENTS_PATH)

    measurements_df = measurements_df.append({
        'aggregate_consumption': measurement,
        "date": created_time,
        "measure_unit": measure_unit,
        'contract': contract_name,
        'photo': filename
    }, ignore_index=True)

    measurements_df.to_csv(MEASUREMENTS_PATH, index=False)

    os.system('git add .')
    os.system(f"git commit -m 'New {contract} measurement for {contract_name} on {created_time}'")
    os.system('git push')

    flash('Measurement submitted successfully')
    # return render_template('upload.html', filename=filename)
    return render_template('upload.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
