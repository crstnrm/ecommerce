from mixer.backend.django import mixer
from orders.constants import OrderStatus
from orders.models import Order
from pytest_bdd import given, scenarios, then, when
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from shipments.constants import ShipmentStatus
from shipments.models import Shipment

scenarios('../features/send_shipment.feature')

SEND_SHIPMENT_ENDPOINT = '/shipments/{shipment_id}/send/'
TOKEN_ENDPOINT = '/api/token/'


@given('I am a registered user', target_fixture='scenario')
def create_user():
    return {}


@given('I am logged in')
def login(scenario, mock_user):
    client = APIClient()
    data = {
        'username': mock_user.username,
        'password': mock_user.plain_password,
    }
    response = client.post(TOKEN_ENDPOINT, data, format='json')
    body = response.json()
    scenario['token'] = body['access']


@given('I have an order already created', target_fixture='mock_order')
def create_order(db):
    return mixer.blend(Order)


@given('I have a shipment already configured', target_fixture='mock_shipment')
def create_shipment(db, mock_order):
    return mixer.blend(Shipment, order=mock_order)


@when('I send the shipment')
def send_shipment(mock_send_communication, scenario, mock_shipment):
    token = scenario['token']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    scenario['response'] = client.post(
        SEND_SHIPMENT_ENDPOINT.format(shipment_id=mock_shipment.id),
        format='json'
    )


@then('A successful message is returned')
def validate_process(scenario, mock_shipment):
    mock_shipment.refresh_from_db()
    response = scenario['response']
    assert response.status_code == HTTP_204_NO_CONTENT
    assert mock_shipment.status == ShipmentStatus.SENT.value
    assert mock_shipment.order.status == OrderStatus.SENT.value
