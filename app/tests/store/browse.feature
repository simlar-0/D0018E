# Tests for product browsing feature. 
Feature: Product Browsing
    Browsing items

    Scenario: Render Products
        Given I have a catalog

        When I enter the catalog

        Then I should see the available products

    Scenario: View product details
        Given I have a catalog

        When I enter the catalog

        When I press a product link

        Then I should see the product details

    Scenario: Load More products
        Given I have a catalog

        When I enter the catalog

        When I press an arrow
        
        Then I should see a list of new products