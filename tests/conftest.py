import pytest
import tempfile
import os
from app import create_app, db
from app.models import Student, Grade


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def app_context(app):
    """Push application context."""
    with app.app_context():
        yield
