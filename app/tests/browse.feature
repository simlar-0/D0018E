# Tests for product browsing feature. 
Feature: Product Browsing
    Browsing items

    Scenario: Render Procucts
        When I enter the catalog

        Then I should see the available products
    
    Scenario: Visiting the product information page
        When I press a product link

        Then I should see the product information page

    Scenario: Load More products
        When I press an arrow
        
        Then I should see a list of new products