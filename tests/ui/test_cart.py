def LoginPage():
    pass


def ProductPage():
    pass


def CartPage():
    pass


def test_add_cart(browser):  # browser是pytest-selenium提供的fixture
    login_page = LoginPage(browser)
    login_page.login("test_user", "pass123")

    product_page = ProductPage(browser)
    product_page.add_to_cart("iPhone 15")

    cart_page = CartPage(browser)
    assert "iPhone 15" in cart_page.get_items()