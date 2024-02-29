# Tests for customer management feature
Feature: Management
    Scenario: Show a list of customers
        Given I am logged in as a manager
        
        When I press Customer button

        Then a webpage with customer list should appear on the screen

    Scenario: Show Customer orders list
        Given I am logged in as a manager

        Given I have the customer list open

        When I click order link  in a list entry

        Then a webpage with customer order list should appear on the screen
    
    Scenario: Edit customer information
        Given I am logged in as a manager

        Given I have the customer list open

        When I click edit link in a list entry

        Then a webpage with customer information appear on the screen

        When I edit the information on the screen and click Apply button

        Then a message confirming that account information was changed

    Scenario: Delete a  customer account
            Given I am logged in as a manager

            Given I have the customer list open

            When I click remove link in a list entry

            Then the customer account is deleted from the database and the list
