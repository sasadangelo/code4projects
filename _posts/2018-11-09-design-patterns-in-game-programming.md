---
layout: post
title: Design Patterns in Game Programming
post_series_id: android-game-programming
slug: design-patterns-in-game-programming
thumbnail: assets/img/design-patterns.jpeg
excerpt: This is the sixth article of the Android Game Programming series. Here, I would like to show you how to use Design Patterns in your first video.
categories: 
  - Design Patterns
  - Game Programming
---

![Design Patterns in Game Programming](assets/img/design-patterns.jpeg){:width="200" height="252" .responsive_img}

# Design Patterns in Game Programming
_Posted on **{{ page.date | date_to_string }}**_

This is the sixth article of the [Android Game Programming](android-game-programming) series. In this article, I would like to show you how to use Design Patterns in your first video game.  

The Internet is full of Design Patterns articles and I do not want to repeat things already described elsewhere. Here I want to show you how to use Design Patterns on real projects like your first video game.

## What is a Design Pattern?

In Software Architecture, a Pattern is a known solution to a known problem. Writing code is often art and the code goodness is mostly delegated to the programmer skills. Over time, software engineers found out that there is some recurrence in the problems that arise every day in front of the software developer. In 1994 four software designers [wrote a book](https://www.amazon.it/dp/B000SEIBB8/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1) with a catalog of 23 of the most common solutions to the most recurring problems in the software industry. From that moment new patterns spread and consolidated in various areas of computer science.

## Singleton Pattern

The Singleton is one of the simplest and most well-known pattern. The goal of this patterns is to guarantee, for a given class, that there is only one object instance for it. This applies to classes that need to be accessed at different points in the code to avoid having to pass them as parameters to an infinite number of methods.

This [page contains a good introduction](https://www.journaldev.com/1377/java-singleton-design-pattern-best-practices-examples#lazy-initialization) to the pattern that I suggest you read. In my career, I used these patterns a lot of time. I usually used the [lazy singleton version](https://github.com/sasadangelo/designpatterns/blob/master/singleton/src/main/java/org/code4projects/designpatterns/LazySingleton.java) that is considered the default implementation, only when multiple threads access to it I used the [thread safe version](https://github.com/sasadangelo/designpatterns/blob/master/singleton/src/main/java/org/code4projects/designpatterns/ThreadSingleton.java).

In your first video game, Droids a Tetris clone, you will use this pattern for the class [DroidWorld](https://github.com/sasadangelo/Droids/blob/master/app/src/main/java/org/androidforfun/droids/model/DroidsWorld.java) that is the entry point for our video game model (see Model Control View pattern below).

## State Pattern

This is a pattern I use when the behavior of an object must change based on its state. It applies when an application or part of it behaves like a finite-state machine. In our case, for example, our video game when it is running can be paused, resumed or terminated. While the game is paused, you can resume it or exit.

![Droids States](assets/img/Droids-State.png){:width="450" height="417" .responsive_img}

Usually, in the normal procedural programming, to manage states you have to use conditional statements that examine the state of the objects in order to take some decisions. Very often these decisions are very complex and depend on many values, all this leads to the generation of large IFELSE / SWITCH blocks. This involves serious problems of understanding, maintenance, and evolution of the code.

The use of this pattern allows you to separate the large conditional blocks in state objects, and associate the behavior of an object to their state. I suggest you give a read to the [following Wikipedia page](https://en.wikipedia.org/wiki/State_pattern) that well describes how this pattern works.

In our specific case, we will have the need to update and design the game at each game loop based on game status. To do this we define the abstract class GameState (State) with only two abstract methods: **draw** and **update**.

The relative concrete classes (ConcreteState): [GamePaused](https://github.com/sasadangelo/designpatterns/blob/master/state/src/main/java/org/code4projects/designpatterns/GamePaused.java), [GameReady](https://github.com/sasadangelo/designpatterns/blob/master/state/src/main/java/org/code4projects/designpatterns/GameReady.java), [GameRunning](https://github.com/sasadangelo/designpatterns/blob/master/state/src/main/java/org/code4projects/designpatterns/GameRunning.java), and [GameOver](https://github.com/sasadangelo/designpatterns/blob/master/state/src/main/java/org/code4projects/designpatterns/GameOver.java); will implement the two methods based on the status they represent. The game status is managed by the [World](https://github.com/sasadangelo/designpatterns/blob/master/state/src/main/java/org/code4projects/designpatterns/World.java) class that is the class representing the game model (see Model Control View pattern below). Finally, there is the [client code](https://github.com/sasadangelo/designpatterns/blob/master/state/src/main/java/org/code4projects/designpatterns/GameScreen.java) that is responsible to update and draw the screen according to the World status.

## Factory Method Pattern

This pattern creates objects without specifying the exact class of the object to instantiate. It is based on a Creator class with a **Factory Method** that, based on the information received, will know which object to return. This pattern allows you to separate the framework from the client code allowing you to modify the implementation details without having to modify the client.

[Here you can find a good introduction to this pattern](https://en.wikipedia.org/wiki/Factory_method_pattern) that I suggest reading.

In our game, we will use this pattern to create Music and Sound objects required to play music or all the sounds generated by the game (i.e. projectile sounds, explosions, and so on). Currently, our code will run only on Android but, in the future, it could run also on iOS (iPhone and iPad), Web, and so on.

For this reason, we have two generic interfaces called [Sound](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/Sound.java) and [Music](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/Music.java). The concrete class will be [AndroidSound](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/AndroidSound.java) and [AndroidMusic](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/AndroidMusic.java), they will implement them for Android systems. The creator is the [Audio](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/Audio.java) interface with its concrete class [AudioAndroid](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/AndroidAudio.java).

When the application on the Android system startup the manifest file will reference the [AndroidGame](https://github.com/sasadangelo/designpatterns/blob/master/factorymethod/src/main/java/org/code4projects/designpatterns/AndroidGame.java) that instantiates the audio subsystem for Android and assign it to Gdx.audio variable. In this way, whenever a client code needs to create audio and music objects it can call the methods _Gdx.audio.newSound(filename)_ and _Gdx.audio.newMusic(filename)_.

## Model Control View Pattern

This is an architectural pattern firstly created for web applications. The idea behind this pattern is to separate the classes that represent the data (Model) from those that represent the user interface (View) and the one that controls the behavior of the application(Controller).

To do this in the code you will [find two packages](https://github.com/sasadangelo/Droids/tree/master/app/src/main/java/org/androidforfun): _org.androidforfun.droids.view_ and _org.androidforfun.droids.model_. The first contains both the View part and the Controller part (it would make sense to separate these two parts in two different packages in the future), while the second contains the model part. The idea is that a video game can be, in this way, easily implemented on another platform, such as a java swing, by simply changing the View and Controller part and leaving the Model unchanged.

## Game Loop

In the fifth article of this series, we already talked about **Game Loop**. Robert Nystrom, a programmer with a long experience in the video games area, wrote a very interesting book titled [Game Programming Patterns](http://gameprogrammingpatterns.com/). The book is available both for purchase on Amazon but also for free at this [link](http://gameprogrammingpatterns.com/contents.html). In the book, the author lists a series of recurrent patterns in video game programming and provides solutions on how to deal with them. Among these, there is the Game Loop.

## Object Pool

Video game memory allocation is a fundamental topic because it has an impact on performance and it determines how fast it is perceived by the user. Hardware such as mobile phones and tablets have limited resources compared to a PC and in some cases, it has to be assessed if the management that the programming language provides is adequate to our goals.

For example, if we are in the following conditions:

-   you must allocate and destroy hundreds of thousands of objects during the game;
-   objects have the same nature;
-   in a given time frame only a limited number of these objects is necessary.

Then it may be worthwhile organizing a fixed number of these objects, which we will call Object Pool, and instead of continuously creating and destroying them we simply use them and put them back into the pool as needed.

An approach like this not only increases performance because you do not create objects every time, but you also avoid fragmentation of the heap and the continuous execution of the garbage collector that could lead to delays.

Managing an Object Pool obviously complicates the source code and, therefore, its maintainability, so it should be used if and only if the 3 conditions seen above are true.

For example, in the Tetris game every time a tetramine falls, we assume that the user touches the screen, on average, 20 times in order to position and drop it. Suppose that every tetramine requires, on average, 3 seconds to fall, in a 1-hour game we will have the fall of 1200 tetramines, then 24000 touch events per hour. With a rapid calculation that takes into account the frame rate, an event pool of 100 elements is more than enough to handle 24,000 events per hour.

Instead of creating objects when needed and destroying them when they are not needed, at the beginning of the game the Object Pool is initialized, which will allocate N objects of the same type in memory. In this way, the objects will occupy a contiguous area eliminating the fragmentation problem. Moreover, having created it at the beginning, every time we need an object we will not waste time creating it, but we will simply take the pointer to a free one in the pool. When it is no longer needed, we will put it back in the pool so that it can be reused.

There are cases in which the request for objects cannot be satisfied by the pool because it is now exhausted. This problem can be solved in various ways. The first and also the simplest is to size the pool in such a way that this condition never occurs. When this cannot be guaranteed it is necessary to provide a dynamic object pool that allocates the object anyway and then places it in the pool when it is no longer needed.

At the [following link](https://github.com/sasadangelo/designpatterns/blob/master/objectpool/src/main/java/org/code4projects/designpatterns/Pool.java), you can find an example of the Object Pool class that we are going to use in our video game. As you can notice the pool is not preallocated because on average we only manage about 7 events every second (24000/3600=6.66). However, if you want to preallocate the events it is sufficient to remove the comment from the code in the constructor.

If you want to use the Object Pool for TouchEvent objects a code like this is required.

    {% highlight java %}
PoolObjectFactory<TouchEvent> factory = new PoolObjectFactory<TouchEvent>() {
    public TouchEvent createObject() {
        return new TouchEvent();
    }
};
touchEventPool = new Pool<TouchEvent>(factory, 100);
    {% endhighlight %}

## Observer Pattern

The Observer pattern is a behavioral pattern that is used when the change of state of a single object (Subject) must be notified to other objects (Observers) who have shown interest in it.

The typical example I use to explain how this pattern works is through an Excel spreadsheet. Suppose we have the cell A1 that contains the number 2 and A2 and A3 cells that contain, respectively, the double and the triple (A2 = A1 \* 2, A3 = A1 \* 3). Now if A1 = 3, then A2 = 6 and A3 = 9. If A1 (Subject) changes from 3 to 4, A2 and A3 (Observers) will be notified about the change and update their values accordingly (A2 = 8 and A3 = 12).

![Observer Spreadsheet](assets/img/Observer-Spreadsheet.png){:width="450" height="334" .responsive_img}

With this mechanism, the A2 and A3 cells will change only when A1 change, without any time-consuming polling.

This pattern is used in many libraries, GUI toolkit, and the MVC architectural pattern.

You can learn more about this pattern by reading the [following article](https://en.wikipedia.org/wiki/Observer_pattern).

In our video game, we are going to use the Observer Pattern to manage the collision detection dilemma that we will analyze in future articles.

## Risks of Patterns

Although the GoF book dates back to 1994, I began to study it a few years later when I started my professional work. Needless to say, this subject fascinated me a lot because I finally had mechanisms that allowed me to write elegant, maintainable, and efficient code.

Unfortunately, this discipline also had negative effects, because I tried to apply them whenever I could, penalizing the simplicity of the code. Sometimes I managed to create dozens of classes for problems that required only one. It took a long time to admit that the use of the patterns is not always suitable.

Today I have a more detached attitude towards them and when I want to apply one I always ask myself: is it worth it? Do I have any advantages? Based on the answers, I adjust my code accordingly.