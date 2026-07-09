import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_login_exitoso(driver):
    """Caso válido: credenciales correctas llevan al dashboard."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("admin", "admin123")

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_loaded()
    assert "admin" in dashboard_page.get_welcome_text()


def test_login_credenciales_incorrectas(driver):
    """Caso de error: contraseña incorrecta."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("admin", "clave_mala")

    error = login_page.get_error_message()
    assert "incorrectos" in error.lower()


def test_login_usuario_vacio(driver):
    """Caso de frontera: usuario vacío."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("", "admin123")

    error = login_page.get_error_message()
    assert "obligatorios" in error.lower()


def test_login_password_vacio(driver):
    """Caso de frontera: contraseña vacía."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("admin", "")

    error = login_page.get_error_message()
    assert "obligatorios" in error.lower()


def test_login_usuario_no_existente(driver):
    """Caso de error: usuario que no existe en el sistema."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("usuario_fantasma", "cualquierpwd")

    error = login_page.get_error_message()
    assert "incorrectos" in error.lower()


def test_logout(driver):
    """Caso válido: logout regresa a la pantalla de login."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("admin", "admin123")

    dashboard_page = DashboardPage(driver)
    dashboard_page.is_loaded()
    dashboard_page.logout()

    login_page.open()
    assert driver.find_element(*LoginPage.LOGIN_BUTTON) is not None


@pytest.mark.parametrize("username,password,resultado_esperado", [
    ("admin", "admin123", "exito"),
    ("user1", "password1", "exito"),
    ("admin", "wrongpass", "incorrectos"),
    ("", "admin123", "obligatorios"),
    ("admin", "", "obligatorios"),
    ("nouser", "nopass", "incorrectos"),
])
def test_login_data_driven(driver, username, password, resultado_esperado):
    """Prueba data-driven: varias combinaciones de usuario/contraseña."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    if resultado_esperado == "exito":
        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_loaded()
    else:
        error = login_page.get_error_message()
        assert resultado_esperado in error.lower()
