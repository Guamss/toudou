import os 
import logging

TODO_FOLDER = "database"
DATABASE = "toudou.db"
TABLE_NAME = "TOUDOU"

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
    handlers=[
        logging.FileHandler("log/toudou.log"),
            logging.StreamHandler()
    ]
)

config = dict(
    LOGGING = logging,
    FLASK_SECRET_KEY = os.getenv("TOUDOU_FLASK_SECRET_KEY", ""),
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True"
)