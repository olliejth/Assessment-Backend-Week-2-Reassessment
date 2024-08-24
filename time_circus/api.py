"""An API for a time travelling circus troop"""

"""
TODO: Add specific error messaging and test it
TODO: TOCHAR() -> strptime?
"""


from datetime import datetime
from flask import Flask, request
import psycopg2
from database_functions import get_connection, get_cursor, make_performer_string, is_valid_sort, is_valid_order, get_venues_str, add_new_venue, add_new_performance
from database_functions import get_performances_str, get_performance_by_id_str, get_performers_by_specialty_str, get_max_id, get_venue_mapping, add_new_ppa_assignments
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
    sort = request.args.get("sort")
    order = request.args.get("order")

    cur = get_cursor(conn)

    if not sort:
        sort = 'birth_year'
    if not order:
        order = 'descending'

    if not is_valid_sort(sort):
        return {'error': True, "message": f'{sort} is an invalid sort parameter.'}
    if not is_valid_order(order):
        return {"error": True, "message": f'{order} is an invalid order parameter.'}

    query_str = make_performer_string(sort, order)

    cur.execute(query_str)
    results = cur.fetchall()
    cur.close

    return results, 200


@app.route('/venues', methods=["GET"])
def venues():

    cur = get_cursor(conn)

    query_str = get_venues_str()

    cur.execute(query_str)

    venue_result = cur.fetchall()

    return venue_result, 200


@app.route('/performances', methods=['GET', 'POST'])
def performances():
    if request.method == 'GET':
        cur = get_cursor(conn)

        query_str = get_performances_str()

        cur.execute(query_str)

        performances_result = cur.fetchall()

        return performances_result, 200

    elif request.method == 'POST':
        data = request.json

        if not "performer_id" in data or not "performance_date" in data or not "venue_name" in data or not "review_score" in data.keys():
            return {"error": True, "message": "Invalid data provided."}, 400

        if len(data.keys()) > 4:
            return {"error": True, "message": "Invalid data provided1."}, 400

        performer_id = data["performer_id"]
        performance_date = data["performance_date"]
        venue_name = data["venue_name"]
        review_score = data["review_score"]

        if not all((isinstance(performer_id, list),
                    isinstance(performance_date, str),
                    isinstance(venue_name, str),
                    isinstance(review_score, int))):
            return {"error": True, "message": "One or more data types invalid"}, 400

        max_performance_id = get_max_id(conn, 'performance', 'performance_id')
        max_ppa_id = get_max_id(conn,
                                'performance_performer_assignment',
                                'performance_performer_assignment_id')

        new_performance_id = max_performance_id + 1
        new_ppa_id = max_ppa_id + 1

        venue_mapping = get_venue_mapping(conn)
        if venue_mapping.get(venue_name):
            new_venue_id = venue_mapping[venue_name]
        else:
            max_venue_id = get_max_id(conn, 'venue', 'venue_id')
            new_venue_id = max_venue_id + 1
            add_new_venue(conn, new_venue_id, venue_name)

        add_new_performance(conn, new_performance_id,
                            performance_date, new_venue_id, review_score)

        add_new_ppa_assignments(
            conn, new_ppa_id, performer_id, new_performance_id)

        conn.commit()

        result_dict = {
            "performance_id": new_performance_id,
            "venue_id": new_venue_id,
            "performance_date": performance_date,
            "review_score": review_score
        }

        return {"message": f'New performance added: {result_dict}'}, 201


@app.route('/performances/<int:performance_id>', methods=['GET'])
def performance_by_id(performance_id):
    cur = get_cursor(conn)

    query_str = get_performance_by_id_str()

    cur.execute(query_str, (performance_id,))

    single_performance_results = cur.fetchone()

    if single_performance_results:
        return single_performance_results, 200
    else:
        return {"error": True, "message": f"No performance with an ID of {performance_id}"}, 404


@app.route('/performer_specialty', methods=['GET'])
def performer_specialty():

    cur = get_cursor(conn)

    query_str = get_performers_by_specialty_str()

    cur.execute(query_str)

    specialty_results = cur.fetchall()

    return specialty_results, 200


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

    # conn.close()
