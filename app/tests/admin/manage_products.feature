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

    Scenario: Edit a product
        Given I am logged in as a manager or admin

        And I am in the Manage products page

        When I press the product name link

        Then A form to edit the product should appear on the screen

    Scenario: Unlist a product
        Given I am logged in as a manager or admin

        And I am in the Edit product page

        When I select the Unlist status of the product

        And I press the Apply changes button

        Then The product status should be changed

        And The product should not appear in customer views