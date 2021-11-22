# Note: Using Git Bash to run website and Anaconda to run jupyter notebook
# Could not get this to work with VSCode terminal.

# open command prompt to update flask (both git bash and anaconda, not sure if it mattered)
# pip install flask

# inside of VSCode
# update workspace (left side) to new folder surfs up, removed older workspaces
# ctrl+shift+p python: select interpreter 
# select surfs up folder, check using PythonData env
# write code
from flask import Flask
app = Flask(__name__)
@app.route('/')

def hello_world():
    return 'Hello world'

#Skill Drill9.4.3:
def star_trek():
    return 'Welcome to the Collective!'

# Back to the command prompt(git bash), run flask to get host website
# export FLASK_APP=app.py
# set FLASK_APP=app.py
# flask run

# get host website from command prompt
# then paste into Google Chrome to see Flask run

# Skill Drill 9.4.3
# can use ctrl+C in the command prompt to quit running flask
# made changes to VScode 
# back to command prompt
# only need to use flask run again to see the updated changes on the webiste
# might need to refresh website to see the effect of the changed VSCode

