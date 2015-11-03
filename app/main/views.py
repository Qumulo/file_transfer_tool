from . import main
import json
import os
from flask import current_app, Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename

import qumulo.lib.request
import qumulo.rest.fs as fs
import qumulo.lib.auth

def create_json_list(path, directories):

    children = []

    for directory in directories:

        d = { "title": directory, \
           "expanded" : False, \
           "folder" : True, \
           "lazy" : True }
        children.append(d)

    if path == '/':
        result = [ { "title": path, \
                   "expanded" : True, \
                   "folder" : True, \
                   "children" : children } ]
    else:
        result = children

    return json.dumps(result)


def get_directories(path):
    ''' return JSON tree of all directories on cluster starting at path '''

    host = current_app.config['CLUSTER']
    user = current_app.config['CLUSTER_USER']
    passwd = current_app.config['CLUSTER_PWD']
    port = current_app.config['PORT']

    try:
        connection = qumulo.lib.request.Connection(\
                            host, port)
        login_results, _ = qumulo.rest.auth.login(\
                connection, None, user, passwd)

        credentials = qumulo.lib.auth.Credentials.\
                from_login_response(login_results)

    except Exception, excpt:
        print "Error connecting to the REST server: %s" % excpt
        print __doc__
        # TODO: Raise error
        return False

    directories = []
    for response in fs.read_entire_directory(connection, credentials, 5000, path):
        directories = directories + [f['name'] for f in response.data['files'] if f['type'] == 'FS_FILE_TYPE_DIRECTORY']

    return create_json_list(path, directories)


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


    path = request.args.get('path')
    if path is None:
        path = '/'


    # if a cluster folder has been specified, prefix everything with that folder
    folder = current_app.config['CLUSTER_FOLDER']
    if folder is not None:
        path = folder + path
        
    json_result = get_directories(path)
    return json_result
    
    # return '''
    # [
    #     {"title": "Animalia", "expanded": true, "folder": true, "children": [
    #         {"title": "Chordate", "folder": true, "children": [
    #             {"title": "Mammal", "children": [
    #                 {"title": "Primate", "children": [
    #                     {"title": "Primate", "children": [
    #                     ]},
    #                     {"title": "Carnivora", "children": [
    #                     ]}
    #                 ]},
    #                 {"title": "Carnivora", "children": [
    #                     {"title": "Felidae", "lazy": true}
    #                 ]}
    #             ]}
    #         ]},
    #         {"title": "Arthropoda", "expanded": true, "folder": true, "children": [
    #             {"title": "Insect", "children": [
    #                 {"title": "Diptera", "lazy": true}
    #             ]}
    #         ]}
    #     ]}
    # ]
    # '''


