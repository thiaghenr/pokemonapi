import pytest
import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .test_database import TestingSessionLocal, test_engine
from main import app, get_db
from database import Base as Test_Base
import models, hashing


Test_Base.metadata.create_all(test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# from .test_pokemon import TestPokemon


def test_delete_db_data():
    Test_Base.metadata.drop_all(bind=test_engine)
    Test_Base.metadata.create_all(bind=test_engine)