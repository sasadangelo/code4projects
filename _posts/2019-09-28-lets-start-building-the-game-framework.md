---
layout: post
title: Let’s start building the Game Framework
post_series_id: android-game-programming
slug: lets-start-building-the-game-framework
thumbnail: assets/img/game-framework.jpeg
excerpt: In this article, we will start to create our Game Framework. It will be used to write all our videogames.
categories: Android
---

![Let’s start building the Game Framework](assets/img/game-framework.jpeg){:width="312" height="200" }

# Let’s start building the Game Framework
_Posted on **{{ page.date | date_to_string }}**_

This is the eleventh article of the [Android Game Programming](android-game-programming) series. Starting from this article we will begin to add very significant classes to our Game Framework.

## Graphics interface

First, we will add the _Graphics_ interface that will manage the graphics services such as drawing bitmaps, points, lines, rectangles, and more. The bitmaps are managed by the _Pixmap_ interface created from a file using the _newPixmap_ API. This API also requires you to specify the bitmap format (_PixmapFormat_):: _ARGB8888_, _ARGB4444_, _RGB565_.

{% highlight java %}
    public interface Graphics {
        enum PixmapFormat {
            ARGB8888, ARGB4444, RGB565
        }
        Pixmap newPixmap(String fileName, PixmapFormat format);
        void drawPixmap(Pixmap pixmap, int x, int y, int srcX, int srcY, int srcWidth, int srcHeight);
        void drawPixmap(Pixmap pixmap, int x, int y);
    }
{% endhighlight %}

The _newPixmap_ and _drawPixmap_ methods will take care of loading the bitmap into memory and draw it on video. The first method, we will encapsulate the code of loading the bitmap [discussed here](android-resources-management), in the second one we will support the _drawBitmap_ method of class Android _Canvas_.

## The Screen interface

In the graphics management, a basic role is played by the _Screen_ interface which represents the single screen of the video game.

{% highlight java %}
    interface Screen {
        void update();
        void draw();
        void pause();
        void resume();
        void dispose();
    }
{% endhighlight %}

Creating a video game is a bit like making a movie. First, there is the storyline, that is the basic idea of what the video game will do. Afterward, it is necessary to write the script. In our case, it is a sheet where we draw the video game screenshots and events to switch from one to another.

## The Loading and Start screen

The following image shows, for example, the screens that we will implement in this article.

![Start and Loading Screen](assets/img/StartAndLoadingScreen.png){:width="450" height="327" }

As you can see the first screen is Loading Screen which is a dummy screen in which we only worry about loading all the video game assets into memory. In this case, there is just the bitmap **startscreen.png**. In the future, this screen could be made visible showing a progress bar that will report the loading progress. As this processing is very fast today we will avoid complicating unnecessarily our interface. Once all the assets have been loaded, the control will switch to the Start Screen on which we will show the bitmap already discussed [here](android-graphics-programming-for-games).

We define the package _org.androidforfun.droids.view_ where we will put the two screens mentioned above. In the package, we add the _Assets_ class which will contain the pointers to all the assets of our video game:

{% highlight java %}
    public class Assets {
        public static Pixmap startscreen;
    }
{% endhighlight %}

We will then define the _LoadingScreen_ class in which we will implement the update method:

{% highlight java %}
    public class LoadingScreen implements Screen {
        ...
        public void update() {
            Assets.startscreen = Gdx.graphics.newPixmap("startscreen.png", PixmapFormat.RGB565);
            Settings.load(Gdx.fileIO);
            Gdx.game.setScreen(new StartScreen());
        }
        ...
    }
{% endhighlight %}

The method loads the assets and the scores saved on external memory, then it passes the control to _StartScreen_ class. The _StartScreen_ class we will implement only the draw method in which we will draw the bitmap on screen:

{% highlight java %}
    public class StartScreen implements Screen {
        public void draw() {
            Gdx.graphics.drawPixmap(Assets.startscreen, 0, 0);
        }
    }
{% endhighlight %}

To execute the code you can perform the procedure [discussed here](how-to-create-an-android-application). The source code of this article can be found [here](https://github.com/sasadangelo/HelloWorldApp/archive/0.0.6.zip).