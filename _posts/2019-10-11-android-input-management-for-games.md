---
layout: post
title: Android Input Management for Games
post_series_id: android-game-programming
slug: android-input-management-for-games
thumbnail: wp-content/uploads/2019/10/Android-Input-Management2.jpg
excerpt: This is the twelfth article of the Android Game Programming series. Here, I would like to discuss how to manage user input on Android for our games.
categories:
- Android
- Game Programming
---

![Android Input Management for Games]({{ site.baseurl }}/wp-content/uploads/2019/10/Android-Input-Management2.jpg){:width="200" height="200" .responsive_img}

# Android Input Management for Games
_Posted on **{{ page.date | date_to_string }}**_

This is the twelfth article of the [Android Game Programming]({{ site.baseurl }}/android-game-programming/) series. In this article, I would like to discuss how to manage user input on Android for our video game.

In an Android application, graphic elements such as buttons, text fields, radio buttons, etc., composes the user interface. In Android, all these objects derive from the _View_ interface and grouped together using *ViewGroup* objects such as a *Layout*. With such interfaces, input management is simple because if we click a button, Android itself that takes the care of it running the relative action code.

For example, the *Button* class extends the *View* class which allows you to set up a listener to respond to click commands. If you want to execute some code when you click a button, you need to write a code like this:

    {% highlight java %}
Button button = (Button) findViewById(R.id.button_id);     
button.setOnClickListener(new View.OnClickListener() {
    public void onClick(View v) {
        // put here the code to run        
    }     
})
    {% endhighlight %}

Unfortunately, writing a video game is very different from writing a normal Android application. Having to draw game objects by ourselves we cannot leverage the Android APIs to manage buttons.

We have to do everything ourselves and rely on a few classes (such as *View* and *ViewGroup*) and from these build our infrastructure. In an application the input can occur in several ways:

- keyboard;
- video touch;
- accelerometer;
- gyroscope;

## Input Management for Games

### Single-Touch Events

This article series presents only the necessary concepts for the implementation of our video game, so we won’t talk about keyboard input, accelerometer or gyroscope, but only events resulting from the video touch.

However, we will create such a flexible interface that adding other input modes will be a piece of cake. In this article, we will add to our Start Screen a button to turn the sound on and off (even if at the moment there is no audio management yet). The button will have a speaker icon that indicates its use.

Clicking on the button, the icon will change making a speaker appear in mute mode. As we have seen we cannot use the Android _Button_ class but we’ll have to draw the button ourselves, capture the touch event, understand that the button has been clicked and execute the corresponding action.

![Button Disable Audio]({{ site.baseurl }}/wp-content/uploads/2019/10/Disattiva-audio.png){:width="450" height="316" .responsive_img}

Luckily the _View_ interface (hence also our *AndroidFastRenderView* class) allows you to register touch events with the _setOnTouchListener_ method and create listeners that implement the _OnTouchListener_ interface just to intercept these events. This interface has only one method to implement:

    {% highlight java %}
abstract boolean onTouch(View v, MotionEvent event);
    {% endhighlight %}

The idea is to collect all the events that arrive in a buffer and when the user requests them, we supply them in output. To do this we need to extend the interface *OnTouchListener* so in the package *org.androidforfun.framework.impl* we add the *TouchHandler* interface defined as follows:

    {% highlight java %}
public interface TouchHandler extends OnTouchListener {
    ...
    List<TouchEvent> getTouchEvents();
}
    {% endhighlight %}

*TouchEvent* static class will represent touch-type events in our framework, it will have the following public fields:

    {% highlight java %}
class TouchEvent {
    public static final int TOUCH_DOWN = 0;
    public static final int TOUCH_UP = 1;
    public static final int TOUCH_DRAGGED = 2;
    public int type;
    public int x, y;
    public int pointer;
    {% endhighlight %}

As you can see there is the need to know what kind of touch event is, for example, if there was a touch (TOUCH\_DOWN) or a release (TOUCH\_UP) or if the finger was dragged along the video (TOUCH\_DRAGGED), the x, y coordinates of the video you touch and a pointer we’ll see better later.

### Multi-Touch Events

With version 1.6 and earlier, Android was only able to detect individual touch events, with later versions you can also manage multi-touch events. **What is a multi-touch event?**

Have you ever wanted to zoom in on one web page and used two fingers spreading them outwards? This is an example of a multi-touch. To avoid having to handle exceptions on older versions of Android will be necessary to implement the *TouchHandler* interface in two ways depending on whether the Android version is higher or lower than version 1.6. We introduce two classes *SingleThouchHandler* and *MultiTouchHandler* which will implement the *TouchHandler* interface depending on the Android version:

    {% highlight java %}
if(Integer.parseInt(VERSION.SDK) 
    touchHandler = new SingleTouchHandler(view, scaleX, scaleY);
else
    touchHandler = new MultiTouchHandler(view, scaleX, scaleY);
    {% endhighlight %}

SDK 5 corresponds to Android 2.0 which is the version after 1.6. Because today is really difficult to find phones with Android below 2.0 we can safely say that in 99% of cases we will use the *MultiTouchHandler* class which is the one that we will analyze in this article, the other is similar. The implementation of the *MultiTouchHandler* class must take into account some very important technical requirements so that input management is done correctly and without degrading performance.

- In a video game the phone screen may be touched by dozens of thousands of times and to generate a new event each time would require an expenditure of memory with consequent activation of the garbage collector that would degrade the video game performance. To avoid this, the allocation of new events will take place using the Object Pool pattern sized up to 100 items. In the package *org.androidforfun.framework* we define the *Pool* class whose implementation has already been discussed [here]({{ site.baseurl }}/design-patterns-in-game-programming/).
- The X and Y scale factors of the current video must be taken into account. We said that our assumption is that the resolution of the video is always 320×480 and then we will adapt images and events at the actual resolution of the video using scale factors *scaleX* and *scaleY*.
- Collect events in a buffer to prevent them from being lost.

Touch events can be single or multi-touch. In the former case, what is needed to know is if the screen has been touched, released or scrolled. It is also necessary to know in which point of the video the touch occurred. Furthermore, in the case of multi-touch, you need this information for each finger. Let’s see what Android offers to manage user touch events.

Every time the user touches the screen, Android generates a *MotionEvent* event and associates it with the View currently in the foreground. The action field describes what kind of event it is, in our case, it will be an ACTION\_DOWN. Vice versa, when the action releases it, the action will be ACTION\_UP. In the case of dragging, the action will be ACTION\_MOVE. The event will also provide the x, y coordinates where the finger (or mouse, pen, etc.) touched the screen. In the case of single touches, the pointer will always be 0. In the case of multiple touches, a *MotionEvent* event will be created for each finger. A pointer field will provide information on which finger touched the screen. For each finger, we will have the following actions:

- ACTION\_POINTER\_DOWN every time the finger touches the screen;
- ACTION\_POINTER\_UP every time the finger releases the screen; when a gesture is aborted an ACTION\_CANCEL event will be generated which we will consider as an ACTION\_UP.

Now let’s see how to implement the MultiTouchHandler class.

    {% highlight java %}
public class MultiTouchHandler implements TouchHandler {
    boolean[] isTouched = new boolean[20];
    int[] touchX = new int[20];
    int[] touchY = new int[20];
    Pool<TouchEvent> touchEventPool;
    List<TouchEvent> touchEvents = new ArrayList<>();
    List<TouchEvent> touchEventsBuffer = new ArrayList<>();
    float scaleX;
    float scaleY;
    {% endhighlight %}

The class manages a maximum of 20 pointers (typically 2 or 3 are enough), a pool of 100 events (*touchEventPool*), a buffer (*touchEventsBuffer*) and *scaleX* and *scaleY* factors. The constructor is quite simple and requires no comment.

    {% highlight java %}
public MultiTouchHandler(View view, float scaleX, float scaleY) {
    PoolObjectFactory<TouchEvent> factory=new PoolObjectFactory<TouchEvent>() {
        public TouchEvent createObject() {
            return new TouchEvent();
        }
    };
    touchEventPool = new Pool<>(factory, 100);
    view.setOnTouchListener(this);
    this.scaleX = scaleX;
    this.scaleY = scaleY;
}
    {% endhighlight %}

The most important method of the class is *onTouch* which will convert Android events into events understandable by our framework. How easy it is to observe events ACTION\_DOWN and ACTION\_POINTER\_DOWN will be converted to TOUCH\_DOWN events. The x, y coordinates of the event and the pointer will be taken. The same thing for ACTION\_UP events, ACTION\_POINTER\_UP and ACTION\_CANCEL converted to TOUCH\_UP. Finally, the ACTION\_MOVE event converted to TOUCH\_DRAGGED. You can see that every event arriving is stored in the *touchEventsBuffer* buffer.

    {% highlight java %}
public boolean onTouch(View v, MotionEvent event) {
    synchronized (this) {
        int action = event.getAction() &amp; MotionEvent.ACTION_MASK;
        int pointerIndex = (event.getAction() &amp; 
            MotionEvent.ACTION_POINTER_ID_MASK) &gt;&gt;
            MotionEvent.ACTION_POINTER_ID_SHIFT;
        int pointerId = event.getPointerId(pointerIndex);
        TouchEvent touchEvent;

        switch (action) {
            case MotionEvent.ACTION_DOWN:
            case MotionEvent.ACTION_POINTER_DOWN:
                touchEvent = touchEventPool.newObject();
                touchEvent.type = TouchEvent.TOUCH_DOWN;
                touchEvent.pointer = pointerId;
                touchEvent.x = touchX[pointerId] = (int) (event
                    .getX(pointerIndex) * scaleX);
                touchEvent.y = touchY[pointerId] = (int) (event
                    .getY(pointerIndex) * scaleY);
                isTouched[pointerId] = true;
                touchEventsBuffer.add(touchEvent);
                break;
            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_POINTER_UP:
            case MotionEvent.ACTION_CANCEL:
                touchEvent = touchEventPool.newObject();
                touchEvent.type = TouchEvent.TOUCH_UP;
                touchEvent.pointer = pointerId;
                touchEvent.x = touchX[pointerId] = (int) (event
                    .getX(pointerIndex) * scaleX);
                touchEvent.y = touchY[pointerId] = (int) (event
                    .getY(pointerIndex) * scaleY);
                isTouched[pointerId] = false;
                touchEventsBuffer.add(touchEvent);
                break;
            case MotionEvent.ACTION_MOVE:
                int pointerCount = event.getPointerCount();
                for (int i = 0; i < pointerCount; i++) {
                    pointerIndex = i;
                    pointerId = event.getPointerId(pointerIndex);
                    touchEvent = touchEventPool.newObject();
                    touchEvent.type = TouchEvent.TOUCH_DRAGGED;
                    touchEvent.pointer = pointerId;
                    touchEvent.x = touchX[pointerId] = (int) (event
                        .getX(pointerIndex) * scaleX);
                    touchEvent.y = touchY[pointerId] = (int) (event
                        .getY(pointerIndex) * scaleY);
                    touchEventsBuffer.add(touchEvent);
                }
                break;
            }
        return true;
    }
}
    {% endhighlight %}

The video game, as we have seen, is a game loop that updates and draws itself N times per second, with N corresponding to the FRAME RATE. At each update, the code must get all user input and do it with a code like this:

    {% highlight java %}
List touchEvents = game.getInput().getTouchEvents();
int len = touchEvents.size();
for(int i = 0; i < len; i++) {
    Input.TouchEvent event = touchEvents.get(i);
    switch (event.type)
        case Input.TouchEvent.TOUCH_UP:
            ...
            break;
        case Input.TouchEvent.TOUCH_DOWN:
            ...
            break;
        case Input.TouchEvent.TOUCH_DRAGGED:
            ...
            break;
}
    {% endhighlight %}

The video game, as we have seen, is a game loop that updates and draws itself N times per second, with N corresponding to the FRAME RATE. At each update the code must get all user input and do it with a code like this:

    {% highlight java %}
public List getTouchEvents() {
    synchronized (this) {
        int len = touchEvents.size();
        for (int i = 0; i < len; i++)
            touchEventPool.free(touchEvents.get(i));
            touchEvents.clear();
            touchEvents.addAll(touchEventsBuffer);
            touchEventsBuffer.clear();
            return touchEvents;
         }
}
    {% endhighlight %}

### Buttons Management

Now that we've added the infrastructure to manage user input let's see how to add a button to our screen and how to change its appearance by clicking repeatedly. First, let’s copy the **buttons.png** image into the assets folder. You can take this image with the source code [here](https://github.com/sasadangelo/HelloWorldApp/archive/0.0.7.zip). In the *Assets* class we add a new bitmap:

![Buttons]({{ site.baseurl }}/wp-content/uploads/2019/10/buttons.png){:width="100" height="250" .responsive_img}

    {% highlight java %}
public class Assets {
    ...
    public static Pixmap buttons;
}
    {% endhighlight %}

and in the *LoadingScreen* class we provide to load it in memory:

    {% highlight java %}
public class LoadingScreen implements Screen {
    ...
    public void update() {
        Assets.startscreen = Gdx.graphics.newPixmap("startscreen.png", 
                                                    PixmapFormat.RGB565);
        Assets.buttons = Gdx.graphics.newPixmap("buttons.png", 
                                                PixmapFormat.RGB565);
        Settings.load(Gdx.fileIO);
        game.setScreen(new StartScreen());
}
    {% endhighlight %}

At this point, in the *StartScreen* class we define a *soundEnabled* attribute that indicates whether the sound is active or not. By default, it is activated. In the *update* method, we take the user inputs and check whether the button has been pressed or not, setting the relative *soundEnabled* attribute. In the draw method, we will draw the button with the loudspeaker or mute depending on the value of the *soundEnabled* attribute.

    {% highlight java %}
public class StartScreen implements Screen {
    private boolean soundEnabled;
    ...
    public void update() {
        List touchEvents = Gdx.input.getTouchEvents();
        int len = touchEvents.size();
        for(int i = 0; i < len; i++) {
            Input.TouchEvent event = touchEvents.get(i);
            if(event.type == Input.TouchEvent.TOUCH_UP) {
                if(inBounds(event, 32, 374, 51, 51)) {
                    soundEnabled = !soundEnabled;
                }
            }
        }
    }

    private boolean inBounds(Input.TouchEvent event, int x, int y, int width, int height) {
        if (event.x > x && event.x < x + width - 1 && event.y > y && event.y < y + height - 1)
            return true;
        else
            return false;
    }

    public void draw() {
        Gdx.graphics.drawPixmap(Assets.startscreen, 0, 0);
        if (soundEnabled)
            Gdx.graphics.drawPixmap(Assets.buttons, 32, 370, 0, 0, 51, 51);
        else
            Gdx.graphics.drawPixmap(Assets.buttons, 32, 370, 50, 0, 51, 51);
    }
    ...
}
    {% endhighlight %}

*Gdx.input* is the reference to the input subsystem of the framework. It must be initialized in *onCreate* method of the class *MyActivity* as we have already done for the file subsystems and graphics.

    {% highlight java %}
public void onCreate(Bundle savedInstanceState) {
    ...
    input = new AndroidInput(this, renderView, scaleX, scaleY);
    ...
    Gdx.graphics = graphics;
    Gdx.fileIO = fileIO;
    Gdx.input = input;
    Gdx.game = this;
}
    {% endhighlight %}

To execute the code you can perform the procedure seen in paragraph 1.4. The source code the exercise can be found [here](https://github.com/sasadangelo/HelloWorldApp/archive/0.0.7.zip).
