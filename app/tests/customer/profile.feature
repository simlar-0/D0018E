#
Feature: Customer profile

    Scenario: View Orders
        Given I am logged in as a customer

        Given I press the view orders button in my profile

        When I have previously made orders

        Then All of my orders should appear in the page

    Scenario: Edit Profile
        Given I am logged in as a customer

        Given I press the edit profile button in my profile sidebar

        When I change my details

        Then My details should be updated

        