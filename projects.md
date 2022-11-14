---
layout: page
title: Projects
---
# Projects

On this page, I will collect all the projects that I have made using my technological and programming skills. The goal is to be able to pass on to others the knowledge acquired and my passion for programming and technology. To do this, I believe there is nothing better than showing how to implement a project step by step.

## Featured Projects

The following are the projects in hightlight. I consider them the most important projects I worked on and that could be useful for you.

<div class="featured-projects-area">
{% for item in site.data.featured-projects %}
  <div class="featured-projects-box">
    <div class="featured-projects-image">
      <a title="{{ item.title}}" href="{{ item.link}}"><img src="{{ item.image}}" alt="{{ item.title}}" width="200" height="auto"/></a>
    </div>
      <div class="featured-projects-title">
        <h3><a title="{{ item.title}}" href="{{ item.link}}">{{ item.title}}</a></h3>
      </div>
    <div class="featured-projects-text">{{ item.description}}</div>
  </div>
{% endfor %}
</div>

## Other Projects

There are other projects I worked on during the last 30 years but most of them are lost forever. In the past, a website like github.com didn’t exist. I kept all my projects on floppy disk or CD that with time I lost. However, I was able to find some of them that I saved on my Github page together with others that I developed recently.

**[Droids](https://github.com/sasadangelo/Droids)**: since the first years of my journey in programming I had always been fascinated by game programming. When I started to play with Android I had the chance to read a very good book called [Android Game Programming](https://www.amazon.it/Beginning-Android-Games-English-Zechner-ebook/dp/B00A4EH7D0/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=android+game+programming+mario&qid=1593502057&sr=8-1) wrote by Mario Zachner. The book explains basic game programming principles and how to use them with Android and Java. In the book he built, step by step, a game framework and some game examples. I used the framework code as a starting point for my project and in a very short time, I was able to build my first video game on Android: **Droids**, a Tetris clone.

**[Alien Invaders](https://github.com/sasadangelo/AlienInvaders)**: this project was my second attempt with Android Game Programming. In this project, I reused the game framework and on top of it, I built a clone of Space Invaders.

**[Mr Snake](https://github.com/sasadangelo/AlienInvaders)**: this is my third project in the Android Game Programming area. It is a Snake clone the famous game appeared in ’90 on Nokia phones.

**[Gollumix](https://github.com/sasadangelo/gollumix)**: when I was at the college and attended the Operating Systems course I wanted to develop a very small operating system by myself. Linux had already been available for a few years but the 2.2 version was too complex to understand at that time. For this reason, I started to study the earlier versions (from 0.01 to 0.96) and I created a project I called Gollumix. It was basically a boot loader that starts the kernel code with six consoles where whatever you type on the keyboard was written on the screen. For the project, I implemented a keyboard, floppy, and screen driver, process management, and a simple scheduler. The last time I tried this mini operating system was several years ago with a virtual machine called [Bochs](http://bochs.sourceforge.net/). I don’t know if it still works today.
