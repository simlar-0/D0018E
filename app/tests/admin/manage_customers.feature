# Tests for customer management feature
Feature: Management
    Scenario: Show a list of customers
        Given I am logged in as a manager
        
        When I press Customer button

        Then a webpage with customer list should appear on the screen

    Scenario: Show Customer orders list
        Given I am logged in as a manager

        Given I have the customer list open

        When I click customer name in a list entry

        Then a webpage with customer order list should appear on the screen