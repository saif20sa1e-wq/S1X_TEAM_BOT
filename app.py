from flask import Flask, render_template, request, redirect, session, jsonify
import threading, time, json

app = Flask(__name__)
app.secret_key = "super_secret"

USERNAME = "saif2026"
PASSWORD = "saif2026"

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def level_system(user_id, hours):
    data = load_data()
    total_seconds = hours * 3600
    start = time.time()

    while time.time() - start < total_seconds:
        time.sleep(1)
        elapsed = int(time.time() - start)
        progress = int((elapsed / total_seconds) * 100)

        data[user_id]["progress"] = progress
        data[user_id]["xp"] += 50
        data[user_id]["level"] = data[user_id]["xp"] // 1000
        data[user_id]["remaining"] = total_seconds - elapsed

        save_data(data)

    data[user_id]["status"] = "finished"
    save_data(data)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["login"] = True
            return redirect("/dashboard")
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("login"):
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/start", methods=["POST"])
def start():
    user_id = request.form["user_id"]
    hours = int(request.form["hours"])

    data = load_data()
    data[user_id] = {
        "xp": 0,
        "level": 1,
        "progress": 0,
        "remaining": hours * 3600,
        "status": "running"
    }
    save_data(data)

    thread = threading.Thread(target=level_system, args=(user_id, hours))
    thread.start()

    return jsonify({"success": True})

@app.route("/status/<user_id>")
def status(user_id):
    data = load_data()
    return jsonify(data.get(user_id, {}))

if __name__ == "__main__":
    app.run(debug=True)