import pytest
import requests
from helpers.helpers import ApiClient
from data import BASE_URL, test_user, test_order

class TestOrder:
    # Успешное создание объявления в любой категории
    def test_create_order(self):
        apiclient = ApiClient()
        apiclient.signin(test_user["email"], test_user["password"])

        # Создание объявления
        order_payload = {
            "name": test_order["name"],
            "category": test_order["category"],
            "condition": test_order["condition"],
            "city": test_order["city"],
            "description": test_order["description"],
            "price": str(test_order["price"]),
        }

        order_response = apiclient.create_listing(order_payload)
        assert order_response.status_code == 201
        order_data = order_response.json()

        assert order_data["name"] == order_payload["name"]
        assert order_data["category"] == order_payload["category"]
        assert order_data["condition"] == order_payload["condition"]
        assert order_data["city"] == order_payload["city"]
        assert int(order_data["price"]) == int(order_payload["price"])

    # Успешное редактирование любого поля объявления
    def test_edit_order(self):
        # Авторизация пользователя
        apiclient = ApiClient()
        apiclient.signin(test_user["email"], test_user["password"])

        # Создание объявления для редактирования
        order_payload = {
            "name": test_order["name"],
            "category": test_order["category"],
            "condition": test_order["condition"],
            "city": test_order["city"],
            "description": test_order["description"],
            "price": str(test_order["price"]),
        }

        order_response = apiclient.create_listing(order_payload)
        assert order_response.status_code == 201
        order_data = order_response.json()
        order_id = order_data["id"]

        # Редактирование объявления
        edited_order_payload = {
            "name": "Updated Test Order",
            "category": test_order["category"],
            "condition": test_order["condition"],
            "city": test_order["city"],
            "description": test_order["description"],
            "price": str(test_order["price"]),
        }
        edit_response = apiclient.update_offer(order_id, edited_order_payload)
        assert edit_response.status_code == 200
        edit_data = edit_response.json()

        assert edit_data["name"] == edited_order_payload["name"]

    # Редактирование объявления, созданного не тем пользователем, под токеном которого производится редактирование
    def test_edit_order_not_owner(self):
        # Авторизация пользователя
        apiclient = ApiClient()
        apiclient.signin(test_user["email"], test_user["password"])

        edited_order_payload = {
            "name": "Updated Test Order",
            "category": test_order["category"],
            "condition": test_order["condition"],
            "city": test_order["city"],
            "description": test_order["description"],
            "price": str(test_order["price"]),
            "image": test_order["image"]
        }

        edit_response = apiclient.update_offer(68, edited_order_payload)
        
        # Ожидается ошибка доступа или несуществующего ресурса
        assert edit_response.status_code == 401

    # Успешное удаление объявления
    def test_delete_order(self):
        # Авторизация пользователя
        apiclient = ApiClient()
        apiclient.signin(test_user["email"], test_user["password"])

        # Создание объявления для удаления
        order_payload = {
            "name": test_order["name"],
            "category": test_order["category"],
            "condition": test_order["condition"],
            "city": test_order["city"],
            "description": test_order["description"],
            "price": str(test_order["price"]),
            "image": test_order["image"]
        }

        order_response = apiclient.create_listing(order_payload)
        assert order_response.status_code == 201
        order_data = order_response.json()
        order_id = order_data["id"]

        # Удаление объявления
        delete_response = requests.delete(f"{BASE_URL}/listings/{order_id}", headers=apiclient.get_auth_headers())
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert delete_data["message"] == "Объявление удалено успешно"