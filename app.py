{% extends "base.html" %}
{% block title %}Results – EduFeedback{% endblock %}

{% block content %}
<section class="hero">
  <div class="hero-text">
    <span class="tag">Live Data</span>
    <h1>Feedback<br>Results</h1>
    <p>All submitted feedback is stored and displayed here in real time.</p>
  </div>
</section>

<section class="stats-row">
  <div class="stat-card">
    <div class="stat-number">{{ total }}</div>
    <div class="stat-label">Total Responses</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">{{ avg_rating }} ★</div>
    <div class="stat-label">Average Rating</div>
  </div>
</section>

<section class="results-section">
  {% if entries %}
    {% for entry in entries %}
    <div class="result-card">
      <div class="result-header">
        <div>
          <strong>{{ entry.name }}</strong>
          <span class="course-tag">{{ entry.course }}</span>
        </div>
        <div class="rating-badge">{{ entry.rating }}★</div>
      </div>
      {% if entry.comment %}
      <p class="comment">"{{ entry.comment }}"</p>
      {% endif %}
      <p class="timestamp">{{ entry.timestamp }}</p>
    </div>
    {% endfor %}
  {% else %}
  <div class="empty-state">
    <p>No feedback submitted yet. <a href="/">Be the first!</a></p>
  </div>
  {% endif %}
</section>
{% endblock %}
