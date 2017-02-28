from . import main
import errno
import json
import os
from flask import current_app, Flask, render_template, request, session, redirect, url_for
from werkzeug import secure_filename

import qumulo.lib.request
import qumulo.rest.fs as fs
import qumulo.lib.auth

def create_json_list(path, contents):

    children = []

    for c in contents:

        title = c[0]
        type = c[1]
        if type == 'FS_FILE_TYPE_DIRECTORY':
            folder = True
            lazy = True
        else:
            folder = False
            lazy = False

        d = { "title": c[0], \
           "expanded" : False, \
           "folder" : folder, \
           "lazy" : lazy }
        children.append(d)

    if path == '/':
        result = [ { "title": path, \
                   "expanded" : True, \
                   "folder" : True, \
                   "children" : children } ]
    else:
        result = children

    return json.dumps(result)


def get_contents(path):
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

    contents = []
    for response in fs.read_entire_directory(connection, credentials, 5000, path):
        contents = contents + [ (f['name'], f['type']) for f in response.data['files']]

    return create_json_list(path, contents)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/upload-target', methods=['POST'])
def upload_file():

    file = request.files['file']

    if file:

        fullPath = request.form['fullPath']
        filename = secure_filename(file.filename)

        # destPath = request.form['destPath']
        # import ipdb; ipdb.set_trace()
        # If the current user has a specified starting folder, tack that on to the path
        # also tack on destPath if provided as the 'root' for the upload

        starting_folder = session.get("starting_folder")
        base_path = current_app.config['UPLOADS_FOLDER']
        if starting_folder:
            base_path = base_path + starting_folder + "/"

        saveFolder = os.path.join(base_path + os.path.dirname(fullPath))

        if not os.path.exists(saveFolder):
           try:
               os.makedirs(saveFolder)
           except OSError as exc:
               if exc.errno == errno.EEXIST and os.path.isdir(saveFolder):
                   pass
               else:
                   raise

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

    path = '/'

    # if a cluster folder has been specified, prefix everything with that folder
    folder = current_app.config['CLUSTER_FOLDER']
    if folder is not None:
        path = folder
        # If the current user has a specified starting folder, tack that on to the path
        starting_folder = session.get("starting_folder")
        if starting_folder:
            path = path + starting_folder

    arg_path = request.args.get('path')
    if arg_path:
        path = path + arg_path

    json_result = get_contents(path)
    return json_result
