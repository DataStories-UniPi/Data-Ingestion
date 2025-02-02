import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()  # Load environment variables from .env file if it exists


PROJ_ROOT = Path(__file__).resolve().parents[1]  # Root directory

# Path configurations
MISC_DIR = PROJ_ROOT / "misc"
LOGS_DIR = PROJ_ROOT / "logs"
BACKUP_DIR = PROJ_ROOT / "backups"

DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DB_NAME = os.environ["POSTGRES_DB"]

# Request parameters
API_URL = "https://api.deelfietsdashboard.nl/dashboard-api/public/vehicles_in_public_space"
REFRESH_INTERVAL = 60
BACKUP_INTERVAL = 24  # Interval in hours

logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")
