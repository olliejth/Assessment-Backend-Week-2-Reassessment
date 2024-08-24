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
ORDER BY performance_date DESC"""

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


def get_max_id(connection: connection, table_name: str, col_name: str):

    cur = connection.cursor()
    q1 = f"""
SELECT {col_name}
FROM {table_name}
ORDER BY {col_name} DESC
LIMIT 1"""

    cur.execute(q1)

    new_id_obj = cur.fetchone()

    return new_id_obj[f"{col_name}"]


def get_venue_str() -> str:
    q = """
    INSERT INTO venue (venue_id, venue_name)
    VALUES
    (%s, %s)
    RETURNING venue_id
    """
    return q


def get_performance_post_str() -> str:
    q = """
    INSERT INTO performance (performance_id, venue_id, performance_date, review_score)
    VALUES (%s, %s, %s, %s)
    RETURNING performance_id
    """


def get_venue_mapping(connection):

    cur = connection.cursor()

    q = """SELECT * FROM venue"""

    cur.execute(q)

    venue_table_list = cur.fetchall()

    venue_mapping_dict = {}
    for v in venue_table_list:
        venue_mapping_dict[v["venue_name"]] = v["venue_id"]

    return venue_mapping_dict


def add_new_venue(connection, venue_id, venue_name):
    q = """
INSERT INTO venue (venue_id, venue_name)
VALUES (%s, %s)"""

    cur = connection.cursor()
    cur.execute(q, (venue_id, venue_name))
    connection.commit()


def add_new_performance(connection, perf_id, perf_date, venue_id, score):
    q = """
INSERT INTO performance
(performance_id, venue_id, performance_date, review_score)
VALUES
(%s, %s, %s, %s)"""

    cur = connection.cursor()
    cur.execute(q, (perf_id, venue_id, perf_date, score))
    connection.commit()


def add_new_ppa_assignments(connection, ppa_id, performer_ids, performance_id):
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


# def get_per_pnce_assign_str():
#     ...


# p = """INSERT INTO rating_interaction
#             (event_at, exhibition_id, rating_id)
#         VALUES %s;
#     """

# extras.execute_values(cur, p, data)
# # # thing that talks to the db, thing with one gap, list of things that can fill the gap
