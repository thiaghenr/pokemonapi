import sys
sys.path.append('/home/user/Desktop/app') #/home/user/Desktop/app
import sys
from fastapi.testclient import TestClient
from test_database import test_engine, override_get_db
from app.main import app, pokemon, pokemon_type, user, team
from app.routers.pokemon import get_db

pokemon.Base.metadata.create_all(test_engine)
pokemon_type.Base.metadata.create_all(test_engine)
user.Base.metadata.create_all(test_engine)
team.Base.metadata.create_all(test_engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_delete_db_data():
    pokemon.Base.metadata.drop_all(bind=test_engine)
    pokemon_type.Base.metadata.drop_all(bind=test_engine)
    user.Base.metadata.drop_all(bind=test_engine)
    team.Base.metadata.drop_all(bind=test_engine)

    pokemon.Base.metadata.create_all(bind=test_engine)
    pokemon_type.Base.metadata.create_all(bind=test_engine)
    user.Base.metadata.create_all(bind=test_engine)
    team.Base.metadata.create_all(bind=test_engine)