"""An API for a time travelling circus troop"""

from flask import Flask, request

import database_functions as f

app = Flask(__name__)

# pylint: disable=R0914, R1705, R1710

"""
For testing reasons; please ALWAYS use this connection.
- Do not make another connection in your code
- Do not close this connection
"""

conn = f.get_connection("time_circus")
tc_logger = f.get_logger()
f.configure_logging('time_circus_log.log')


@app.route("/")
def home_page():
    """Returns API homepage and welcome message."""
    s = """<h1>Time Travelling Circus API</h1><h2>Delighting
     you any time, anywhere, any universe</h2>"""
    return s, 200


@app.route('/performers', methods=['GET'])
def performers():
    """Returns list of performers with sort nd order options."""
    sort = request.args.get("sort")
    order = request.args.get("order")

    cur = f.get_cursor(conn)

    if not sort:
        sort = 'birth_year'
    if not order:
        order = 'descending'

    if not f.is_valid_sort(sort):
        return {'error': True, "message": f'{sort} is an invalid sort parameter.'}
    if not f.is_valid_order(order):
        return {"error": True, "message": f'{order} is an invalid order parameter.'}

    query_str = f.make_performer_string(sort, order)

    cur.execute(query_str)
    results = cur.fetchall()
    cur.close()

    return results, 200


@app.route('/venues', methods=["GET"])
def venues():
    """Returns time circus venue names and IDs."""

    cur = f.get_cursor(conn)

    query_str = f.get_venues_str()

    cur.execute(query_str)

    venue_result = cur.fetchall()

    return venue_result, 200


@app.route('/performances', methods=['GET', 'POST'])
def performances():
    """
    Returns list of performances and performers
    or is used to add new performance data
    """
    if request.method == 'GET':
        cur = f.get_cursor(conn)

        query_str = f.get_performances_str()

        cur.execute(query_str)

        performances_result = cur.fetchall()

        cur.close()

        return performances_result, 200

    elif request.method == 'POST':
        data = request.json

        required_keys = ("performer_id", "performance_date",
                         "venue_name", "review_score")
        for k in required_keys:
            if k not in data.keys():
                return {"error": True, "message": "Invalid data provided1."}, 400

        if len(data.keys()) > len(required_keys):
            return {"error": True, "message": "Invalid data provided2."}, 400

        performer_id = data["performer_id"]
        performance_date = data["performance_date"]
        venue_name = data["venue_name"]
        review_score = data["review_score"]

        if not all((isinstance(performer_id, list),
                    isinstance(performance_date, str),
                    isinstance(venue_name, str),
                    isinstance(review_score, int))):
            return {"error": True, "message": "One or more data types invalid"}, 400

        max_performance_id = f.get_max_id(
            conn, 'performance', 'performance_id')
        max_ppa_id = f.get_max_id(conn,
                                  'performance_performer_assignment',
                                  'performance_performer_assignment_id')

        new_performance_id = max_performance_id + 1
        new_ppa_id = max_ppa_id + 1

        venue_mapping = f.get_venue_mapping(conn)
        if venue_mapping.get(venue_name):
            new_venue_id = venue_mapping[venue_name]
        else:
            return {"error": True, "message": "Invalid venue name."}, 404
            ## CODE TO ADD NEW VENUE NAME ##
            # max_venue_id = get_max_id(conn, 'venue', 'venue_id')
            # new_venue_id = max_venue_id + 1
            # add_new_venue(conn, new_venue_id, venue_name)

        f.add_new_performance(conn, new_performance_id,
                              performance_date, new_venue_id, review_score)

        f.add_new_ppa_assignments(
            conn, new_ppa_id, performer_id, new_performance_id)

        conn.commit()

        result_dict = {
            "performance_id": new_performance_id,
            "venue_id": new_venue_id,
            "performance_date": performance_date,
            "review_score": review_score
        }

        f.log_message(tc_logger, f'New performance added: {result_dict}')

        return {"message": f'New performance added: {result_dict}'}, 200


@app.route('/performances/<int:performance_id>', methods=['GET'])
def performance_by_id(performance_id):
    """Returns a single performance with a matching ID."""

    cur = f.get_cursor(conn)

    query_str = f.get_performance_by_id_str()

    cur.execute(query_str, (performance_id,))

    single_performance_results = cur.fetchone()

    if single_performance_results:
        return single_performance_results, 200

    return {"error": True, "message": f"No performance with an ID of {performance_id}"}, 404


@app.route('/performer_specialty', methods=['GET'])
def performer_specialty():
    """Returns list of specialties and corresponding performers."""

    cur = f.get_cursor(conn)

    query_str = f.get_performers_by_specialty_str()

    cur.execute(query_str)

    specialty_results = cur.fetchall()

    return specialty_results, 200


@app.route('/performers/summary', methods=['GET'])
def performers_summary():
    """Returns performers with total performances and average review score."""

    output_list = f.get_average_performer_scores(conn)

    return output_list, 200


if __name__ == "__main__":

    try:
        app.config["DEBUG"] = True
        app.config["TESTING"] = True
        app.run(port=8000)
    finally:
        conn.close()
        print("Connection closed")
