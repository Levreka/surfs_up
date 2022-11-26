#inside of VSCode in order to run flask
#hit ctrl+shift+p it will take you to searh type python: select interpreter 
# select your conda envioroment pythondata base

#import flask 
from flask import Flask
#create an app and assing variable name to app
app = Flask(__name__)
#define our starting point by setting our root using '/'
#This denotes that we want to put our data at the root of our routes. 
@app.route('/')
#create hello world function within our @app.route('/')
def hello_world():
    return 'Hello world'

#run the app in your anaconda envioroment and navigate to your folder
#where app is located type the following code: windows only
#set FLASK_APP=app_practice.py
#mac only: export export FLASK_APP=app.py

#run the application 
#Note: this is done still in your conda envioroment
#code: flask run
#copy and paste the http adress to web browser to see result

