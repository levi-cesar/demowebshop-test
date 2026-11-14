from decimal import Decimal

from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage


def test_ct01_pesquisar_produto(driver, base_url):
    catalog = CatalogPage(driver, base_url).open()

    catalog.search("laptop")

    assert driver.current_url == f"{base_url}/search?q=laptop"
    assert catalog.title == "Search"
    assert "14.1-inch Laptop" in catalog.product_names


def test_ct02_navegar_ate_subcategoria(driver, base_url):
    catalog = CatalogPage(driver, base_url).open()

    catalog.open_computers()

    assert driver.current_url == f"{base_url}/computers"
    assert set(catalog.subcategories) == {"Desktops", "Notebooks", "Accessories"}

    catalog.open_notebooks()

    assert driver.current_url == f"{base_url}/notebooks"
    assert catalog.title == "Notebooks"
    assert catalog.breadcrumb == ["HOME", "COMPUTERS", "NOTEBOOKS"]


def test_ct04_filtrar_produtos_por_preco(driver, base_url):
    catalog = CatalogPage(driver, base_url).open("/books")

    catalog.filter_under_25()

    assert driver.current_url == f"{base_url}/books?price=-25"
    assert all(price < Decimal("25.00") for price in catalog.prices)
    assert "Science" not in catalog.product_names

    catalog.remove_filter()

    assert driver.current_url == f"{base_url}/books"
    assert "Science" in catalog.product_names


def test_ct06_atualizar_quantidade_no_carrinho(driver, base_url, cart_with_laptop):
    cart = cart_with_laptop

    cart.update_laptop_quantity(3)

    assert driver.current_url == f"{base_url}/cart"
    assert cart.laptop_total == Decimal("4770.00")
    assert cart.subtotal == Decimal("4770.00")
    assert cart.cart_quantity == "(3)"


def test_ct07_recusar_cupom_invalido(driver, base_url, cart_with_laptop):
    cart = cart_with_laptop
    original_total = cart.total

    message = cart.apply_coupon("CUPOMINVALIDO")

    assert message == "The coupon code you entered couldn't be applied to your order"
    assert cart.total == original_total
    assert driver.current_url == f"{base_url}/cart"


def test_ct11_exibir_produtos_vistos_recentemente(driver, base_url):
    product = ProductPage(driver, base_url)
    product.open("/141-inch-laptop")
    product.open("/fiction")

    recently_viewed = product.open_recently_viewed()

    assert driver.current_url == f"{base_url}/recentlyviewedproducts"
    assert recently_viewed.title == "Recently viewed products"
    assert recently_viewed.product_names == ["Fiction", "14.1-inch Laptop"]
