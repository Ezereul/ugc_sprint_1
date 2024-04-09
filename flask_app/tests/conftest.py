from unittest.mock import Mock

import pytest

from flask_app.app import create_app


@pytest.fixture
def app_with_producer():
    app = create_app(testing=True)
    app.producer = Mock()
    return app


@pytest.fixture
def client(app_with_producer):
    with app_with_producer.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def neuter_jwt(monkeypatch):
    monkeypatch.setattr('flask_jwt_extended.utils.get_jwt', lambda: {'_jwt_extended_jwt': '123'})
    monkeypatch.setattr('flask_jwt_extended.view_decorators.verify_jwt_in_request', lambda *args: None)
