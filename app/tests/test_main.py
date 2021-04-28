import pytest
import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .test_database import TestingSessionLocal, test_engine
from main import app, get_db
from database import Base as Test_Base
import models


Test_Base.metadata.create_all(test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create():
    jobossauro  = jobossauro_data()
    raichu      = raichu_data()

    jobossauro_response = client.post('/pokemon', data = json.dumps(jobossauro))
    new_jobossauro      = jobossauro_response.json()

    assert jobossauro_response.status_code == 201, jobossauro_response.text
    assert new_jobossauro['id'] == jobossauro['id'] 
    assert new_jobossauro['name'] == jobossauro['name']
    assert new_jobossauro['weight'] == jobossauro['weight']

    raichu_response = client.post('/pokemon', data = json.dumps(raichu))
    new_raichu = raichu_response.json()
    assert raichu_response.status_code == 201, raichu_response.text
    assert new_raichu['id'] == raichu['id']
    assert new_raichu['name'] == raichu['name']
    assert new_raichu['weight'] == raichu['weight']


def test_get_all():
    response = client.get('/pokemon')
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_pokemon():
    pokemon_id = 2
    response = client.delete(f'/pokemon/{pokemon_id}')
    assert response.status_code == 204
    assert response.json() == 'Deleted'


# def test_update_pokemon():
#     pokemon_id = 1
#     response = client.put(f'/pokemon/{pokemon_id}')
#     import pprint
#     pprint.pprint("=========")
#     pprint.pprint(response)
#     assert response.status_code == 202
#     assert response.json() == 'Updated'


def test_get_pokemon():
    pokemon_id = 1
    response = client.get(f'/pokemon/{pokemon_id}')
    jobossauro = jobossauro_data()
    pokemon = response.json()
    
    assert response.status_code == 200, response.text
    # assert pokemon['id'] == jobossauro['id']
    assert pokemon['name'] == jobossauro['name']
    assert pokemon['weight'] == jobossauro['weight']



def test_create_pokemon_type():
    pokemon_type_eletric = {'name': 'eletric'}
    eletric_response = client.post('/pokemonType', data = json.dumps(pokemon_type_eletric))
    new_eletric_type = eletric_response.json()

    assert eletric_response.status_code == 201, eletric_response.text
    assert new_eletric_type['name'] == pokemon_type_eletric['name']

    pokemon_type_aquatic = {'name': 'aquatic'}
    aquatic_response = client.post('/pokemonType', data = json.dumps(pokemon_type_aquatic))
    new_aquatic_type = aquatic_response.json()

    assert aquatic_response.status_code == 201, aquatic_response.text
    assert new_aquatic_type['name'] == pokemon_type_aquatic['name']


def test_get_all_pokemon_type():
    response = client.get('/pokemonType')
    assert response.status_code == 200
    assert len(response.json()) == 2

# def test_update_pokemon_type():
#     pokemon_type_id = 1


def test_create_user():
    new_user = user_thiago()
    response = client.post('/user', data = json.dumps(new_user))
    new_user_response = response.json()
    print('--=======')
    print(new_user_response)
    assert response.status_code == 201, response.text
    assert new_user_response['name'] == new_user['name']
    assert new_user_response['password'] == new_user['password']
    assert new_user_response['email'] == new_user['email']



def test_delete_db_data():
    Test_Base.metadata.drop_all(bind=test_engine)
    Test_Base.metadata.create_all(bind=test_engine)


def jobossauro_data():
    return {
        'id': 1,
        'name': 'jobossauro',
        'height': 1.5,
        'weight': 2.5,
        'xp': 50,
        'image': 'www.pokemon.com/jobossauro'
    }


def raichu_data():
    return {
        'id': 2,
        'name': "raichu",
        'height': 3.5,
        'weight': 7.5,
        'xp': 70    ,
        'image': "www.pokemon.com/raichu"
    }


def user_thiago():
    return {
        'id': 1,
        'name': 'Thiago Henry',
        'password': '123456',
        'email': 'thiago@email.com'
    }