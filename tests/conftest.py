import os

import pytest
from selenium import webdriver

from pages.product_page import ProductPage


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Exibe a janela do Chrome")
    parser.addoption(
        "--base-url", default="https://demowebshop.tricentis.com",
        help="Endereço da aplicação sob teste",
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture
def driver(request):
    # Um navegador novo por teste mantém cookies e listas independentes.
    os.environ.setdefault("SE_CACHE_PATH", str(request.config.rootpath / ".cache" / "selenium"))
    options = webdriver.ChromeOptions()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(45)
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def cart_with_laptop(driver, base_url):
    """Cria a pré-condição do carrinho dentro do navegador de cada teste."""
    product = ProductPage(driver, base_url).open("/141-inch-laptop")
    return product.add_to_cart().open_cart()
