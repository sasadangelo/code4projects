---
layout: post
title: Android Files Management
post_series_id: android-game-programming
slug: android-files-management
thumbnail: assets/img/android-file.jpeg
excerpt: This is the eighth article of the Android Game Programming series. In this article, I will discuss how to manage files
categories:
- Android
- Game Programming
---

![Android Files Management](assets/img/android-file.jpeg){:width="280" height="197" .responsive_img}

# Android Files Management
_Posted on **{{ page.date | date_to_string }}**_

This is the eighth article of the [Android Game Programming](android-game-programming) series. In this article, I will discuss how to manage **files** in Android.

## File Management

Android uses a file system similar to those on other platforms. In this section, we will see how to manage files in Android and we will use this knowledge later in our video game to save and read the highest scores made by players. This section assumes that you are already familiar with the basic concepts of **java.io** files and APIs.

### Internal and External Memory

All Android devices have two mass memories: “internal” and “external”. These names derive from the first days when Android was born when Android devices provided a built-in memory  (internal) often large just to contain the operating system and a few dozen applications and then a removable memory (external) called ” SD “where to install other applications. These are the rules that usually apply to these two types of memories.

**Internal Memory:**

-   it is always available;
-   Files saved here are only accessible by your application.
-   When the user uninstalls your application, the system removes all application files.

Using internal memory is convenient when you want data to be inaccessible to the user or other applications.

**External memory:**

-   it is not always available. The user may decide to remove it temporarily or permanently.
-   It is readable by everyone, so the files saved here can be read by all applications.
-   When the user uninstalls your application, the system only removes the files stored in the folder returned by the getExternalFilesDir () API.

External memory is the ideal place for files that do not require special restrictions and can be shared by multiple applications. By default the applications are installed in the internal memory, you can specify the android: installLocation attribute in the manifest to install the application on the external memory. Users typically appreciate this option especially when the APK file size is large.

![SD Card External Storage](assets/img/sd-card-external-storage.jpeg){:width="450" height="253" .responsive_img}

### External Memory Permissions

In order for your application to write to external memory, it must request the WRITE\_EXTERNAL\_STORAGE permissions in the manifest file:

{% highlight xml %}
<manifest ...>
    ...
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    ...
</manifest>
{% endhighlight %}

### Read and Write on External Memory

There is a lot to write about Android files management on both internal memory and external memory, but the purpose of this article is to allow you to write your first video game in the shortest possible time and explaining only the concepts you will need for this purpose. Reading and writing files in Android uses the same Java java.io APIs that you already know: _InputStream_, _OutputStream_, _FileInputStream,_ and _FileOutputStream_. The only problem is knowing on which path the SD card is mounted on. To know this, simply use the _Environment.getExternalStorageDirectory().getAbsolutePath()_ API.

## Read and save scores in a file

In this section, we will begin to add functionality to [our “Hello World” application](how-to-create-an-android-application) by including the ability to read and write files to and from external memory. We will use this file to read and write to a file the 5 highest scores reached with the video game. Since we haven’t implemented it yet we will use 5 fake scores such as 100, 80, 50, 30 and 10.

Here we will put the first brick for the construction of our framework that you can use to write many video games.

We create the package _org.androidforfun.framework_ e _org.androidforfun.framework.impl_ that will contain the source code of our game framework. The first one will contain the interfaces and the second their implementations. If you want, you can add implementations for other platforms in the future. In the first package we create the [_FileIO_ interface](https://github.com/sasadangelo/HelloWorldApp/blob/0.0.2/app/src/main/java/org/androidforfun/framework/FileIO.java) with only two methods:

-   _readFile_
-   _writeFile_

These two methods will have to open an input and output stream to a file that will reside on the external memory. We create the [_AndroidFileIO_ class](https://github.com/sasadangelo/HelloWorldApp/blob/0.0.2/app/src/main/java/org/androidforfun/framework/impl/AndroidFileIO.java) in the _org.androidforfun.framework.impl_ package which will implement these two methods.

We now create a [_Settings_ class](https://github.com/sasadangelo/HelloWorldApp/blob/0.0.2/app/src/main/java/org/androidforfun/droids/model/Settings.java) in the _org.androidforfun.droids.model_ package that we will use to read and write the 5 scores on the file. The _load_ method loads the 5 scores from the file and stores them in the static high scores array. The save method does the opposite. Finally, the _addScore_ method adds new scores to the ranking. If a new score is higher than the first 5, the last one will be excluded and the new one will be inserted respecting the descending order.

We modify the file _[AndroidManifest.xml](https://github.com/sasadangelo/HelloWorldApp/blob/0.0.2/app/src/main/AndroidManifest.xml)_ adding the permissions to write on the card External SD card.

{% highlight xml %}
    ...
    </application>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
</manifest>
{% endhighlight %}

We also change the layout file [_activity\_my.xml_](https://github.com/sasadangelo/HelloWorldApp/blob/0.0.2/app/src/main/res/layout/activity_my.xml) in order to associate an id with the _TextView_, so that we can then modify it from Java code.

{% highlight xml %}
<TextView android:id="@+id/TextView" android:text="@string/hello_world" android:layout_width="wrap_content" android:layout_height="wrap_content" />
{% endhighlight %}

Finally, we modify the _onCreate_ method of the [MyActivity class](https://github.com/sasadangelo/HelloWorldApp/blob/0.0.2/app/src/main/java/org/androidforfun/helloworldapp/MyActivity.java) by adding the following code after the call to _setContentView_.

{% highlight java %}
FileIO fileIO = new AndroidFileIO();
Settings.addScore(5000);
Settings.addScore(4000);
Settings.addScore(3000);
Settings.addScore(2000);
Settings.addScore(1000);
Settings.save(fileIO);
Settings.addScore(9999);
Settings.addScore(8888);
Settings.addScore(7777);
Settings.addScore(6666);
Settings.addScore(6666);
Settings.load(fileIO);
StringBuffer s = new StringBuffer();
for (int i: Settings.highscores) {
    s.append(i);
    s.append(" ");
}
TextView textView = (TextView) this.findViewById(R.id.TextView);
textView.setText(s);
{% endhighlight %}

The purpose of this code is to add 5 scores to the rankings: 5000, 4000, 3000, 2000 and 1000; and save them to disk. Then change the rankings by adding 5 higher scores. In the end, we reload the previously saved values to show them on video. On the video, the saved scores should be visible and not those added after even higher.

To execute the code of this section you can perform the [procedure here](how-to-create-an-android-application). The source code for the exercise [can be found here](https://github.com/sasadangelo/HelloWorldApp/archive/0.0.2.zip).