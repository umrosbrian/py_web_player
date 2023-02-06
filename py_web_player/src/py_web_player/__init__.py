from flask import Flask
from turbo_flask import Turbo
app = Flask(__name__, template_folder='templates')
# https://blog.miguelgrinberg.com/post/dynamically-update-your-flask-web-pages-using-turbo-flask indicates that a \
# Turbo class should be instantiated immediately after Flask().  I think this will start asynchrounous activity \
# before any connections are made to the app.
turbo = Turbo(app)
from py_web_player import routes