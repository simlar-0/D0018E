# Tests for product browsing feature. 
Feature: Register

    Scenario: Email exists
        Given I am on the register page

        When I fill in all fields

        When I use an email address that already exists in the DB

        Then I should get an error message

        Then No data will be changed or added
    
    Scenario: Unique email
        Given I am on the register page

        When I fill in all fields

        When I use an email address that does not already exists in the DB

        Then I should be added to the DB