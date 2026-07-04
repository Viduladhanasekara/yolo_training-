import mysql.connector
from mysql.connector import Error
import config


def get_connection():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        database=config.MYSQL_DATABASE,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
    )


def init_table():
    """Create the cracks table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cracks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            severity VARCHAR(20),
            image_path VARCHAR(255),
            crack_type VARCHAR(50),
            confidence FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            fps FLOAT,
            camera_id VARCHAR(50)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def insert_detection(data: dict):
    """
    Insert one detection record into MySQL.
    data keys: timestamp, severity, image_path, crack_type,
               confidence, latitude, longitude, fps, camera_id
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cracks
            (timestamp, severity, image_path, crack_type, confidence, latitude, longitude, fps, camera_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["timestamp"], data["severity"], data["image_path"], data["crack_type"],
            data["confidence"], data["latitude"], data["longitude"], data["fps"], data["camera_id"],
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Saved to MySQL."
    except Error as e:
        return False, f"MySQL error: {e}"