""""""
import logging
from datetime import datetime

from psycopg2 import connect, extras
from psycopg2.extensions import cursor, connection
from psycopg2.extras import RealDictCursor


def get_connection(dbname, password="postgres") -> connection:
    return connect(
        dbname=dbname,
        host="localhost",
        port=5432,
        password=password,
        cursor_factory=RealDictCursor)


def get_cursor(connection: connection) -> cursor:
    return connection.cursor()


def get_logger() -> logging.Logger:
    """Retrieves logger."""
    return logging.getLogger("museum_logger_week7")


def configure_logging():
    """Configures logging objects."""
    logging.basicConfig(encoding='utf-8', level=logging.INFO)


def log_message(logger: logging.Logger, message: str):
    """Filters and formats logging messages."""
    message = f' [{datetime.now()}] -> {message}'
    level = level.lower()
    match level:
        case "info":
            logger.info(message)
        case "warning":
            logger.warning(message)
        case "debug":
            logger.debug(message)


def is_valid_sort(sort_param: str) -> bool:
    if sort_param.lower() not in ('birth_year', 'specialty_name', 'performer_name'):
        return False
    return True


def is_valid_order(order_param: str) -> bool:
    if order_param.lower() not in ('ascending', 'descending'):
        return False
    return True


def make_performer_string(sort: str, order: str) -> list[dict]:

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

    q = """
SELECT venue_id, venue_name
FROM venue
"""
    return q


def get_performances_str() -> str:
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
ORDER BY PE.performance_id"""

    return q


def get_performance_by_id_str() -> str:

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


def get_post_performance_str(json_data: dict) -> str:
    p_id = json_data["performer_id"]
    p_date = json_data["performance_date"]
    venue = json_data["venue_name"]
    score = json_data["review_score"]

    output_string =

    for i in p_id


p = """INSERT INTO rating_interaction
            (event_at, exhibition_id, rating_id)
        VALUES %s;
    """

extras.execute_values(cur, p, data)
# # thing that talks to the db, thing with one gap, list of things that can fill the gap
