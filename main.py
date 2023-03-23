from flask import Flask, request, jsonify
from pymongo import MongoClient
import sqlite3
import pandas as pd

# Creation of a Flask app
app = Flask(__name__)

# Run the Flask app in development mode
if __name__ == "__main__":
    app.run(debug=True)
