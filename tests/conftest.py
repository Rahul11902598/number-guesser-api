# tests/conftest.py
"""Pytest configuration and fixtures"""

import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """Create application for testing"""
    flask_app.config.update({
        'TESTING': True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """Test client for making requests"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner for testing commands"""
    return app.test_cli_runner()

@pytest.fixture
def sample_game(client):
    """Create a sample game for testing"""
    response = client.post('/game/start', json={
        'player_name': 'TestHero',
        'difficulty': 'easy'
    })
    data = response.get_json()
    return data['game_id']