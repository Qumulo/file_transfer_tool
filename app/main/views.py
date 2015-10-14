from . import main
import os
from flask import current_app, Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.realpath('.') + '/app/static/uploads/'

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload-target', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOADS_FOLDER'], filename))
            # return redirect('/')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


