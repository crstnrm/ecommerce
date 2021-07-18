from mixer.backend.django import mixer
from orders.logic import OrderLogic
from orders.models import Order
from pytest_bdd import given, scenarios, then, when
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

scenarios('../features/list_orders.feature')

ORDERS_ENDPOINT = '/orders/'
TOKEN_ENDPOINT = '/api/token/'


@given('I am a registered user', target_fixture='scenario')
def create_user():
    return {}


@given('I am logged in')
def login(scenario, mock_user):
    client = APIClient()
    data = {
        'username': mock_user.username,
        'password': '1234',
    }
    response = client.post(TOKEN_ENDPOINT, data, format='json')
    body = response.json()
    scenario['token'] = body['access']


@given('There are several orders created')
def create_orders(db):
    return [
        mixer.blend(Order),
        mixer.blend(Order),
        mixer.blend(Order)
    ]


@when('I list the orders')
def list_orders(scenario):
    token = scenario['token']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    scenario['response'] = client.get(ORDERS_ENDPOINT, format='json')
    

@then('A data is displayed in the screen')
def validate_process(scenario):
    response = scenario['response']
    assert response.status_code == HTTP_200_OK

    order_logic = OrderLogic()
    orders_len = order_logic.find().count()
    body = response.json()

    assert orders_len == body['total_records']
    assert body['offset'] == 0
    assert body['limit'] == 3
    