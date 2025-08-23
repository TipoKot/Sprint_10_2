import requests
import uuid
from data import BASE_URL, test_order
from pathlib import Path


class ApiClient:
    def register_new_user(self):
        email = f"user_{uuid.uuid4()}@example.com"
        password = "securePassword123"
        return requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})

    def signin(self, email: str, password: str) -> str:
        return requests.post(f"{BASE_URL}/signin", json={"email": email, "password": password})

    def create_listing(self, headers: dict, order_payload: dict):
        img_path = Path(test_order.get("image_path", "test.png"))
        files = {"images": (img_path.name, open(img_path, "rb"), "image/png")}
        return requests.post(f"{BASE_URL}/create-listing", data=order_payload, files=files, headers=headers)

    def update_offer(self, headers: dict, listing_id: int, fields: dict):
        img_path = Path(test_order.get("image_path", "test.png"))
        files = {"images": (img_path.name, open(img_path, "rb"), "image/png")}
        return requests.patch(f"{BASE_URL}/update-offer/{listing_id}", data=fields, files=files, headers=headers)
