# Tests for order view feature. 
Feature: View Orders
    Review

    Scenario: View Orders
        Given I am logged in as a customer

        Given I press the view orders button in my profile

        When I have previously made orders

        Then All of my orders should appear in the page

