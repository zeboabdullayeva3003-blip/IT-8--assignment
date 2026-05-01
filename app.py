from flask import Flask, request, redirect
import os, json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "feedback_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f0f13;color:#f0eee8;font-family:'DM Sans',sans-serif;min-height:100vh}
nav{display:flex;justify-content:space-between;align-items:center;padding:1.4rem 3rem;border-bottom:1px solid #2a2a3a;background:rgba(15,15,19,0.95);position:sticky;top:0}
.logo{font-family:'Playfair Display',serif;font-size:1.4rem;color:#e8c97d;text-decoration:none}
.nav-links a{color:#8a8a9a;text-decoration:none;margin-left:2rem;font-size:0.9rem;text-transform:uppercase;letter-spacing:0.05em}
.hero{padding:5rem 3rem 3rem;max-width:900px;margin:0 auto}
.tag{display:inline-block;background:rgba(232,201,125,0.12);color:#e8c97d;border:1px solid rgba(232,201,125,0.3);padding:0.3rem 0.9rem;border-radius:20px;font-size:0.78rem;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1.2rem}
h1{font-family:'Playfair Display',serif;font-size:3.5rem;line-height:1.05;margin-bottom:1rem}
.hero p{color:#8a8a9a;font-size:1.05rem;max-width:480px;line-height:1.7}
.form-section{padding:0 3rem 4rem;max-width:900px;margin:0 auto}
.card{background:#1a1a24;border:1px solid #2a2a3a;border-radius:16px;padding:2.5rem}
.card h2{font-family:'Playfair Display',serif;font-size:1.6rem;margin-bottom:2rem;color:#e8c97d}
.form-group{margin-bottom:1.5rem}
label{display:block;font-size:0.85rem;letter-spacing:0.06em;text-transform:uppercase;color:#8a8a9a;margin-bottom:0.5rem}
input[type=text],textarea{width:100%;background:#0f0f13;border:1px solid #2a2a3a;border-radius:8px;padding:0.85rem 1rem;color:#f0eee8;font-family:'DM Sans',sans-serif;font-size:0.95rem}
textarea{resize:vertical}
.rating-group{display:flex;gap:0.6rem;flex-wrap:wrap}
.rating-label input[type=radio]{display:none}
.star-btn{display:block;padding:0.55rem 1rem;border:1px solid #2a2a3a;border-radius:8px;cursor:pointer;font-size:0.9rem;background:#0f0f13;color:#f0eee8}
.rating-label input[type=radio]:checked+.star-btn{background:#e8c97d;color:#0f0f13;border-color:#e8c97d;font-weight:500}
.btn{background:#e8c97d;color:#0f0f13;border:none;padding:0.9rem 2rem;border-radius:8px;font-size:0.95rem;font-weight:500;cursor:pointer;margin-top:0.5rem}
.stats-row{display:flex;gap:1.5rem;padding:0 3rem 2rem;max-width:900px;margin:0 auto}
.stat-card{flex:1;background:#1a1a24;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;text-align:center}
.stat-number{font-family:'Playfair Display',serif;font-size:2.5rem;color:#e8c97d}
.stat-label{color:#8a8a9a;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.06em;margin-top:0.3rem}
.results-section{padding:0 3rem 4rem;max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:1rem}
.result-card{background:#1a1a24;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem}
.result-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.8rem}
.course-tag{display:inline-block;background:rgba(125,212,232,0.1);color:#7dd4e8;border:1px solid rgba(125,212,232,0.25);padding:0.15rem 0.6rem;border-radius:6px;font-size:0.78rem;margin-left:0.7rem}
.rating-badge{background:rgba(232,201,125,0.12);color:#e8c97d;padding:0.2rem 0.7rem;border-radius:6px;font-size:0.9rem;font-weight:500}
.comment{color:#8a8a9a;font-style:italic;font-size:0.95rem;line-height:1.6;margin-bottom:0.6rem}
.timestamp{font-size:0.78rem;color:rgba(138,138,154,0.6)}
.about-section{padding:0 3rem 4rem;max-width:900px;margin:0 auto}
.about-section p{color:#8a8a9a;line-height:1.8;margin-bottom:1rem}
.about-section h3{font-size:1rem;font-weight:500;text-transform:uppercase;color:#8a8a9a;margin:2rem 0 1rem;letter-spacing:0.05em}
.tech-list{list-style:none;display:flex;flex-direction:column;gap:0.7rem}
.tech-list li{color:#8a8a9a;display:flex;align-items:center;gap:0.7rem}
.tech-badge{background:rgba(232,201,125,0.12);color:#e8c97d;border:1px solid rgba(232,201,125,0.25);padding:0.2rem 0.6rem;border-radius:6px;font-size:0.8rem;min-width:80px;text-align:center}
.empty{text-align:center;padding:4rem;color:#8a8a9a}
footer{padding:1.5rem 3rem;border-top:1px solid #2a2a3a;text-align:center;color:#8a8a9a;font-size:0.82rem}
</style>"""

NAV = "<nav><a class='logo' href='/'>EduFeedback</a><div class='nav-links'><a href='/'>Submit</a><a href='/results'>Results</a><a href='/about'>About</a></div></nav>"
FOOTER = "<footer>Cloud Technologies Assignment &mdash; Deployed on Render.com &mdash; Zebo Abdullayeva</footer>"

def page(content):
    return f"<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>EduFeedback</title>{CSS}</head><body>{NAV}{content}{FOOTER}</body></html>"

@app.route("/")
def index():
    content = """
    <section class='hero'><div><span class='tag'>Cloud-Hosted App</span>
    <h1>Course Feedback<br>Portal</h1>
    <p>Share your experience with your courses.</p></div></section>
    <section class='form-section'><div class='card'>
    <h2>Submit Your Feedback</h2>
    <form action='/submit' method='POST'>
    <div class='form-group'><label>Full Name *</label><input type='text' name='name' placeholder='e.g. Ali Karimov' required></div>
    <div class='form-group'><label>Course Name *</label><input type='text' name='course' placeholder='e.g. Introduction to IT' required></div>
    <div class='form-group'><label>Rating *</label><div class='rating-group'>
    <label class='rating-label'><input type='radio' name='rating' value='1' required><span class='star-btn'>1★</span></label>
    <label class='rating-label'><input type='radio' name='rating' value='2'><span class='star-btn'>2★</span></label>
    <label class='rating-label'><input type='radio' name='rating' value='3'><span class='star-btn'>3★</span></label>
    <label class='rating-label'><input type='radio' name='rating' value='4'><span class='star-btn'>4★</span></label>
    <label class='rating-label'><input type='radio' name='rating' value='5'><span class='star-btn'>5★</span></label>
    </div></div>
    <div class='form-group'><label>Comments</label><textarea name='comment' rows='4' placeholder='What did you think?'></textarea></div>
    <button type='submit' class='btn'>Submit Feedback →</button>
    </form></div></section>"""
    return page(content)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    course = request.form.get("course", "").strip()
    rating = request.form.get("rating", "").strip()
    comment = request.form.get("comment", "").strip()
    if not name or not course or not rating:
        return redirect("/")
    entry = {"name": name, "course": course, "rating": int(rating),
             "comment": comment, "timestamp": datetime.now().strftime("%B %d, %Y at %H:%M")}
    data = load_data()
    data.append(entry)
    save_data(data)
    return redirect("/results")

@app.route("/results")
def results():
    data = load_data()
    avg = round(sum(e["rating"] for e in data) / len(data), 1) if data else 0
    cards = ""
    for e in data[::-1]:
        comment = f"<p class='comment'>\"{e['comment']}\"</p>" if e.get("comment") else ""
        cards += f"<div class='result-card'><div class='result-header'><div><strong>{e['name']}</strong><span class='course-tag'>{e['course']}</span></div><div class='rating-badge'>{e['rating']}★</div></div>{comment}<p class='timestamp'>{e['timestamp']}</p></div>"
    if not cards:
        cards = "<div class='empty'>No feedback yet. <a href='/' style='color:#e8c9
