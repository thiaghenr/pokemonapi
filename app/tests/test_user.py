import json
from fastapi.testclient import TestClient
from main import app
import hashing


client = TestClient(app)

class TestUser():
    def test_create_user(self):
        new_user = self.user_thiago()
        response = client.post('/user', data = json.dumps(new_user))
        new_user_response = response.json()
        print('--=======')
        print(new_user_response)
        assert response.status_code == 201, response.text
        assert new_user_response['name'] == new_user['name']
        # assert new_user_response['password'] == new_user['password']
        assert new_user_response['email'] == new_user['email']

    def user_thiago(self):
        return {
            'id': 1,
            'name': 'Thiago Henry',
            'password': hashing.Hash().bcrypt('123456'),
            'email': 'thiago@email.com'
        }