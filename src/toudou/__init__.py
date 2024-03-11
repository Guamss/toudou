TODO_FOLDER = "database"
DATABASE = "toudou.db"
TABLE_NAME = "TOUDOU"

config = dict(
    FLASK_SECRET_KEY = "azerty",
    DATABASE_URL=f"sqlite:///{TODO_FOLDER}/{DATABASE}",
    DEBUG=True
)