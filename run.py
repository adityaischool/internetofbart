#!flask/bin/python
from bart import app
from bart import views
from os import environ
app.config['Callback'] = 'http://localhost:5000/oauth2callback'
app.run(host='0.0.0.0', debug = True)
# app.run(port=int(environ['FLASK_PORT']))