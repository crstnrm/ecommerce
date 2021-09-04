@SendShipment
Feature: Send a shipment
    As a user
    I want to send a shipment
    So that I can delivery the order

    Scenario: I send a order through a shipment
        Given I am a registered user
        And I am logged in
        And I have an order already created
        And I have a shipment "1" already configured
        When I send the shipment <shipment_id> "successfully"
        Then A successful message is returned

        Examples:
        | shipment_id |
        | 1           |

    Scenario: I send a shipment and the shipement doesn't exits
        Given I am a registered user
        And I am logged in
        And I have an order
        And I have a shipment "1" already configured
        When I send the shipment <shipment_id> "unsuccessfully"
        Then An unsuccessful message is returned

        Examples:
        | shipment_id |
        | 2           |
        | 12          |
