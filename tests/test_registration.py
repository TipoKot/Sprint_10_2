import pytest
import requests
import uuid
from helpers.helpers import ApiClient
from data import BASE_URL, test_user

class TestRegistration:
    # Успешная регистрация нового пользователя с уникальным email (генерировать новый email для каждого теста регистрации обязательно)
    def test_registration(self):
        apiclient = ApiClient()
        response = apiclient.register_new_user()
        assert response.status_code == 201

    # Повторная регистрация пользователя (используется email который уже есть в БД)
    def test_registration_existing_email(self):
        payload = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/signup", json=payload)
        assert response.status_code == 400
        data = response.json()

        assert "message" in data, data
        assert data["message"] == "Почта уже используется"