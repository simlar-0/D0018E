# Tests for product browsing feature. 
Feature: Customer Login
    Customer login

    Scenario: Correct credentials
        Given I have login credentials

        Given I am on the login page

        When I enter correct password and email

        When I press login

        Then I should be logged in
    
    Scenario: Incorrect credentials
        Given I have login credentials

        Given I am on the login page

        When I enter incorrect password and email

        When I press login

        Then I should get an error message