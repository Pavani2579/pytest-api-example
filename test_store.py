from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


@pytest.fixture
def created_order():
    payload = {
        "pet_id": 0
    }

    response = api_helpers.post_api_data("/store/order", payload)

    assert response.status_code == 201

    order_data = response.json()

    return order_data["id"], payload["pet_id"]


def test_patch_order_by_id(created_order):

    order_id, pet_id = created_order

    patch_payload = {
        "status": "sold"
    }

    response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["message"] == "Order and pet status updated successfully"

    pet_response = api_helpers.get_api_data(f"/pets/{pet_id}")

    assert pet_response.status_code == 200
    assert pet_response.json()["status"] == "sold"