#inside of VSCode in order to run flask
#hit ctrl+shift+p it will take you to searh type python: select interpreter 
# select your conda envioroment pythondata base

#import flask 
from flask import Flask
#create an app and assing variable name to app
app = Flask(__name__)
#define our starting point by setting our root using '/'
#
@app.route('/')

def hello_world():
    return 'Hello world'

#

