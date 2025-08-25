import pytest
import requests
from helpers.helpers import ApiClient
from data import BASE_URL, test_user

class TestAuth:
    # Успешная авторизация ранее зарегистрированного пользователя
    def test_auth(self):
        apiclient = ApiClient()
        response = apiclient.signin(test_user["email"], test_user["password"])
        assert response.status_code == 201
        
        data = response.json()
        assert "user" in data and isinstance(data["user"], dict), data
        assert "token" in data and isinstance(data["token"], dict), data
        assert "access_token" in data["token"], data
        token = data["token"]["access_token"]
        assert isinstance(token, str) and token, data