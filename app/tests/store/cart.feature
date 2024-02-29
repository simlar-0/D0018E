# Tests for cart feature. 
Feature: Cart

    Scenario: Add to cart
        Given I am logged in as a customer

        Given I have a catalog

        When I press the add to cart button

        When The amount of items I have chosen is X

        Then X items should be added to my cart
    
    Scenario: View cart
        Given I am logged in as a customer

        Given I have 0 to X items in my cart

        When I press the view cart button

        Then I should see all items in my cart

    Scenario: Update cart
        Given I am logged in as a customer

        Given I have 0 to X items in my cart

        When I change the amount of items in my cart
        
        And I press the update cart button

        Then The amount of items in my cart should be updated
    
    Scenario: Checkout
        Given I am logged in as a customer

        Given I have more than 0 items in my cart

        When I press the checkout button

        Then I should get a confirmation

        Then The cart should be added to my past orders

        Then All items should be removed from my cart
