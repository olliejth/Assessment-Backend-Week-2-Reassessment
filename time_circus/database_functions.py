"""Functions for the time_circus API routes."""

# pylint: disable=W0621

import logging
from datetime import datetime

from psycopg2 import connect, extras
from psycopg2.extensions import cursor, connection
from psycopg2.extras import RealDictCursor


def get_connection(dbname, password="postgres") -> connection:
    """Creates database connection."""
    return connect(
        dbname=dbname,
        host="localhost",
        port=5432,
        password=password,
        cursor_factory=RealDictCursor)


def get_cursor(connection: connection) -> cursor:
    """Creates connection cursor."""
    return connection.cursor()


def get_logger() -> logging.Logger:
    """Retrieves logger."""
    return logging.getLogger("museum_logger_week7")


def configure_logging(destination_file_name) -> None:
    """Configures logging objects."""
    logging.basicConfig(filename=destination_file_name,
                        encoding='utf-8', level=logging.INFO)


def log_message(logger: logging.Logger, message: str):
    """Filters and formats logging messages."""
    message = f' [{datetime.now()}] -> {message}'
    logger.info(message)


def is_valid_sort(sort_param: str) -> bool:
    """Checks that provided sort parameter is valid."""
    if sort_param.lower() not in ('birth_year', 'specialty', 'performer_name'):
        return False
    return True


def is_valid_order(order_param: str) -> bool:
    """Checks that provided order parameter is valid."""
    if order_param.lower() not in ('ascending', 'descending'):
        return False
    return True


def make_performer_string(sort: str, order: str) -> list[dict]:
    """Creates the query string for the performer route."""

    q = """
SELECT P.performer_id AS performer_id, 
P.performer_stagename AS performer_name, 
CAST(EXTRACT(YEAR FROM P.performer_dob) AS INT) AS birth_year, 
S.specialty_name AS specialty_name
FROM performer AS P
JOIN specialty AS S
ON S.specialty_id = P.specialty_id"""

    sort_q = f" ORDER BY {sort}"

    if order.lower() == 'ascending':
        order_q = " ASC"
    else:
        order_q = " DESC"

    return q + sort_q + order_q


def get_venues_str() -> str:
    """Creates the query string for the venues route."""

    q = """
SELECT venue_id, venue_name
FROM venue
"""
    return q


def get_performances_str() -> str:
    """Creates the query string for the performances route."""

    q = """
SELECT PE.performance_id, 
PR.performer_stagename AS performer_name, 
TO_CHAR(PE.performance_date, 'YYYY-MM-DD') AS performance_date, 
V.venue_name, 
PE.review_score AS score
FROM performance_performer_assignment AS PPA

JOIN performance AS PE
ON PPA.performance_id = PE.performance_id

JOIN performer AS PR
ON PPA.performer_id = PR.performer_id

JOIN venue AS V
ON V.venue_id = PE.venue_id
ORDER BY performance_date DESC"""

    return q


def get_performance_by_id_str() -> str:
    """Creates the query string for the performance by ID route."""

    q = """
SELECT PE.performance_id, 
ARRAY_AGG(PR.performer_stagename) AS performer_names, 
MAX(V.venue_name) AS venue_name,
MAX(TO_CHAR(PE.performance_date, 'YYYY-MM-DD')) AS performance_date, 
MAX(PE.review_score) AS review_score
FROM performance_performer_assignment AS PPA

JOIN performance AS PE
ON PPA.performance_id = PE.performance_id

JOIN performer AS PR
ON PPA.performer_id = PR.performer_id

JOIN venue AS V
ON V.venue_id = PE.venue_id

WHERE PE.performance_id = %s
GROUP BY PE.performance_id
ORDER BY PE.performance_id"""

    return q


def get_performers_by_specialty_str() -> str:
    """Creates the query string for the performers by specialty route."""

    q = """
SELECT S.specialty_id,
MAX(S.specialty_name) AS specialty_name,
ARRAY_AGG(P.performer_stagename) AS performer_names
FROM specialty AS S
JOIN performer AS P
ON S.specialty_id = P.specialty_id

GROUP BY S.specialty_id
ORDER BY S.specialty_id"""

    return q


def get_max_id(connection: connection, table_name: str, col_name: str) -> int:
    """Obtains and returns max ID from existing table"""

    cur = connection.cursor()
    q1 = f"""
SELECT {col_name}
FROM {table_name}
ORDER BY {col_name} DESC
LIMIT 1"""

    cur.execute(q1)

    new_id_obj = cur.fetchone()

    cur.close()

    return new_id_obj[f"{col_name}"]


def get_venue_str() -> str:
    """Creates the query string for the venue route."""

    q = """
    INSERT INTO venue (venue_id, venue_name)
    VALUES
    (%s, %s)
    RETURNING venue_id
    """
    return q


def get_venue_mapping(connection: connection) -> dict:
    """Creates venue mapping dictionary of valid venue names/IDs."""

    cur = connection.cursor()

    q = """SELECT * FROM venue"""

    cur.execute(q)

    venue_table_list = cur.fetchall()

    venue_mapping_dict = {}
    for v in venue_table_list:
        venue_mapping_dict[v["venue_name"]] = v["venue_id"]

    cur.close()

    return venue_mapping_dict


def add_new_venue(connection: connection, venue_id: int, venue_name: str) -> None:
    """Adds new venue entity to the database."""

    q = """
INSERT INTO venue (venue_id, venue_name)
VALUES (%s, %s)"""

    cur = connection.cursor()
    cur.execute(q, (venue_id, venue_name))
    connection.commit()
    cur.close()


def add_new_performance(connection: connection, perf_id: int,
                        perf_date: str, venue_id: int,
                        score: int) -> None:
    """Adds a new performance entity to the performance table."""

    q = """
INSERT INTO performance
(performance_id, venue_id, performance_date, review_score)
VALUES
(%s, %s, %s, %s)"""

    cur = connection.cursor()
    cur.execute(q, (perf_id, venue_id, perf_date, score))
    connection.commit()
    cur.close()


def add_new_ppa_assignments(connection: connection, ppa_id: int,
                            performer_ids: list[int],
                            performance_id: int) -> None:
    """Creates the query string for the performer route."""

    ppa_list = []
    for performer_id in performer_ids:
        ppa_list.append([ppa_id, performer_id, performance_id])
        ppa_id += 1

    q = """
INSERT INTO performance_performer_assignment
(performance_performer_assignment_id, performer_id, performance_id)
VALUES %s"""

    cur = connection.cursor()
    extras.execute_values(cur, q, ppa_list)
    connection.commit()
    cur.close()


def get_average_performer_scores(connection: connection) -> list[dict]:
    """Gets number of performances and average review scores per performer."""

    cur = connection.cursor()
    q = """
SELECT PR.performer_id AS performer_id,
MAX(PR.performer_stagename) AS performer_stagename, 
COUNT(*) AS total_performances, 
ROUND(AVG(PE.review_score), 1) AS average_review_score
FROM performer AS PR

JOIN performance_performer_assignment AS PPA
ON PR.performer_id = PPA.performer_id

JOIN performance AS PE
ON PPA.performance_id = PE.performance_id

GROUP BY PR.performer_id
ORDER BY total_performances DESC"""

    cur.execute(q)
    output_list = cur.fetchall()
    cur.close()
    return output_list
