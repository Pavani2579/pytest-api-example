from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    validate(instance=response.json(), schema=schemas.pet)


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)

    assert response.status_code == 200

    response_json = response.json()

    assert isinstance(response_json, list)

    for pet in response_json:
        assert pet["status"] == status
        validate(instance=pet, schema=schemas.pet)


@pytest.mark.parametrize("pet_id", [999, -1, 100000])
def test_get_by_id_404(pet_id):

    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404
    assert_that(response.text.lower(), contains_string("not found"))