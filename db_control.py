"""
Central database control layer.
Lets the Streamlit UI turn MongoDB / MySQL saving ON or OFF
independently, without touching the detection pipeline.
"""

import mysql_db
import mongo_db


def save_detection(data: dict, mysql_enabled: bool, mongo_enabled: bool):
    """
    Save a detection record to whichever database(s) are enabled.
    Returns a list of (db_name, success, message) tuples.
    """
    results = []

    if mysql_enabled:
        ok, msg = mysql_db.insert_detection(data)
        results.append(("MySQL", ok, msg))

    if mongo_enabled:
        ok, msg = mongo_db.insert_detection(data)
        results.append(("MongoDB", ok, msg))

    return results