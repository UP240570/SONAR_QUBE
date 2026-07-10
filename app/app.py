import os
import itertools
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-in-development")
# "Base de datos" en memoria solo para fines de demostración
USERS = {
    "admin": "admin123",
    "user1": "password1",
}

# Tareas por usuario: { "admin": [{"id": 1, "text": "Comprar leche", "done": False}, ...] }
TASKS = {}
_task_id_counter = itertools.count(1)


def get_user_tasks(username):
    return TASKS.setdefault(username, [])


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            error = "Usuario y contraseña son obligatorios"
        elif username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    tasks = get_user_tasks(session["user"])
    return render_template("dashboard.html", user=session["user"], tasks=tasks)


@app.route("/tasks/add", methods=["POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("login"))
    text = request.form.get("task_text", "").strip()
    if text:
        tasks = get_user_tasks(session["user"])
        tasks.append({"id": next(_task_id_counter), "text": text, "done": False})
    return redirect(url_for("dashboard"))


@app.route("/tasks/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    if "user" not in session:
        return redirect(url_for("login"))
    tasks = get_user_tasks(session["user"])
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
    return redirect(url_for("dashboard"))


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user" not in session:
        return redirect(url_for("login"))
    tasks = get_user_tasks(session["user"])
    TASKS[session["user"]] = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
