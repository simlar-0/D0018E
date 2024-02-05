"""
Step definitions for browse.feature
"""
from pytest_bdd import scenario, given, when, then
import pytest

@scenario('browse.feature', 'Render Products')
def render_products():
    pass

@pytest.fixture
def catalog():
    return ""

@when('I enter the catalog', target_fixture='catalog')
def step_enter_catalog():
    pass

@then('I should see the available products')
def step_see_available_products():
    pass

@scenario('browse.feature', 'Visiting the product information page')
def visiting_the_product_information_page():
    pass

@when('I press a product link')
def step_press_product_link():
    pass

@then('I should see the product information page')
def step_see_product_info_page():
    pass

@scenario('browse.feature', 'Load More products')
def load_more_products():
    pass

@when('I press an arrow')
def step_press_arrow():
    pass

@then('I should see a list of new products')
def step_see_new_products():
    pass