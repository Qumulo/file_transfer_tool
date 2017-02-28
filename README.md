# Qumulo File Transfer Tool (FTT) 

Licensed under the Educational Community License, Version 2.0 (ECL-2.0) (the "License"); 
you may not use this file except in compliance with the License.  Please refer to LICENSE
file as part of this project for details.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.

## Requirements

* Qumulo cluster and API credentials for the cluster
* Linux or Mac with continuous access to the Qumulo cluster
* python
* python libraries: flask, argparse, sqlite
* Qumulo API python library
* Email smtp server or google apps credentials


## Installation Steps

### 1. Install the File Transfer Tool
```shell
git clone https://github.com/Qumulo/file_transfer_tool.git
```
Or, download the zip file (https://github.com/Qumulo/file_transfer_tool/archive/master.zip) and unzip it to your machine where you will be running this tool.



### 2. Install Prerequisites

We currently support Linux or MacOSX for running the File Transfer Tool.

You will need Python 2.7 and pip in order to install dependencies for the FTT.

NOTE that we strongly recommend using python virtual environments to isolate the libaries used
for this and other python applications from your system versions of python and libraries.  If
you are unfamiliar with the use of virtual environments, please have a look at this Qumulo Community 
article that we created on the subject:

https://community.qumulo.com/qumulo/topics/virtual-environments-when-using-qumulo-rest-api

A virtual environment for this app and python is not a requirement but it is a best practice.



### 3. Install the prerequisite python libraries

From a terminal window, `cd` to the folder where you cloned/installed file_transfer_tool and then run

```
pip install -r requirements.txt
```

to install the python prerequisites including the SQLite database and the Qumulo REST API
wrapper.  *NOTE* that the FTT sample requires Qumulo REST API version 1.2.15 or later.  You can 
potentially use FTT with Qumulo Core versions earlier than 1.2.15 but we have not tested earlier versions.  

As always, you'll want to be sure that the version of Qumulo REST API specified in `requirements.txt' matches
your Qumulo Cluster version.

#### Flask Plugins
FTT uses the [Flask web development framework](http://flask.pocoo.org/) to handle http requests and a number
of Flask plugins:

[Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) for styling/theming using Twitter Bootstrap

[Flask-SqlAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) for local SqLite DB

[Flask-Mail](https://pythonhosted.org/Flask-Mail/) for email integration

[Flask-Uploads](#) for file upload support


and more.  See ```requirements.txt``` file for all Python/Flask dependencies.



### 4. Set up the configuration file
There are a number of settings you'll need to set up in `config.py` before you can run the 
FTT server. Specifically look at the following settings:

```
# The locally mounted path of the uploads folder. 
# Must be mounted to a qumulo cluster.
UPLOADS_FOLDER = '<locally-mounted-upload-path>'

# The full path of the uploads folder on the Qumulo cluster
CLUSTER_FOLDER = os.environ.get('FTT_CLUSTER_FOLDER') or '<cluster-upload-path>'

# Qumulo api host, user, and password
CLUSTER = os.environ.get('FTT_CLUSTER') or '<cluster-host-name>'
CLUSTER_USER = os.environ.get('FTT_CLUSTER_USER') or '<cluster-api-user>'
CLUSTER_PWD = os.environ.get('FTT_CLUSTER_PWD') or '<cluster-api-password>'
```

*NOTE* Don't forget to `source` your shell script, restart a new session or otherwise pick up settings 
such as `FTT_CLUSTER_FOLDER` after you change them; Typically you'll need to restart the application
after making any config changes.



### 5. Create local Sql database for users and logging
FTT uses SqLite and [Flask-Migrate](https://flask-migrate.readthedocs.org/en/latest/) to store user sessions, user names and upload activity.  You'll need to
initialize SqlLite before the app can run, as described in the flask-migate docs:

From a terminal prompt, change folder to directory where you've installed FTT and run the 
following commands:

    ./manage.py db init
    ./manage.py db migrate
    ./manage.py db upgrade

If you run into problems, try

```
./manage.py db --help
```



### 6. Supporting multiple users

The [guidance](http://flask.pocoo.org/docs/0.10/deploying/#deployment) from the developers of Flask is that
you should not deploy your app into production using Flask's built-in webserver; Specifically: 
they say:

    "You can use the builtin server during development, but you should use a full deployment option for production applications. (Do not use the builtin development server in production.)"
    
So for production scenarios you should consider using [uWSGI](http://flask.pocoo.org/docs/0.10/deploying/uwsgi/)
with ngnx or perhaps [mod_wsgi](http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/) for Apache environments, or
another option. For simplicity's sake (easy to get up and running) I'm using [Gunicorn](http://docs.gunicorn.org/en/19.3/),
 which is another WSGI server.  Starting and running using `gunicorn` is simple:
 
     gunicorn -b 0.0.0.0:8000 -w 4 --threads 4 -t 360 --access-logfile ~/ftt_log.txt manage:app
     
will start the server with four workers with four threads per worker at port 8000.

If you want to go uWSGI/nginx route, a good 'how to' document for ubuntu can be found [here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04).

Short of creating a WSGI-based deployment, you can run FTT in non-developer/debug mode and support simultaneous users, you 
should start the server using the following form/command (from http://goo.gl/A3YfNt):

```./manage.py runserver --host 0.0.0.0 --threaded```

or

```./manage.py runserver --host 0.0.0.0 --processes=[n]```

where

```[n]```  is some integer value such as 3,10 etc.  

using ```--host 0.0.0.0``` makes the host visible to other machines.



### 7. Associating a project folder with a user
Users can be associated with a specific upload folder.  When this feature is used the user's "root"
for FTT is the specified folder relative to FTT_CLUSTER_FOLDER.

You can enable this feature for users in two ways:

1. Provide user with a sign-up link that specifies the project folder as a parameter:

http://localhost:5000/auth/register?starting_folder=research1

2. Edit sqlite user database and enter a value in starting_folder field.

** NOTE ** that the folder has to exist relative to FTT_CLUSTER_FOLDER on your Qumulo cluster prior to referencing
in FTT.

Users without a specified project folder will see all files in FTT_CLUSTER_FOLDER.
