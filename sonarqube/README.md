# SonarQube en marcha — materiales de clase (S8.1)

Materiales para **levantar SonarQube y obtener el primer análisis** del proyecto de
pruebas Selenium/SauceDemo. Acompaña a la presentación `semana08_s1_simple`.

Estos scripts operan sobre el proyecto padre (`semana07_s2_selenium/`), donde está
`sonar-project.properties` y el código a analizar (`pages/`, `tests/`).

## Requisitos

- **Docker Desktop** instalado y **abierto** (ícono verde).
- ~2 GB de RAM libres y el **puerto 9000** libre.
- El proyecto Selenium con su entorno (no es necesario correr las pruebas para la S8.1).

> **Windows / Mac vs Linux (¡importante!)**
> El contenedor del *scanner* necesita alcanzar el servidor. En **Windows y Mac** se usa
> `http://host.docker.internal:9000`. En **Linux** se usa `http://localhost:9000` con
> `--network host`. Los scripts `.ps1` ya usan la variante de Windows/Mac; los `.sh`, la de Linux.

---

## Flujo en clase (Windows / PowerShell)

### 1. Verificar prerrequisitos
```powershell
./sonarqube/01_verificar.ps1
```
Comprueba Docker, el daemon, el puerto 9000 y Python.

### 2. Levantar el servidor
```powershell
./sonarqube/02_levantar.ps1
```
Lanza el contenedor `sonarqube:community` y espera a que el tablero responda.
Abre luego **http://localhost:9000** (usuario `admin`, contraseña `admin`).

### 3. Cambiar la contraseña y generar el token
En el navegador: cambia la contraseña inicial y ve a
**My Account → Security → Generate Token**. Copia el token (`sqp_...`).

### 4. Ejecutar el análisis
Pasa el token por variable de entorno (NO lo escribas en el archivo de config):
```powershell
$env:SONAR_TOKEN = "sqp_pega_aqui_tu_token"
./sonarqube/03_analizar.ps1
```
Al terminar verás `EXECUTION SUCCESS` y la URL del tablero:
`http://localhost:9000/dashboard?id=selenium-saucedemo`

---

## Flujo equivalente en Linux / Mac (bash)
```bash
./sonarqube/01_verificar.sh
./sonarqube/02_levantar.sh
export SONAR_TOKEN="sqp_pega_aqui_tu_token"
./sonarqube/03_analizar.sh
```

---

## Comandos manuales (si prefieres no usar los scripts)

```powershell
# Servidor
docker run -d --name sonarqube -p 9000:9000 sonarqube:community

# Analisis (Windows/Mac). El scanner corre desde la RAIZ del proyecto.
docker run --rm -v "${PWD}:/usr/src" `
  -e SONAR_HOST_URL=http://host.docker.internal:9000 `
  -e SONAR_TOKEN=$env:SONAR_TOKEN `
  sonarsource/sonar-scanner-cli
```

```bash
# Analisis (Linux)
docker run --rm --network host -v "$PWD:/usr/src" \
  -e SONAR_HOST_URL=http://localhost:9000 \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  sonarsource/sonar-scanner-cli
```

## Limpieza al terminar la clase
```powershell
docker stop sonarqube ; docker rm sonarqube
```

## Troubleshooting rápido

| Síntoma | Causa / solución |
|---|---|
| `cannot connect to the Docker daemon` | Docker Desktop no está abierto. |
| Contenedor se cae (`Exited`) | Falta RAM; dale ≥2 GB a Docker (Settings → Resources). |
| Tablero no carga en `:9000` | Espera 1–2 min; revisa que el puerto esté libre. |
| Scanner `401 Unauthorized` | Token mal pegado o `SONAR_TOKEN` no definido. |
| Scanner `Connection refused` | En Windows/Mac usa `host.docker.internal`, no `localhost`. |
| `0 files indexed` | `sonar.sources` mal; debe ser `pages`. |
