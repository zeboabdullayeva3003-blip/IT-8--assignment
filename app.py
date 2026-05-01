from flask import Flask, render_template, request, redirect, url_for
import os, json
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.')

DATA_FILE = "feedback_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    course = request.form.get("course", "").strip()
    rating = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()
    if not name or not course or not rating:
        return render_template("index.html", error="Please fill in all required fields.")
    entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "name": name, "course": course, "rating": int(rating),
        "comment": comment,
        "timestamp": datetime.now().strftime("%B %d, %Y at %H:%M")
    }
    data = load_data()
    data.append(entry)
    save_data(data)
    return redirect(url_for("results"))

@app.route("/results")
def results():
    data = load_data()
    avg_rating = round(sum(e["rating"] for e in data) / len(data), 1) if data else 0
    return render_template("results.html", entries=data[::-1], avg_rating=avg_rating, total=len(data))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
