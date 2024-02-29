Feature: Manage Orders
    Scenario: Load order list
        Given I am logged in as an admin or store manager

        And there are non-cart orders in the DB

        When I press on manage orders in the admin panel

        Then I will see a list of all non-cart orders in the DB

    Scenario: Change order status
        Given I am logged in as an admin or store manager

        And there are non-cart orders in the DB

        And I am viewing the orders list

        When I pick a new status from the dropdown list of an order

        Then the order status will be updated in the DB

        And the page will update accordingly