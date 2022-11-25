---
layout: post
title: How to transform your Kodi Box in a Netflix-like platform
post_series_id: raspberry-media-center
slug: kodi-box-media-library
thumbnail: assets/img/kodi-movies-library-mini.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories: Multimedia
---

![How to transform your Kodi Box in a Netflix-like platform](assets/img/kodi-movies-library-mini.png){:width="200" height="112" }

# How to transform your Kodi Box in a Netflix-like platform
_Posted on **{{ page.date | date_to_string }}**_

In this article, I’ll show you how to transform your Kodi Box in a Netflix-like platform. Before you read this article I assume:

1.  you already [built your own Kodi Media Center following these instructions](raspberry-media-center);
2.  you already [configured your own Kodi Media Center following these instructions](how-to-configure-kodi-media-center).

## Prepare your media files

In order to make your media file recognizable from your Library rename the title of your movies and TV Series using the following format.

For Movies use the Title and Year of Publication separated by “\_” and with the media extension:

{% highlight plaintext %}
<Title>_<Year>.<ext>
{% endhighlight %}

Here an example:

{% highlight plaintext %}
Alladin_1992.mkv
{% endhighlight %}

For TV Shows use the following format:

{% highlight plaintext %}
<Title>/<Title>_<Season>_<Season Number>/<Title>_<Episode Number>x<Season Number>.<ext>
{% endhighlight %}

Here an example:

{% highlight plaintext %}
Arrow/Arrow_Season_01/Arrow_01x01.avi 
{% endhighlight %}

## Create your Movies Library

Go on the Movies menu and click on Add videos.

![Kodi Movies Add Videos](assets/img/Kodi_Movies_Add_Videos.png)

Browse your Movies clicking on the Browse button and selecting the Root Filesystem.

![Kodi Movies Select Sources 2](assets/img/Kodi_Movies-Select_Sources_2.png)

Then select your movies folder that in our case is _/media/KODI/Movies_. Leave the default name Movies and click OK.

![Kodi Movies Select Sources 3](assets/img/Kodi_Movies-Select_Sources_3.png)

You have to tell Kodi that this folder contains Movies. To do that select “This directory contains”.

![Kodi Movies Select Sources 4](assets/img/Kodi_Movies-Select_Sources_4.png)

Specify that this folder contains Movies.

![Kodi Movies Select Sources 5](assets/img/Kodi_Movies-Select_Sources_5.png)

Leave the default settings and click OK.

![Kodi Movies Select Sources 6](assets/img/Kodi_Movies-Select_Sources_6.png)

Start to populate the Library selecting Yes when it asks “Do you want to refresh information for all items within this path?”.

![Kodi Movies Select Sources 7](assets/img/Kodi_Movies-Select_Sources_7.png)

The system will start to download Fan Art from the Movie Database for each film in the _/media/KODI/Movies_ folder.

![Kodi Movies Select Sources 8](assets/img/Kodi_Movies-Select_Sources_8.png)

## Create your TV Shows Library

With a similar procedure, you can create a TV Shows Library with a style similar to Netflix.

Go on TV Shows and click on Add videos. Follow the same procedure as above but this time select the /media/KODI/TVShows folder. When the system asks for media content, specify the folder contains TV Shows.

![Kodi TV Series](assets/img/Kodi-TV_Series.png)

## Improve Media Library Performance

Once you created the Media Library for Movies and TV Series you’ll notice that images load is a little bit slow. To speed it up and make the system responsive, you have to reduce the Kodi user interface resolution to 720p. Video will still play at full resolution (e.g. 1080p).

Go to Settings -> System -> Display -> Resolution to change the resolution.