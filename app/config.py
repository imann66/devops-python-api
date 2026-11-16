
import os

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


def build_database_url(database_name):
    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=database_name,
    )


class Config:
    SQLALCHEMY_DATABASE_URI = build_database_url(
        os.getenv("DB_NAME", "devops_api")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = build_database_url(
        os.getenv("TEST_DB_NAME", "devops_api_test")
    )
