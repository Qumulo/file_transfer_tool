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

    file = request.files['file']

    if file:

        fullPath = request.form['fullPath']
        filename = secure_filename(file.filename)
        saveFolder = os.path.join(current_app.config['UPLOADS_FOLDER']+ os.path.dirname(fullPath))

        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)

        file.save(os.path.join(saveFolder, filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@main.route('/get-cluster-data')
def get_cluster_data():

    return '''
    [
        {"title": "Animalia", "expanded": true, "folder": true, "children": [
            {"title": "Chordate", "folder": true, "children": [
                {"title": "Mammal", "children": [
                    {"title": "Primate", "children": [
                        {"title": "Primate", "children": [
                        ]},
                        {"title": "Carnivora", "children": [
                        ]}
                    ]},
                    {"title": "Carnivora", "children": [
                        {"title": "Felidae", "lazy": true}
                    ]}
                ]}
            ]},
            {"title": "Arthropoda", "expanded": true, "folder": true, "children": [
                {"title": "Insect", "children": [
                    {"title": "Diptera", "lazy": true}
                ]}
            ]}
        ]}
    ]
    '''


@main.route('/set-cluster-folder', methods=['POST'])
def set_cluster_folder():
    pass


