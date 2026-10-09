---
layout: page
title: Projects & Tutorials
slug: projects-2
excerpt: All the projects and tutorial series on Code4Projects — real code, step-by-step articles, and free ebooks.
---
# Projects & Tutorials

Every topic on this blog is built around a **series** of progressive articles — from fundamentals to a working system. Projects have real source code on GitHub. Tutorials are complete series you can follow end to end.

## Featured Projects & Tutorials

<div class="featured-projects-area">
{% for item in site.data.featured-projects %}
  <div class="featured-projects-box">
    <div class="featured-projects-image">
      <a title="{{ item.title }}" href="{{ item.series_link }}">
        <img src="{{ item.image }}" alt="{{ item.title }}" width="200" height="auto"/>
      </a>
    </div>
    <div class="featured-projects-title">
      <h3><a title="{{ item.title }}" href="{{ item.series_link }}">{{ item.title }}</a></h3>
    </div>
    <div class="featured-projects-text">
      {{ item.description }}
      <br/>
      <a href="{{ item.series_link }}">Read the series →</a>
      {% if item.github %}
      &nbsp;·&nbsp;
      <a href="{{ item.github }}" target="_blank" rel="noopener">View on GitHub →</a>
      {% endif %}
    </div>
  </div>
{% endfor %}
</div>

---

## Other Projects

Projects I worked on over the years — some older, but still worth exploring.

**[Droids](https://github.com/sasadangelo/Droids)** — A Tetris clone for Android built in Java, using a custom game framework inspired by the book *Beginning Android Games* by Mario Zechner. The full game framework is documented in the [Android Game Programming]({{ site.baseurl }}/android-game-programming/) series.

**[Alien Invaders](https://github.com/sasadangelo/AlienInvaders)** — A Space Invaders clone for Android, built on top of the same game framework.

**[Mr Snake](https://github.com/sasadangelo/AlienInvaders)** — A Snake clone for Android. Classic Nokia-era gameplay, modern Android implementation.

---

## All Source Code

All project source code is available on [GitHub](https://github.com/sasadangelo).
