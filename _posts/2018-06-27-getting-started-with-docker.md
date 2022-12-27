---
layout: post
title: Getting Started with Docker
post_series_id: getting-started-with-docker
slug: getting-started-with-docker
thumbnail: assets/img/docker-logo-mini.png
excerpt: In this article, you will learn what Docker is, its main concepts, how to create images and containers and the commands to play with it.
categories: Virtualization
sitemap:
  lastmod: 2018-06-27
  priority: 0.7
  changefreq: 'weekly'
---

![Docker](assets/img/docker-logo-mini.png){:width="258" height="200" .responsive_img}

# Getting Started with Docker
_Posted on **{{ page.date | date_to_string }}**_

This is the first article of **Getting started with Docker** series. Here I would like to explain what is Docker and how I use it in my day by day job. To make this series more practical, I will show you how to write your first “Hello World!” containerized application. In the next articles, I will show you how to create a PostgreSQL cluster.

## Why Docker?

Docker is a hot technology adopted by the most important companies in the world. The following picture shows the adoption growth in recent years.

![Docker adoption](assets/img/docker-adoption.png){:width="450" height="241" .responsive_img}

This other picture shows some numbers relative to Docker. It’s clear that in recent five years the technology acquired a good momentum and its adoption has grown very fast.

![Docker statistics](assets/img/docker-numbers.png){:width="450" height="165" .responsive_img}

_Photo from [www.slideshare.net](https://www.slideshare.net/Docker/introduction-to-docker-2017)_

However, containerization is not a new concept and as you can see in the following figure it goes back to 2004. The question now is **why the containerization has become so important only in recent years?**

![Docker History](assets/img/history-of-docker.png){:width="450" height="252" .responsive_img}

_Photo from [www.slideshare.net](https://www.slideshare.net/Docker/introduction-to-docker-2017)_

### Why Docker is so important?

To understand why Docker has this huge momentum you have to consider the problems that it solves from the perspective of the three main actors of the technology landscape: **developers**, **operators**, and **companies**.

#### Developers

The company behind Docker has always described the program as fixing the _“it works on my machine”_ problem. This is a very old problem that always tormented developers. Usually, a developer creates an application that works fine on his machine but it doesn’t in a test or production environment.

The problem happens because the development environment configuration could not perfectly match with the one in test or production environments. Docker solves this issue because the container encapsulates the application with all its dependencies so that it is the same in development, test, and production.

#### Operators

The operators besides being victims of the “it works on my machine” problem, sometimes they must deploy applications according to requirements that don’t fit with the original design or they should fight with applications that are too sensitive to the environment configuration.

For example, imagine an operator need to deploy application A on a server S. Then to save cost he needs to deploy another application B on the same server that for some reason cannot coexist with A. Docker solve this problem because a container encapsulates each application with its own dependencies. Moreover, Docker allows them to easily manage the application lifecycle  (deploy, upgrade, start, stop, removal) in a very easy and scalable way.

#### Companies

Companies suffer from the same problems above with a higher order of magnitude because they have a lot of employees that are developers and/or operators. However, the great benefit that Docker provides to them must be identified in the way in which they design modern applications.

Twenty years ago applications were a unique monolithic piece of code. Usually,  these applications were managed by large teams and contained thousands of lines of code. Maintenance of these applications was hard because any change in the code required its complete build and deploy to test it.

In recent years, application designers started to consider convenient divide the applications in microservices each one implementing specific application requirements. Small agile teams manage the lifecycle (development,  test, and deploy) of these microservices.  Maintain a small piece of code is easier than a big application and the release of new functionalities becomes faster.

Today hundreds of microservices compose applications like Netflix and manage their deployment lifecycle (install, configure, and upgrade) and dependencies is not an easy task. **Here where Docker comes into play**.

![Netflix Ecosystem](assets/img/netflix_ecosystem.png){:width="450" height="323" .responsive_img}

_Photo from [medium.com](https://medium.com/refraction-tech-everything/how-netflix-works-the-hugely-simplified-complex-stuff-that-happens-every-time-you-hit-play-3a40c9be254b)_

Microservices can be deployed in a container with all the dependencies. Deploy a microservice means deploy its container that usually occurs in few seconds without pains. Upgrade of the microservices is simply the removal of the old container and the add of the new one.

Microservices data usually are separated from the code so that the microservices are stateless and then more easy to update.

## What is Docker?

When I started working with Docker, the first thing I needed to learn was what Docker really was and its main differences with a virtual machine. Here how Docker is defined on its [official website](https://docs.docker.com/engine/docker-overview/):

> Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.

From this definition, it’s clear that Docker is an isolated environment on your target system where your application runs with its own dependencies that are completely unrelated to the other software deployed on the system. This isolated environment is called **Container**.

![Container](assets/img/container.png){:width="289" height="258" .responsive_img}

More details about the differences between Containers and Virtual Machines will be discussed [here](containers-vs-virtual-machines).

The next thing I had to learn was the Container concept in detail. Docker is based mainly on this concept and in order to understand it, I needed to understand first the **Docker image** concept.

## What is a Docker Image?

A _Docker image_ is a read-only template with instructions for creating a Docker container. For example, you may build an image that is based on the Ubuntu operating system and installs the Apache web server and your application, as well as the configuration details needed to make it run. Often, an image is based on another image, with some additional customizations.

You might create your own images or you might only use those created by others and published in the [official Docker HUB](https://hub.docker.com/explore/). To build your own image, you create a _Dockerfile_ with a simple syntax for defining the steps needed to create and run it. Each instruction in a Dockerfile creates a layer in the image. When you change it and rebuild the image, only those layers which have changed are rebuilt. This is part of what makes images so lightweight, small, and fast when compared to other virtualization technologies.

## What is a Container?

According to the [official website](https://docs.docker.com/engine/docker-overview/#docker-objects), a Container is:

> a runnable instance of a docker image. You can create, start, stop, move, or delete a container using the Docker API or CLI. You can connect a container to one or more networks, attach storage to it, or even create a new image based on its current state. By default, a container is relatively well isolated from other containers and its host machine.

A container is the runnable instance of a docker image. You can have multiple containers running on a target system and the user that access to them has the feeling to be on an isolated system with its own filesystem, networking, volumes, IPC and so on. The main difference between containers and virtual machines is that these containers share the same kernel and use their isolation mechanisms (i.e. namespaces) to create the illusion of virtualization.

A container, however, is more efficient than a virtual machine because it does not add any layer between kernel and application but it only uses its isolation mechanism that does not degrade performance. This is the reason why modern architectures deploy a containerized version of applications in order to avoid classical dependencies problems of a normal on-premise application.

![Container vs VM](assets/img/container-vs-vm.png){:width="450" height="201" .responsive_img}

## How to install Docker

Docker official documentation contains [detailed steps to install it](https://docs.docker.com/docker-for-mac/install/#where-to-go-next), I suggest following the instructions reported there to install the product on your machine. I suggest also to read the [Getting Started](https://docs.docker.com/docker-for-mac/) guide to get familiar with the Docker CLI commands.

## Docker cheat sheet

Start learning Docker from the official documentation is a MUST for whoever wants to be serious about it. However, to start playing with Docker it is sufficient to know very few commands and practice with them.

For this reason, I created this cheat sheet with the most important commands that I use every day. You can start with them to get familiar with the platform. Once you learn them, read the official documentation will be easier.

To list all the available images you can use the following command:

    {% highlight shell %}
docker image ls
    {% endhighlight %}

At the very beginning, the list is empty. Now suppose you want to download an Ubuntu 16.04 (Xenial) image and store it on your system. On the Docker HUB, you’ll [find a lot of images](https://hub.docker.com/explore/) you can start to play with. The command to run is the following:

    {% highlight shell %}
docker pull ubuntu:16.04
    {% endhighlight %}

Now if you run the “_docker image ls_” command the following will appear:

_ubuntu              16.04               a35e70164dfb        1 minute ago         222MB_

You have installed the image on your system. Start an instance of this image (the container) using the following command:

    {% highlight shell %}
docker run -it ubuntu /bin/bash
    {% endhighlight %}

You created a container called “ubuntu” with a bash shell you can use to run whatever Ubuntu command. In another host shell you can run the command to list all docker containers running on your system:

    {% highlight shell %}
docker container ls
    {% endhighlight %}

**Whenever you close a container you lost all the changes you applied to it**. In order to avoid this, you can create a snapshot of the current container state so you can recover it whenever you need it. The command to do that is:

    {% highlight shell %}
docker commit CONTAINER_ID TAG
    {% endhighlight %}

It creates a new image TAG with the status the container had when you committed it. The CONTAINER\_ID is the number that identifies the container and that you can retrieve it with the “_docker container ls_” command.

The strategy to commit containers to avoid to lose the work you have done on a Docker image is a good strategy but sometimes you need to create a custom image starting from a basic one downloaded from a docker registry and share it with your team or customers or simply using it as a starting point for your activities. In this case, could be useful to create it using a _Dockerfile_ and the Docker build capabilities.

## How to create a “Hello World!” Docker application

The first program you write when you learn a new programming language or technology is the classic “Hello World!”, an application that simply prints the “Hello World!” message.

To make things more interesting let’s create a Docker container with a web server (Nginx) listening on port 80 that accepts connection from a web browser and print the “Hello World!” message.

Here the _Dockerfile_ code to build the Docker image from which we will create our container.

    {% highlight docker %}
FROM ubuntu:16.04
RUN apt-get update; apt-get install -y nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./www-data /home/www/www-data
EXPOSE 80
CMD ["nginx"]
    {% endhighlight %}

**_FROM_** is the keyword used by Docker to specify the docker image to use as a starting point. In our example, we start with Ubuntu 16.04. In order to download software packages, you need to run the Ubuntu _apt-get update_ command. **_RUN_** is the keyword used by Docker to run a command on the target image. We will use it to install the Nginx package.

Then we use the **COPY** command to copy the [_nginx.conf_](https://github.com/sasadangelo/docker-tutorials/blob/master/hello-world/nginx.conf) file and the _www-data_ folder on the image. the nginx.conf file simply tells Nginx to listen on port 80 and retrieve files from folder _/home/www/www-data_. This folder will contain the [_index.html_](https://github.com/sasadangelo/docker-tutorials/blob/master/hello-world/www-data/index.html) file that prints the “Hello World!” message in the browser. Docker provides the **ADD** command that is similar to COPY, the only difference is that all the compressed files are uncompressed when copied on the container image. 

The command **EXPOSE** tells Docker to map the port 80 on which the web server listens. In this way, when we start the container we can map this port with a port on the host system.

Finally, the **CMD** command tells Docker which command to start when the container is started. In our case, the Nginx web server is started.

### Run the “Hello World!” application

To build this image you can run the following shell command:

    {% highlight shell %}
docker build -t TAG .
    {% endhighlight %}

Docker will build the Dockerfile in the current folder. If you issue the “_docker image ls_” command, you’ll notice the new image TAG appeared on the list. To run the docker image just created give the following command:

    {% highlight shell %}
docker run -d -p 80:80 TAG
    {% endhighlight %}

The -d option will start the container in detach mode so that the shell doesn’t hang.

Open your browser and type localhost in the address bar. You’ll see the “Hello World!” message appear.

![Docker Hello World application](assets/img/docker-hello-world.jpeg){:width="450" height="194" .responsive_img}

If you want, you can access the container using the command:

    {% highlight shell %}
docker exec -it CONTAINER_ID /bin/bash
    {% endhighlight %}

where you can retrieve the  CONTAINER\_ID with the “_docker container ls_” command.

## What’s Next?

In this article, you learned the basics of Docker and you wrote your first Docker application. You can download the source code from [here](https://github.com/sasadangelo/docker-tutorials) in the _hello-world_ folder. In the source code, you’ll find some helpers scripts (i.e. [build\_image.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/hello-world/build_image.sh), [clean\_image.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/hello-world/clean_image.sh), [start\_containers.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/hello-world/start_containers.sh), and [stop\_containers.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/hello-world/stop_containers.sh)) to build and cleanup the image and the container. In the [next article](containers-vs-virtual-machines), we will focus on the main differences between Containers and Virtuals Machines.