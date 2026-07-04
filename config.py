import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOADS_DIR, exist_ok=True)

# ---------------- Drone ----------------
CAMERA_ID = "DRONE001"

# ---------------- MySQL ----------------
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "crack_db")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# ---------------- MongoDB ----------------
MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DB_NAME = "crack_detection"
MONGO_COLLECTION = "detections"

# ---------------- Detection ----------------
CONF_THRESHOLD = 0.4

SEVERITY_HIGH = 0.80
SEVERITY_MEDIUM = 0.55