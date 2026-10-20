import os

import requests
from flask import Flask, redirect, render_template_string, request

# Config comes from the environment (set in config/frontend/deployment.yaml)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001")

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Task Board</title>
<h1>Task Board</h1>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
<form method="post" action="/add">
  <input name="title" placeholder="New task" required>
  <button>Add</button>
</form>
<ul>{% for t in tasks %}<li>{{ t.title }}</li>{% endfor %}</ul>
"""


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/")
def index():
    try:
        tasks = requests.get(f"{BACKEND_URL}/api/tasks", timeout=5).json()
        return render_template_string(PAGE, tasks=tasks, error=None)
    except requests.RequestException:
        return render_template_string(PAGE, tasks=[], error="Backend unreachable")


@app.post("/add")
def add():
    requests.post(f"{BACKEND_URL}/api/tasks", json={"title": request.form["title"]}, timeout=5)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
