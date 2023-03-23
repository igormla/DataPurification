from flask import Flask, request, jsonify
from pymongo import MongoClient
import sqlite3
import pandas as pd

# Creation of a Flask app
app = Flask(__name__)


@app.route("/companies", methods=["GET"])
def read_companies():
    """
    Reads data from the `"companies"` table of a SQLite database.
    The data afterwards is converted to a Pandas DataFrame.
    Finally, the data is processed using the ``process_data()`` method of
    the ``TransformData`` utility class, which is used for reordering the data.

    Returns a json version of the processed data.
    """
    # Read the "companies" table from the SQLite database
    db_path = "data.db"
    sqlite_db = sqlite3.connect(db_path)
    sql_query = "SELECT * FROM companies"

    # Convert the data to a Pandas DataFrame and process (reorder) it
    data = pd.read_sql(sql_query, sqlite_db).fillna("")
    data = TransformData.process_data(data, "name")

    # Close the opened SQLite database
    sqlite_db.close()

    # Return a json version of the process data
    return jsonify(data)


# Run the Flask app in development mode
if __name__ == "__main__":
    app.run(debug=True)
