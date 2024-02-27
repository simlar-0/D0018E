# Tests for product reviews feature. 
Feature: Review
    Review

    Scenario: Leave a review
        Given I am logged in as a customer

        Given I am on a product page

        Given I have previously purchased this product

        Given I have not prevously reviewd this item

        When I clicked on the amount of stars I want to given

        Then My ranking should be added to the product

        Then If I have given a comment, then the comment should be added to the product

