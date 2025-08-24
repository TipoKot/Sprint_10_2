import requests
import uuid
from data import BASE_URL, test_order
from pathlib import Path


class ApiClient:
    def __init__(self):
        self.token = None

    def register_new_user(self):
        email = f"user_{uuid.uuid4()}@example.com"
        password = "securePassword123"
        return requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})

    def signin(self, email: str, password: str) -> str:
        response = requests.post(f"{BASE_URL}/signin", json={"email": email, "password": password})
        self.token = response.json()["token"]["access_token"]
        return response
    
    def get_auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def create_listing(self, order_payload: dict):
        img_path = Path(__file__).resolve().parent / "test.png"
        files = {"images": (img_path.name, open(img_path, "rb"), "image/png")}
        return requests.post(f"{BASE_URL}/create-listing", data=order_payload, files=files, headers=self.get_auth_headers())

    def update_offer(self, listing_id: int, fields: dict):
        img_path = Path(__file__).resolve().parent / "test.png"
        files = {"images": (img_path.name, open(img_path, "rb"), "image/png")}
        return requests.patch(f"{BASE_URL}/update-offer/{listing_id}", data=fields, files=files, headers=self.get_auth_headers())
