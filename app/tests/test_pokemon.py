import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestPokemon():

    # def __init__(self, client) -> None:
    #     self.client = client

    def test_create_pokemon_type(self):
    
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


    def test_create(self):
        jobossauro  = self.jobossauro_data()
        raichu      = self.raichu_data()

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


    def test_get_all(self):
        response = client.get('/pokemon')
        print('response')
        print(response)
        print('=======')
        assert response.status_code == 200
        assert len(response.json()) == 2


    def test_delete_pokemon(self):
        pokemon_id = 2
        response = client.delete(f'/pokemon/{pokemon_id}')
        assert response.status_code == 204
        assert response.json() == 'Deleted'


    def test_get_pokemon(self):
        pokemon_id = 1
        response = client.get(f'/pokemon/{pokemon_id}')
        jobossauro = self.jobossauro_data()
        pokemon = response.json()
        
        assert response.status_code == 200, response.text
        # assert pokemon['id'] == jobossauro['id']
        assert pokemon['name'] == jobossauro['name']
        assert pokemon['weight'] == jobossauro['weight']




    def test_get_all_pokemon_type(self):
        response = client.get('/pokemonType')
        assert response.status_code == 200
        assert len(response.json()) == 2


    def jobossauro_data(self):
        return {
            'id': 1,
            'name': 'jobossauro',
            'height': 1.5,
            'weight': 2.5,
            'xp': 50,
            'types': self.pokemon_types_data(),
            'image': 'www.pokemon.com/jobossauro'
        }


    def raichu_data(self):
        return {
            'id': 2,
            'name': "raichu",
            'height': 3.5,
            'weight': 7.5,
            'xp': 70    ,
            'types': self.pokemon_types_data(),
            'image': "www.pokemon.com/raichu"
        }
    

    def pokemon_types_data(self):
        return [
            {'name': 'eletric'},
            {'name': 'aquatic'}
        ]