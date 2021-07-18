@SendShipment
Feature: List orders
    As a user
    I want to list the orders created in the platform
    So that I give a review about it

    Scenario: I list the orders
        Given I am a registered user
        And I am logged in
        And There are several orders created
        When I list the orders
        Then A data is displayed in the screen
