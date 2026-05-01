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

def page(body):
    return f"""<!DOCTYPE html><html><head><meta charset='UTF-8'>
<title>EduFeedback</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f13;color:#f0eee8;font-family:sans-serif;min-height:100vh}}
nav{{display:flex;justify-content:space-between;align-items:center;padding:1rem 2rem;border-bottom:1px solid #2a2a3a;background:#0f0f13}}
.logo{{color:#e8c97d;text-decoration:none;font-size:1.3rem;font-weight:bold}}
nav a{{color:#8a8a9a;text-decoration:none;margin-left:1.5rem}}
.wrap{{max-width:800px;margin:0 auto;padding:3rem 2rem}}
h1{{font-size:2.5rem;margin-bottom:1rem;color:#e8c97d}}
p{{color:#8a8a9a;margin-bottom:1.5rem;line-height:1.7}}
.card{{background:#1a1a24;border:1px solid #2a2a3a;border-radius:12px;padding:2rem;margin-bottom:1rem}}
label{{display:block;font-size:0.85rem;text-transform:uppercase;color:#8a8a9a;margin-bottom:0.4rem;margin-top:1rem}}
input,textarea{{width:100%;background:#0f0f13;border:1px solid #2a2a3a;border-radius:8px;padding:0.75rem;color:#f0eee8;font-size:0.95rem}}
.stars{{display:flex;gap:0.5rem;margin-top:0.4rem}}
.stars input{{display:none}}
.stars label{{background:#0f0f13;border:1px solid #2a2a3a;border-radius:8px;padding:0.5rem 1rem;cursor:pointer;text-transform:none;font-size:0.9rem;margin:0}}
.stars input:checked+label{{background:#e8c97d;color:#0f0f13;border-color:#e8c97d;font-weight:bold}}
.btn{{background:#e8c97d;color:#0f0f13;border:none;padding:0.85rem 2rem;border-radius:8px;font-size:0.95rem;font-weight:bold;cursor:pointer;margin-top:1.5rem}}
.badge{{display:inline-block;background:rgba(232,201,125,0.15);color:#e8c97d;border:1px solid rgba(232,201,125,0.3);padding:0.2rem 0.6rem;border-radius:6px;font-size:0.8rem}}
.stats{{display:flex;gap:1rem;margin-bottom:2rem}}
.stat{{flex:1;background:#1a1a24;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;text-align:center}}
.stat-n{{font-size:2rem;color:#e8c97d;font-weight:bold}}
.stat-l{{color:#8a8a9a;font-size:0.8rem;text-transform:uppercase;margin-top:0.3rem}}
footer{{text-align:center;padding:2rem;color:#8a8a9a;font-size:0.8rem;border-top:1px solid #2a2a3a;margin-top:2rem}}
</style></head>
<body>
<nav><a class='logo' href='/'>EduFeedback</a><div><a href='/'>Submit</a><a href='/results'>Results</a><a href='/about'>About</a></div></nav>
{body}
<footer>Cloud Technologies Assignment &mdash; Render.com &mdash; Zebo Abdullayeva &mdash; Millat Umidi University</footer>
</body></html>"""

@app.route("/")
def index():
    return page("""<div class='wrap'>
<h1>Course Feedback Portal</h1>
<p>Share your experience. Your feedback helps improve education quality.</p>
<div class='card'>
<form action='/submit' method='POST
