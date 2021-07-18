@SendShipment
Feature: Send a shipment
    As a user
    I want to send a shipment
    So that I can delivery the order

    Scenario: I send a order through a shipment
        Given I am a registered user
        And I am logged in
        And I have an order already created
        And I have a shipment already configured
        When I send the shipment
        Then A successful message is returned
