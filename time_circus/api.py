"""An API for a time travelling circus troop"""

"""
TODO: Add specific error messaging and test it
TODO: TOCHAR() -> strptime?
"""


from datetime import datetime
from flask import Flask, request
import psycopg2
from database_functions import get_connection, get_cursor
app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection.
- Do not make another connection in your code
- Do not close this connection
"""
conn = get_connection("time_circus")


@app.route("/")
def home_page():
    return "<h1>Time Travelling Circus API</h1><h2>Delighting you any time, anywhere, any universe</h2>", 200


@app.route('/performers', methods=['GET'])
def performers():
    pass


@app.route('/venues', methods=["GET"])
def venues():
    pass


@app.route('/performances', methods=['GET', 'POST'])
def performances():
    pass


@app.route('/performances/<int:performance_id>', methods=['GET'])
def performance_by_id(performance_id):
    pass


@app.route('/performer_specialty', methods=['GET'])
def performer_specialty():
    """
    A poorly made, inefficient API route method

    A GET request to the /performers_by_specialty endpoint should return a list of specialties
    each with the performers in that specialty.
    Each specialty should contain the following information:
    - Specialty ID
    - Specialty Name
    - Performers(list of performer names)
    """
    query = """
    SELECT s.specialty_id, s.specialty_name, p.stagename,
    FROM specialty s, performer as p
    WHERE s.specialty_id = p.specialty_id
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        specialties = {}
        for row in results:
            specialty_id = row['specialty_id']
            specialty_name = row['specialty_name']
            performer_name = f"{row['performer_firstname']} {
                row['performer_surname']}"

            if specialty_id not in specialties:
                specialties[specialty_id] = {
                    "specialty_id": specialty_id,
                    "specialty_name": specialty_name,
                    "performers": []
                }
            specialties[specialty_id]["performers"].append(performer_name)

        return list(specialties.values()), 200
    except:
        return {"error": "Something went wrong"}, 500


@app.route('/performers/summary', methods=['GET'])
def performers_summary():
    pass


if __name__ == "__main__":
    try:
        app.config["DEBUG"] = True
        app.config["TESTING"] = True
        app.run(port=8000)
    finally:
        conn.close()
        print("Connection closed")
