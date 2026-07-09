# Proyecto Login QA — Selenium + SonarQube

Proyecto de ejemplo (login con Flask) ya estructurado para cumplir el
**Examen Práctico Unidad 2 — Estándares y Métricas de Desarrollo de Software (TIID05C)**.

Úsalo como plantilla: cambia `app/` por tu propio sistema (o deja este login
si aún no tienes proyecto) y ajusta los `pages/*.py` a los IDs/elementos reales.

## 1. Estructura del proyecto

```
proyecto_login/
├── app/                    # Sistema bajo prueba (Flask)
│   ├── app.py
│   └── templates/
│       ├── login.html
│       └── dashboard.html
├── pages/                  # Page Objects (POM)
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/                  # Pruebas Selenium
│   └── test_login.py
├── conftest.py             # Fixture del driver
├── requirements.txt
├── pytest.ini
├── sonar-project.properties
└── .github/workflows/ci.yml   # Bonus: CI
```

## 2. Instalación

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Necesitas **Google Chrome** instalado. Selenium 4.23+ ya trae su propio
gestor de driver (Selenium Manager), no necesitas descargar chromedriver a mano.

## 3. Levantar la app (en una terminal)

```bash
python app/app.py
```

Se abre en `http://localhost:5000`. Usuarios de prueba:
| usuario | contraseña |
|---------|------------|
| admin   | admin123   |
| user1   | password1  |

### Nueva funcionalidad: lista de tareas en el Dashboard

Después de iniciar sesión, el dashboard (`/dashboard`) muestra una lista de
tareas **propia de cada usuario** (si entras con `admin` ves solo las tareas
de `admin`; si entras con `user1`, ves solo las de `user1`).

- Agregar tarea: campo de texto + botón "Agregar" (`#task-input`, `#add-task-btn`)
- Marcar como completada: checkbox junto a cada tarea (tacha el texto)
- Eliminar tarea: botón "Eliminar" junto a cada tarea
- Si no hay tareas, se muestra el mensaje "No tienes tareas pendientes."
- Si accedes a `/dashboard` sin haber iniciado sesión, te redirige a `/login`

Las tareas se guardan **en memoria** (se pierden si reinicias el servidor de
Flask) — es suficiente para el examen, no está pensado para producción.

## 4. Correr las pruebas (Parte A del examen)

En otra terminal, con la app corriendo:

```bash
# Ejecución simple
pytest -v

# Con reporte HTML (Parte A, punto 5)
pytest --html=reports/report.html --self-contained-html

# Con cobertura para conectar a SonarQube (Parte B, punto 4)
pytest --cov=app --cov=pages --cov-report=xml:coverage.xml
```

Si quieres ver el navegador en acción (para la demo en video), quita la
línea `options.add_argument("--headless=new")` en `conftest.py`.

## 5. Análisis con SonarQube (Parte B)

1. Levanta SonarQube localmente con Docker:
   ```bash
   docker run -d --name sonarqube -p 9000:9000 sonarqube:community
   ```
2. Entra a `http://localhost:9000` (usuario/clave por defecto: `admin`/`admin`,
   te pedirá cambiarla) y genera un **token** en
   *My Account > Security > Generate Token*.
3. Descarga **sonar-scanner** ([docs oficiales](https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonar-scanner/)).
4. Corre el análisis desde la raíz del proyecto (ya tienes `coverage.xml` del paso 4):
   ```bash
   sonar-scanner -Dsonar.login=TU_TOKEN
   ```
5. En el tablero verás las 5 dimensiones (Reliability, Security,
   Maintainability, Coverage, Duplications), los issues detectados y si el
   Quality Gate quedó en **Passed** o **Failed**.
6. Corrige al menos 2 issues en el código, guarda capturas de antes/después,
   y vuelve a correr `sonar-scanner` para confirmar que se resolvieron.

## 6. Checklist de la rúbrica (100 pts)

- [ ] Estructura `pages/` + `tests/` + `conftest.py` ✅ (ya incluida)
- [ ] ≥2 Page Objects ✅ (`LoginPage`, `DashboardPage`)
- [ ] ≥5 pruebas variadas (válidas/frontera/error) con `WebDriverWait` ✅ (`test_login.py`: 6 pruebas + `test_tasks.py`: 5 pruebas)
- [ ] ≥1 prueba con `@pytest.mark.parametrize` ✅ (`test_login_data_driven` y `test_agregar_varias_tareas_parametrizado`)
- [ ] Reporte HTML en verde → correr `pytest --html=...` y revisar que no haya fallos
- [ ] `sonar-project.properties` + análisis corrido → **pendiente de que tú lo ejecutes**
- [ ] Captura de las 5 dimensiones → **pendiente**
- [ ] ≥3 issues documentados (tipo, severidad, regla, línea) → **pendiente**
- [ ] ≥2 issues corregidos con antes/después → **pendiente**
- [ ] Coverage conectado + captura del % → correr con `--cov-report=xml`
- [ ] Quality Gate explicado (Passed/Failed y por qué) → **pendiente**
- [ ] Video demo (≤10 min): pytest en vivo + explicar un issue en Sonar
- [ ] PDF de evidencias con capturas numeradas + aportes por integrante
- [ ] Bonus: pipeline CI ✅ (ya incluido en `.github/workflows/ci.yml`, solo
      necesitas subir el repo a GitHub y configurar los secrets
      `SONAR_TOKEN` y `SONAR_HOST_URL`)

## 7. Notas para adaptarlo a TU proyecto real

Si tu proyecto integrador de la Unidad 1 no es este login de ejemplo:
- Sustituye `app/` por tu aplicación real (o simplemente apunta
  `LoginPage.URL` a la URL de tu app ya desplegada).
- Cambia los `By.ID` de `pages/*.py` por los selectores reales de tu HTML
  (ID, CSS selector, XPath — usa el inspector del navegador).
- Ajusta `sonar.sources` en `sonar-project.properties` a las carpetas de tu
  código fuente real.
- Mantén la misma lógica de fixture (`conftest.py`) y de esperas explícitas
  (`WebDriverWait`), son requisito del examen.
