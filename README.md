<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{% block title %}EduFeedback{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <nav>
    <a href="/" class="nav-logo">EduFeedback</a>
    <div class="nav-links">
      <a href="/">Submit</a>
      <a href="/results">Results</a>
      <a href="/about">About</a>
    </div>
  </nav>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>
    <p>Cloud Technologies Assignment &mdash; Deployed on Render.com</p>
  </footer>
</body>
</html>
