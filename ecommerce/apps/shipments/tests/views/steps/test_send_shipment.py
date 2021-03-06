from contextlib import nullcontext

import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer
from orders.constants import OrderStatus
from orders.models import Order
from pytest_bdd import given, parsers, scenarios, then, when
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
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


@given('I have an order', target_fixture='mock_order')
@given('I have an order already created', target_fixture='mock_order')
def create_order(db):
    return mixer.blend(Order)


@given(
    parsers.parse('I have a shipment "{mock_shipment_id}" already configured'),
    target_fixture='mock_shipment'
)
def create_shipment(mock_order, mock_shipment_id):
    return mixer.blend(Shipment, order=mock_order, id=mock_shipment_id)


@when(parsers.parse('I send the shipment <shipment_id> "{flow}"'))
def send_shipment(mock_send_communication, scenario, shipment_id, flow):
    token = scenario['token']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    context_mananger = (
        nullcontext()
        if flow == 'successfully'
        else pytest.raises(ValidationError)
    )

    with context_mananger:
        scenario['response'] = client.post(
            SEND_SHIPMENT_ENDPOINT.format(shipment_id=shipment_id),
            format='json'
        )


@then('A successful message is returned')
def validate_process(scenario, mock_shipment):
    mock_shipment.refresh_from_db()
    response = scenario['response']
    assert response.status_code == HTTP_204_NO_CONTENT
    assert mock_shipment.status == ShipmentStatus.SENT.value
    assert mock_shipment.order.status == OrderStatus.SENT.value


@then('An unsuccessful message is returned')
def validate_process(scenario):
    assert 'response' not in scenario
