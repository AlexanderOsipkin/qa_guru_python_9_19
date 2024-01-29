import json
import requests

from jsonschema import validate
from resource.resource import schema_dir


def test_login():
    response = requests.post(
        'https://reqres.in/api/login',
        json={"email": "eve.holt@reqres.in", "password": "cityslicka"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body['token'] == 'QpwL5tke4Pnpja7X4'


def test_failed_login():
    response = requests.post('https://reqres.in/api/login')
    assert response.status_code == 400
    body = response.json()
    assert body['error'] == 'Missing email or username'


def test_successful_register_user():
    response = requests.post(
        'https://reqres.in/api/register',
        json={"email": "eve.holt@reqres.in", "password": "pistol"},
    )
    body = response.json()
    schema_path = schema_dir("register.json")
    with open(schema_path) as file:
        schema = json.load(file)
    validate(body, schema=schema)
    assert response.status_code == 200


def test_unsuccessful_register_user():
    response = requests.post(
        'https://reqres.in/api/register', json={"email": "sydney@fife"}
    )
    assert response.status_code == 400


def test_create_user_validate_schema():
    response = requests.post(
        'https://reqres.in/api/users/', json={"name": "Bob", "job": "Builder"}
    )
    body = response.json()
    schema_path = schema_dir('create_user.json')
    with open(schema_path) as file:
        validate(body, schema=json.loads(file.read()))
    assert response.status_code == 201


def test_validate_users_list():
    response = requests.get('https://reqres.in/api/users?page=2')
    body = response.json()
    schema_path = schema_dir('users_list.json')
    with open(schema_path) as file:
        validate(body, schema=json.loads(file.read()))
    assert response.status_code == 200


def test_validate_user_schema():
    response = requests.get('https://reqres.in/api/users/2')
    body = response.json()
    schema_path = schema_dir('user_schema.json')
    with open(schema_path) as file:
        validate(body, schema=json.loads(file.read()))
    assert response.status_code == 200


def test_delete_user():
    response = requests.delete('https://reqres.in/api/users/2')
    assert response.status_code == 204


def test_user_not_found():
    response = requests.get('https://reqres.in/api/users/20000')
    assert response.status_code == 404


def test_empty_response():
    response = requests.delete('https://reqres.in/api/users/20000')
    print(response.text)
    assert response.text == ''
