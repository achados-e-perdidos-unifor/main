"""Pytest configuration and fixtures for integration tests."""

import os
import sys
import pytest
import requests
from time import sleep

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Model.Database import conectar_BD


@pytest.fixture(scope="session")
def app_url():
    """URL of the Flask application (used in integration tests with docker-compose)."""
    return os.getenv("APP_URL", "http://localhost:5000")


@pytest.fixture(scope="session")
def wait_for_app(app_url):
    """Wait for Flask application to be ready."""
    max_retries = 30
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = requests.get(f"{app_url}/health", timeout=2)
            if response.status_code == 200:
                print("\n✅ Application is ready!")
                return True
        except requests.exceptions.RequestException:
            retry_count += 1
            sleep(1)

    raise RuntimeError(
        f"Application did not become ready after {max_retries} seconds. "
        f"Make sure docker-compose is running and {app_url} is accessible."
    )


@pytest.fixture(scope="function")
def clean_database():
    """Clean test data from database before and after each test."""
    conn = conectar_BD()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE objetos_achados CASCADE;")
            cursor.execute("TRUNCATE TABLE objetos_perdidos CASCADE;")
            conn.commit()
        except Exception as e:
            print(f"Warning: Could not clean database: {e}")
        finally:
            conn.close()

    yield

    conn = conectar_BD()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE objetos_achados CASCADE;")
            cursor.execute("TRUNCATE TABLE objetos_perdidos CASCADE;")
            conn.commit()
        except Exception as e:
            print(f"Warning: Could not clean database after test: {e}")
        finally:
            conn.close()


@pytest.fixture
def http_client(app_url, wait_for_app):
    """Provide HTTP client with base URL."""
    class HTTPClient:
        def __init__(self, base_url):
            self.base_url = base_url

        def get(self, endpoint):
            return requests.get(f"{self.base_url}{endpoint}")

        def post(self, endpoint, json=None):
            return requests.post(f"{self.base_url}{endpoint}", json=json)

        def put(self, endpoint, json=None):
            return requests.put(f"{self.base_url}{endpoint}", json=json)

        def delete(self, endpoint):
            return requests.delete(f"{self.base_url}{endpoint}")

    return HTTPClient(app_url)
