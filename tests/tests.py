import time
from decimal import Decimal

from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.compare_products_page import CompareProductsPage

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

def test_ct03_ordenar_produtos_pelo_maior_preco(driver, base_url):
    catalog = CatalogPage(driver, base_url).open("/books")

    assert driver.current_url == f"{base_url}/books"

    catalog.sort_products('Price: High to Low')

    assert catalog.prices == sorted(catalog.prices, reverse=True)
    assert driver.current_url == f"{base_url}/books?orderby=11"
    assert catalog.product_names[0] == "Science"
    assert catalog.prices[0] == Decimal("51.00")


def test_ct04_filtrar_produtos_por_preco(driver, base_url):
    catalog = CatalogPage(driver, base_url).open("/books")

    catalog.filter_under_25()

    assert driver.current_url == f"{base_url}/books?price=-25"
    assert all(price < Decimal("25.00") for price in catalog.prices)
    assert "Science" not in catalog.product_names

    catalog.remove_filter()

    assert driver.current_url == f"{base_url}/books"
    assert "Science" in catalog.product_names

def test_ct05_configurar_computador_e_adicionar_ao_carrinho(driver, base_url):
    product = ProductPage(driver, base_url).open("/build-your-own-computer")
    cart = CartPage(driver, base_url)

    # Pré-condições: carrinho vazio e preço base 1200.00
    assert cart.cart_quantity == "(0)", f"Esperado carrinho vazio '(0)', mas estava '{cart.cart_quantity}'"
    assert product.price == Decimal("1200.00")

    # Passo 1: Selecionar as opções da tabela de dados de teste
    (
        product
        .desktop_select_processor("14")  # 2.5 GHz Intel Pentium Dual-Core E2200 [+15.00]
        .desktop_select_ram("17")  # 8GB [+60.00]
        .desktop_select_hdd("19")  # 400 GB [+100.00]
        .desktop_select_os("21")  # Windows 10 [+60.00]
        .desktop_select_software(["22"])  # Microsoft Office [+50.00] (somente esta opção)
    )

    # Passo 2: Clicar em Add to cart e validar notificação e cabeçalho
    product.add_to_cart()
    assert "The product has been added to your shopping cart" in product.notification_text
    assert product.header_cart_text == "Shopping cart\n(1)"

    # Passo 3: Clicar em Shopping cart no cabeçalho
    cart = product.open_cart()

    # Resultados esperados no carrinho
    assert driver.current_url == f"{base_url}/cart"

    attributes = cart.product_attributes("Build your own computer")
    assert "2.5 GHz Intel Pentium Dual-Core E2200 [+15.00]" in attributes
    assert "8GB [+60.00]" in attributes
    assert "400 GB [+100.00]" in attributes
    assert "Windows 10 [+60.00]" in attributes
    assert "Microsoft Office [+50.00]" in attributes
    assert "Acrobat Reader" not in attributes
    assert "Total Commander" not in attributes

    expected_price = Decimal("1485.00")
    assert cart.product_unit_price("Build your own computer") == expected_price
    assert cart.subtotal == expected_price
    assert cart.total == expected_price

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

def test_ct10_comparar_dois_produtos(driver, base_url):
    expected_compare_url = f"{base_url.rstrip('/')}/compareproducts"

    # Pré-condição: lista de comparação vazia
    compare_page = CompareProductsPage(driver, base_url).open("/compareproducts")
    assert compare_page.is_empty, "A lista de comparação deveria iniciar vazia."

    # Passo 1: Abrir produto 1 e clicar em Add to compare list
    product = ProductPage(driver, base_url).open("/141-inch-laptop")
    compare_page = product.add_to_compare_list()
    assert driver.current_url == expected_compare_url

    # Passo 2: Abrir produto 2 e clicar em Add to compare list
    product.open("/fiction")
    compare_page = product.add_to_compare_list()
    assert driver.current_url == expected_compare_url

    # Resultados esperados na tabela de comparação
    assert compare_page.product_names == ["Fiction", "14.1-inch Laptop"]
    assert compare_page.product_prices == [Decimal("24.00"), Decimal("1590.00")]
    assert compare_page.is_clear_list_visible

def test_ct11_exibir_produtos_vistos_recentemente(driver, base_url):
    product = ProductPage(driver, base_url)
    product.open("/141-inch-laptop")
    product.open("/fiction")

    recently_viewed = product.open_recently_viewed()

    assert driver.current_url == f"{base_url}/recentlyviewedproducts"
    assert recently_viewed.title == "Recently viewed products"
    assert recently_viewed.product_names == ["Fiction", "14.1-inch Laptop"]
