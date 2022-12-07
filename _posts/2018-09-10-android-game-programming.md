---
layout: post
title: Android Game Programming
post_series_id: android-game-programming
slug: android-game-programming
thumbnail: assets/img/Android-Game-Programming-mini.jpeg
excerpt: "This is the first article of the Android Game Programming series where I will show you how to write your first Android game: Droids a Tetris clone."
categories:
- Android
- Game Programming
---

![Android Game Programming](assets/img/Android-Game-Programming-mini.jpeg){:width="356" height="200" .responsive_img}

# Android Game Programming
_Posted on **{{ page.date | date_to_string }}**_

This is the first article of the **Android Game Programming** series. Here I will show you, step by step, how to write your first Android game: Droids a Tetris clone.

## Why an Android Game Programming series?

In the first decade of the 2000s, the smartphones and tablets boom widened the market of video games.

On one side smartphone owners had the opportunity to use their own mobile phone for recreation. On the other side, this gave a chance to many developers around the world to create their own video games, make them available on Google Play Store and have the opportunity to earn some money.

This article series was written to enable you to write, in a few days, your first Android video game and learn the rudiments of this platform by creating projects that are fun and non-trivial at the same time.

![Android Game Programming](assets/img/Android-Game-Programming.jpeg){:width="450" height="253" }

Writing a video game is not an easy task, it requires different skills such as: know how to program and understand the video games related problems. It is required the knowledge of a programming language and the platform on which the video game should work.

## Why Android over iOS platform?

The reason why I chose Android over iOS platform is that the costs to write an Android application are almost equal to zero. You just need your PC (whether it works with Linux, Mac or Windows), some free development tool and if you already know Java the time to acquire all the new concepts will be really minimal. With iOS, you need a Mac as a development platform and you need to learn a new programming language (Swift). Moreover, Android is much more widespread than the iOS since it runs on 80% of mobile devices.

This article series assumes that you already know the basics of Java programming language. If you don’t, I suggest you integrate the knowledge you will learn here with the reading of the [Java Programming Language](https://www.amazon.it/Java-Programming-Language-Ken-Arnold/dp/0321349806/ref=sr_1_1?ie=UTF8&qid=1536609609&sr=8-1&keywords=the+java+programming+language) book and some other online resource on the subject.

## Article series content

The [second article in this series](how-to-install-android-studio) will be dedicated to the necessary steps to install and configure the development environment. In the [third article](how-to-create-an-android-application), I’ll show you how to create your first Android application.

The [fifth article](video-game-programming-principles) will introduce the basic concepts of video game programming. In the [sixth article](design-patterns-in-game-programming), we will see the Design Patterns used in our video game.

In the seventh article, I will introduce Android basic concepts and, step by step, through a series of exercises, we will build a framework for our video game. The code we will write at this stage will not only be used to write your first video game but it can be used, as it is, to write others video games.

In the tenth article, I will present the video game that we will implement in this series: Droids, a Tetris clone. I chose a video game so famous because I do not want you to spend a lot of time learning the rules of a new game. Tetris is so famous that there is no need for presentations.

![Droids Screen](assets/img/Droids-Main-Screen.png){:width="200" height="355" } ![Droids Game Screen](assets/img/Droids-Game-Screen.png){:width="200" height="355" .responsive_img}

## Source code structure

We will see how the code works in every detail. You’ll learn that it can be divided into two parts:

1.  Framework
2.  Droids

The former is a set of code that you can reuse for other video games. The idea is to have a piece of code that will always be the same for all the video games and a part that is specific to the video game you are implementing. In this way, the time to implement a new video game will be minimum.

Most of the framework code comes from the book [Beginning Android 4 Games Development](https://www.amazon.com/Beginning-Android-4-Games-Development/dp/1430239875) by Mario Zechner and released under GPL3 license. He is the author of Libgdx one of the most used libraries for developing video games for Android. Getting familiar with this code allow us to create the fundamentals to create our video game. In the future, if you want to use Libgdx the changes to be made will be minimal.

The choice not to use Libgdx for implementing the Droid game is that I want you to learn what happens behind the scenes when the framework manages the graphics, the input system, the files, and audio. If you learn how they work you’ll be able to write whatever game you want.

You will find the source code for this article series on my [GitHub account](https://github.com/sasadangelo). The [HelloWorldApp](https://github.com/sasadangelo/HelloWorldApp) repository will contain the source code of our first Android application and all the exercises presented in the 8th and 9th article. The [Droids](https://github.com/sasadangelo/Droids) repository will contain the code of the first video game you will implement: Droids.

The source code is released under the GPL 3 license.

## What’s Next?

In the next articles, we will start the creation of our video game [setting up the development environment](how-to-install-android-studio) and [create our first Android application](how-to-create-an-android-application).