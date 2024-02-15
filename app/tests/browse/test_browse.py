"""
Step definitions for browse.feature
"""
import os
import pytest
import random
from pytest_bdd import given, when, then, scenario
from bs4 import BeautifulSoup
from flaskr.db import execute_script
from flaskr.store import LIMIT as MAX_PRODUCTS_PER_PAGE
from definitions import APP_DIR


def get_products_from_soup(soup):
    catalog = {}
    for item in soup.find_all(attrs={'data-type': 'product'}):
        name = item.find(attrs={'data-type': 'product name'})
        desc = item.find(attrs={'data-type': 'product description'})
        price = item.find(attrs={'data-type': 'product price'})
        image = item.find(attrs={'data-type': 'product image'})

        catalog[name.text]={
            'desc':desc.text,
            'price':price.text,
            'image':image['src'],
            'product url':item.get('href')
        }
    return catalog

@pytest.fixture
def catalog():
    return {}

@pytest.fixture
def new_catalog():
    return {}

@pytest.fixture
def test_response():
    return None

@scenario('browse.feature', 'Render Products')
def test_render_products():
    pass

@given('I have a catalog')
def step_have_catalog(app):
    with app.app_context():
        execute_script(os.path.join(APP_DIR,'sql','catalog.sql'))

@when('I enter the catalog', target_fixture='catalog')
def step_enter_catalog(client):
    response = client.get("/")
    soup = BeautifulSoup(response.data, 'html.parser')
    catalog = get_products_from_soup(soup)
    return catalog

@then('I should see the available products')
def step_see_available_products(catalog):
    """
    Assumes you have at least one full page of products
    """
    # compare loaded catalog with test data ... assert 
    from_sql = {}
    with open(os.path.join(APP_DIR,'sql','catalog.sql'),'r',encoding='utf-8') as f:
        for line in f:
            if len(line.lstrip()) > 0 and line.lstrip()[0] == '(':
                split = line.replace("'", " ").split(',')
                from_sql[split[1].strip()]={
                'desc':split[2].strip(),
                'price':split[3].strip(),
                'image':split[4].strip()
                }

    for i,k in enumerate(from_sql.keys()):
        if i >= MAX_PRODUCTS_PER_PAGE:
            break
        assert k in catalog.keys()
        assert from_sql[k]['desc'] == catalog[k]['desc']

@scenario('browse.feature', 'Visiting the product information page')
def test_visiting_the_product_information_page():
    pass

@when('I press a product link', target_fixture='test_response')
def step_press_product_link(client,catalog):
    product = catalog[random.choice(list(catalog.keys()))]
    response = client.get(product['product url'])
    return response
    

@then('I should see the product information page')
def step_see_product_info_page(test_response):
    assert test_response.status_code == 200

@scenario('browse.feature', 'Load More products')
def test_load_more_products():
    pass

@when('I press an arrow', target_fixture='new_catalog')
def step_press_arrow(client):
    response = client.get('/?page=2')
    soup = BeautifulSoup(response.data, 'html.parser')
    catalog = get_products_from_soup(soup)
    return catalog

@then('I should see a list of new products')
def step_see_new_products(catalog, new_catalog):
    assert new_catalog != catalog