from flask import Flask


UPLOAD_FOLDER = 'static/uploads/'
SECRET_KEY = 'secret key'

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
