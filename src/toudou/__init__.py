import os 

TODO_FOLDER = "database"
DATABASE = "toudou.db"
TABLE_NAME = "TOUDOU"

config = dict(
    FLASK_SECRET_KEY = os.getenv("TOUDOU_FLASK_SECRET_KEY", ""),
    DATABASE_URL=os.getenv("TOUDOU_DATABASE_URL", ""),
    DEBUG=os.getenv("TOUDOU_DEBUG", "False") == "True"
)