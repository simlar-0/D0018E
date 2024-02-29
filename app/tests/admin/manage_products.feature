# Tests for customer management feature
Feature: Management of products
    Scenario: Show a list of products
        Given I am logged in as a manager or admin

        And I am in the admin panel

        When I press the Manage products button in the admin side panel

        Then A list of all products should appear on the screen
        

    Scenario: Add a new product
        Given I am logged in as a manager or admin

        And I am in the Manage products page

        When I press the Add product button

        Then A form to add a new product should appear on the screen

        When I fill in the product details

        And I press the Add product button

        Then The product should be added to the list of products

    Scenario: Edit a product
        Given I am logged in as a manager or admin

        And I am in the Manage products page

        When I press the product name link

        Then A form to edit the product should appear on the screen

        When I change the product details

        And I press the Apply changes button

        Then The product details should be changed

    Scenario: Change product status
        Given I am logged in as a manager or admin

        And I am in the Edit product page

        When I select the status of the product

        And I press the Apply changes button

        Then The product status should be changed