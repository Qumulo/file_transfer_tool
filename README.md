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

### 2. Install Prequisites

We currently support Linux or MacOSX for running the File Transfer Tool.

You will need Python 2.7 and pip in order to install dependencies for the FTT.

NOTE that we strongly recommend using python virtual environments to isolate the libaries used
for this and other python applications from your system versions of python and libraries.  If
you are unfamiliar with the use of virtual environments, please have a look at this Qumulo Community 
article that we created on the subject:

https://community.qumulo.com/qumulo/topics/virtual-environments-when-using-qumulo-rest-api

A virtual environment for this app and python is not a requirement but it is a best practice.


```

### 3. Install the prerequisite python libraries

Just run

```shell
pip install -r requirements.txt
```

to install the python prerequisites including the SQLite database and the Qumulo REST API
wrapper.  *NOTE* that the FTT sample requires Qumulo REST API version 1.2.15 or later.  You can 
potentially use FTT with Qumulo Core versions earlier than 1.2.15 but we have not tested earlier versions.  

As always, you'll want to be sure that the version of Qumulo REST API specified in `requirements.txt' matches
your Qumulo Cluster version.

### 4. Set up the configuration file
Edit *config.json*
1. Add your Qumulo cluster information and credentials as well as the email credentials/server. There are descriptions of all required properties. All settings are required, so make sure to replace all the values in the <> brackets. 

