import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "pwd": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "db": os.getenv("DB_NAME"),
}


def get_connection_string():
    return "postgresql://{}:{}@{}:{}/{}".format(
        DB_CONFIG["user"],
        DB_CONFIG["pwd"],
        DB_CONFIG["host"],
        DB_CONFIG["port"],
        DB_CONFIG["db"],
    )