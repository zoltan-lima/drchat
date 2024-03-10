# Initialise the app here.
from flask import Flask, request, jsonify

app = Flask(__name__)

from setup import database
with app.app_context():
	database.db.create_all()

from setup import routes