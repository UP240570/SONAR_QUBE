import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    """Fixture del driver de Chrome. Se crea antes de cada prueba
    y se cierra automáticamente al terminar (gracias al yield)."""
    options = Options()
    options.add_argument("--headless=new")  # quita esta línea si quieres ver el navegador
    options.add_argument("--window-size=1280,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(3)

    yield drv

    drv.quit()
