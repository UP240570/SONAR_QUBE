import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture
def dashboard(driver):
    """Fixture que ya deja la sesión iniciada y en el dashboard."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("admin", "admin123")

    dashboard_page = DashboardPage(driver)
    dashboard_page.is_loaded()
    return dashboard_page


def test_agregar_tarea(dashboard):
    """Caso válido: agregar una tarea nueva la muestra en la lista."""
    dashboard.add_task("Comprar leche")
    tareas = dashboard.get_task_texts()
    assert "Comprar leche" in tareas


def test_agregar_tarea_vacia_no_se_agrega(dashboard):
    """Caso de frontera: texto vacío no debe crear una tarea."""
    tareas_antes = len(dashboard.get_task_texts())
    dashboard.add_task("   ")
    tareas_despues = len(dashboard.get_task_texts())
    assert tareas_despues == tareas_antes


def test_marcar_tarea_completada(dashboard):
    """Caso válido: marcar el checkbox cambia el estado a completada."""
    dashboard.add_task("Lavar el carro")
    ultimo_index = len(dashboard.get_task_texts()) - 1
    dashboard.toggle_task_by_index(ultimo_index)
    assert dashboard.is_task_done(ultimo_index)


def test_eliminar_tarea(dashboard):
    """Caso válido: eliminar una tarea reduce el total de tareas en 1."""
    dashboard.add_task("Tarea temporal")
    tareas_antes = len(dashboard.get_task_texts())
    dashboard.delete_task_by_index(tareas_antes - 1)
    tareas_despues = len(dashboard.get_task_texts())
    assert tareas_despues == tareas_antes - 1


def test_login_requerido_para_ver_tareas(driver):
    """Caso de error: sin sesión iniciada, no se puede ver el dashboard."""
    driver.get("http://localhost:5000/dashboard")
    login_page = LoginPage(driver)
    # Flask redirige a /login si no hay sesión activa
    assert "login" in driver.current_url


@pytest.mark.parametrize("texto_tarea", [
    "Estudiar para el examen",
    "Hacer ejercicio",
    "Leer un libro",
])
def test_agregar_varias_tareas_parametrizado(dashboard, texto_tarea):
    """Prueba data-driven: agrega varias tareas distintas."""
    dashboard.add_task(texto_tarea)
    tareas = dashboard.get_task_texts()
    assert texto_tarea in tareas
