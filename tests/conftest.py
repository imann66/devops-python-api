import pytest
from sqlalchemy.engine import make_url

from app.app import create_app
from app.config import TestingConfig
from app.extensions import db


@pytest.fixture(scope="session")
def app():
    test_app = create_app(TestingConfig)

    # Safety check: never allow tests to modify the development database.
    database_url = make_url(
        test_app.config["SQLALCHEMY_DATABASE_URI"]
    )

    if database_url.database != "devops_api_test":
        raise RuntimeError(
            "Tests must use the devops_api_test database."
        )

    return test_app


@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

        yield

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
