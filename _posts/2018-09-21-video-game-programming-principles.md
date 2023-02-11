---
layout: post
title: Video game programming principles
post_series_id: android-game-programming
slug: video-game-programming-principles
image: /wp-content/uploads/2018/09/Background-Sprite-Walking-mini.jpg
excerpt: In this article I want to explain basic video game programming principles in order to help you to write your first Android video game.
categories:
- Programming
---

![Video game programming principles]({{ site.baseurl }}/wp-content/uploads/2018/09/Background-Sprite-Walking-mini.jpg){:width="320" height="200" .responsive_img}

# Video game programming principles
_Posted on **{{ page.date | date_to_string }}**_

This is the fifth article of the [Android Game Programming]({{ site.baseurl }}/android-game-programming/) series. Here I would like to explain basic video game programming principles in order to help you to write your first Android video game.

## A Brief Introduction

A video game is different from common PCs, mobile phones, or tablets applications. In order to implement one, it is necessary to have some basic knowledge that we are going to explain in this article.

A video game is basically a loop that polls on the user input, updates the game status, and draw it on video. Draw a video game means to draw the user interface (UI/HUD), draw its status (men, walls, enemies, etc.), special effects, and animations.

Typically, the video game interface is not based on the normal platform framework. For example, on Android to draw buttons we use Button, RadioButtons, and other similar Java classes. All of them inherit from the View class and are grouped by ViewGroup objects like the layouts. These mechanisms are not usable for a video game, both for performance and interface complexity reasons.

Furthermore, a video game also requires handling physics and artificial intelligence as well as various input devices.

![Game]({{ site.baseurl }}/wp-content/uploads/2018/09/Game.png){:width="300" height="296" .responsive_img}

In this article, we will talk about **Game Loop**, **Frame Rate**, **Color Vision**, **Frame buffer**, **Sprite**, **Alpha Blending**, and **Collision detection**.

## Game Loop

Any video game always contains one **Game Loop** and the fact that you see it or not depends on whether you’re using a **game engine** or you are writing the full game by yourself. In the former case, the game loop is usually hidden. In the other case, however, you have to implement it. Since we will not use any game engines, we will create our own Game Loop.

The Game Loop is a piece of code that, generally, represents 1% of the entire game, but it is executed 90% of the time, so it must be written carefully because it must be extremely efficient.

The code of a Game Loop looks like this:

    {% highlight java %}
while (true) {
    processInput();
    update();
    draw();
}
    {% endhighlight %}

The problem with this code, however, is that on a very fast device it will produce a very fast game impossible to play.

## Frame Rate

During a game loop, a video game must keep track of the passage of time to make sure that a fixed number of iterations takes place every second. This number of iterations per second is called the **frame rate**.

Correct management of the Frame Rate allows the video game to run at the same speed regardless of the underlying hardware.

**How much must be the value of the Frame Rate?**

A large Frame Rate value allows a greater game fluidity and a lower latency of user input, obviously, it can not be increased indefinitely due to the overhead. There are games that run at 60 FPS. The time between one update and another (16 ms) is called the time step (TS). There are games of 25, 30, 50, or 60 FPS and sometimes it happens that the same game has an FPS that varies according to the platform. The idea is to have a single parameter to regulate fluidity and latency of the game.

Here is an example of code to manage the frame rate:

    {% highlight java %}
MS_PER_FRAME =1000/FPS // 1s=1000ms

while (true) {
    double start = getCurrentTime();
    processInput();
    update();
    draw();
    sleep(start + MS_PER_FRAME - getCurrentTime());
}
    {% endhighlight %}

The sleep command ensures that the game does not advance too quickly in case the hardware performs the three methods quickly. Unfortunately, though, if the 3 methods require more than 16 ms for their execution (I’m assuming an FPS = 60) then the game will slow down and the only one way to solve this problem is to make the 3 methods do less work.

The problem we have is basically summarized in two steps:

1. at every step the game progresses for a certain amount of time;
2. a certain amount of time is required to advance the game.

If step 2 is faster than step 1 the game will slow down. It is therefore clear that if the game has to advance 16 ms at each iteration but, systematically, its processing takes more time than 16 ms the game is not in synchrony. The only way to remedy this problem is to update it less frequently.

The idea could, therefore, be to choose a time step that is equal to the time elapsed to perform the last iteration. The bigger the time step the more the progress of the game will be great. Thus we will have a variable frame rate which, however, preserves the fluidity of the game. The code will be something like this:

    {% highlight java %}
double lastTime = getCurrentTime();
while (true) {
    double current = getCurrentTime();
    double elapsed = current - lastTime;
    processInput();
    update(elapsed);
    render();
    lastTime = current;
}
    {% endhighlight %}

As you can see from the code, the elapsed variable contains the elapsed time to process the previous iteration and it is passed to the update method to update the game for that exact time.

For example, suppose you have a game in which a little man shoots at enemies. If the game works with a constant frame rate (hence a fixed time step) then the projectile will advance to each frame by an equal amount proportional to its speed. In the case of a variable time step, the larger the value, the more it will progress over a single frame. So the projectile will travel consistently both if it executes 24 small time steps to cross the screen and 4 large time steps. With this mechanism it will be:

- consistent on the various types of hardware;
- more fluid on fast machines because the time steps will be smaller;

It is clear that since the frame rate and time step are not deterministic the debugging of any problems will be more difficult.

## Color Vision

A monitor projects a point on the screen called **pixel** whose color is given by the combination of three lights: red (R), green (G) and blue (B). As we have seen so far the combination of these three lights reach the human eye and its three photoreceptors (S, M, and L) break it down creating the sensation of that specific color in the brain.

![Fotoreceptors]({{ site.baseurl }}/wp-content/uploads/2018/09/Fotoreceptors.png){:width="450" height="259" .responsive_img}

Typically modern computers use one byte (8 bits) for each RGB component for a total of 6 million (2^24=16 million) different colors. Sometimes, a single pixel is added to a fourth byte called Alpha, which we’ll discuss later.

These pixels are organized into an NxM matrix called video resolution.

The greater these values are the better will be the “image definition”. To better understand what “image definition” term means see the following photo. The first image has a 10×10 resolution, the second one has an 18×18 resolution and the third one has a 30×30 resolution. As you can notice as you go on the right the image looks better.

![Image resolution]({{ site.baseurl }}/wp-content/uploads/2018/09/Image-resolution.png){:width="300" height="77" .responsive_img}

Considering that 4 bytes are needed to represent a pixel, in an HD video image (1920×1080) 8 Mb are required.

## Frame buffer

Many computers reserve a portion of memory for displaying video images. However, processing an image and drawing it directly on the screen involves some problems:

- flickering;
- the image will not be drawn instantly but line by line;
- little immediacy in the visualization.

To eliminate this problem, many computers reserve a memory area 2, 4, or 8 times larger than the one needed to view the video image. Each of these areas is said **memory page** and, in a given instant, only one of it will be visible. This area will have a special pointer that will tell the computer which pages to display on the screen.

![Video Memory]({{ site.baseurl }}/wp-content/uploads/2018/09/Video-Memory.png){:width="450" height="334" .responsive_img}

Usually, a video screen is drawn on a not visible memory page (called frame buffer) and as soon as it will be complete a “page swap” occurs that typically is instantaneous. The result is a fluid visualization without flickering where the animation will be perfect. In our game, we will adopt a similar procedure. We will draw the screen first in a not visible area and then we will activate it.

## Sprite

A video game in addition to drawing the background bitmap often requires to draw some smaller bitmaps called **sprite** representing the characters of the video game. Typically to a character is associated with one or more sprites. For example, if the character has to walk you have to create a number of sprites that, displayed in sequence, create the illusion of a walk.

![Sprite Walking]({{ site.baseurl }}/wp-content/uploads/2018/09/Sprites-Walking.png){:width="300" height="117" .responsive_img}

The animation is a sequence of N sprites drawn at a certain speed that creates the illusion of movement. Typically a sprite is a rectangle with its own background, let’s say white. If we overlap the sprite against the background of the game we will get an unpleasant result, because the white of its background overlays the background of the game creating an unpleasant result.

![No Alpha Blending]({{ site.baseurl }}/wp-content/uploads/2018/09/Background-Sprite-Bad.png){:width="450" height="281" .responsive_img}

How do you make sure that the white part becomes transparent and you see the background below? The answer is using **Alpha Blending**.

## Alpha Blending

In computer graphics, **Alpha Blending** is the process of combining an image with the background to create the appearance of partial or full transparency. The concept of Alpha Blending was introduced in 1970 by Alvy Smith and then developed by Thomas Porter and Tom Duff. A 2D image we have seen that it is basically a matrix in which each pixel requires 3 bytes to describe the color. One byte for each RGB component. Besides these 3 bytes, there can be a fourth one indicating, via a value that varies from 0 to 1 (or 0 to 255), the opacity of the sprite background. 0 indicates absolute opacity, while 1 transparency.

![Alpha Blending]({{ site.baseurl }}/wp-content/uploads/2018/09/Background-Sprite-Walking.jpg){:width="450" height="281" .responsive_img}

## Collision Detection

Anyone who is about to write a video game, sooner or later, will have to deal with the problem of **collision detection**. This problem occurs, for example, when a little man is in front of an obstacle and can no longer proceed. In the Tetris game, for example, the problem of collisions occurs when a tetramine can not rotate because it hits a block already deposited on the bottom.

There are several collision detection techniques that vary by their simplicity of implementation and accuracy. Typically, the simple solutions are also the fastest but less precise, while the more complex ones are more precise but also those that, from a computational point of view, cost more. Typically the choice always falls on simple solutions when the visual result is appreciable otherwise it will be necessary to resort to more complicated but more precise techniques.

### The Rectangle method

This is the simplest and easiest to implement the technique and its computational cost is really minimal. It is a technique that works well enough on very small objects, which are symmetrical and have an almost rectangular shape.

The idea is to delimit the object inside a rectangle. Two objects will collide when the relative rectangles containing them intersect.

![Collisions Detection]({{ site.baseurl }}/wp-content/uploads/2018/09/Collision-Detection.png){:width="300" height="141" .responsive_img}

To easily determine if two rectangles intersect verify that the rectangle R1 does not contain one of the vertices of R2.

    {% highlight java %}
R1.contains(R2.x, R2.y) || R1.contains(R2.x+R2.width-1, R2.y) ||
R1.contains(R2.x, R2.y+R2.height-1) ||
R1.contains(R2.x+R2.width-1, R2.y+R2.height-1)
    {% endhighlight %}

With this approach, we have converted the problem of verification if two rectangles intersect in the problem if a rectangle contains a point, which is much simpler.

A rectangle R1 contains a point x, y if and only if:

    {% highlight java %}
x>=R1.x && x < R1.x + R1.width && y >= R1.y && y < R1.y + this.height;
    {% endhighlight %}

This technique is the one we will use for all the video games shown in this blog. There are other techniques for collision detection such as the **Circle Technique** in which the object rather than being delimited by a rectangle is delimited by a circle having a given center and radius. With this technique, two objects collide when their circles intersect. It is a more suitable technique for objects very close to the circular shape and which performs many rotations.

There are techniques for collision detection, but since the philosophy of this article series is to explain only the essential concepts to implement your first video game, we will not delve further into them.
