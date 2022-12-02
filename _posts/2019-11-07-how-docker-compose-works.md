---
layout: post
title: How Docker Compose works
post_series_id: getting-started-with-docker
slug: how-docker-compose-works
thumbnail: assets/img/docker-compose.png
excerpt: This is the seventh article of the Getting started with Docker series. Here I will discuss Docker Compose and how to use it to improve the container orchestration.
categories: Virtualization
---

![How Docker Compose works](assets/img/docker-compose.png){:width="200" height="200" }

# How Docker Compose works
_Posted on **{{ page.date | date_to_string }}**_

This is the seventh article of the [Getting started with Docker](getting-started-with-docker) series. In this article, I will discuss Docker Compose and how to use it to improve the code developed so far for our PostgreSQL cluster.

## Image build and runtime configuration

In the code developed so far, we used some helper scripts to create and clean up the _postgresql_ image and volumes, to start and stop the containers. If the application you are building requires more than one container you can manage the image build and runtime configuration with a new Docker tool: Docker Compose.

## What is Docker Compose?

Docker Compose is a command-line tool that talks with the docker engine and it is able to manage multi containers applications deployed on a single node. The tool is able to build the application docker image and runtime configuration like port mapping, bind and volumes mounts, networking, IPC, and so on.

You can think of the Docker Compose command line as a wrapper that extends the functionalities of the docker command line.

Docker Compose takes in input a YAML file and uses it to create one or more services (the applications) deployed in one or more containers. The YAML file, for each service, specifies the Docker image to use and how to configure it at runtime.

## Docker Compose commands

The following commands work exactly the same as their docker counterparts, the only difference is that they can affect more than one container.

{% highlight shell %}
    docker-compose pull
    docker-compose build
    docker-compose run
    docker-compose exec
    docker-compose create
    docker-compose start
    docker-compose stop
    docker-compose restart
    docker-compose pause
    docker-compose unpause
    docker-compose top
    docker-compose logs
{% endhighlight %}

The most important Docker Compose commands are:

{% highlight shell %}
    docker-compose up
    docker-compose down
{% endhighlight %}

The former builds the required docker image if they don’t exist and start the containers. The latter stop the containers and other docker resources.

For more details on docker-compose commands read the [official documentation](https://docs.docker.com/compose/reference/overview/).

## Create the PostgreSQL cluster with Docker Compose

The goal of this section is to modify our PostgreSQL application to leverage on Docker Compose to improve the code removing all the helpers’ scripts used so far.

To do that, we need to create the YAML file where we define three PostgreSQL services (applications), each one having:

-   the definition of the PostgreSQL docker image
-   a docker volume where store the data;
-   networking connection with IP, Port, and hostname assigned;

### The YAML File

[Here](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster-compose/docker-compose/docker-compose.yml) you can see the YAML file. The tag _version_ specifies the version of the YAML file.

{% highlight yaml %}
    version: '3.6'
{% endhighlight %}

Then we define the three service volumes.

{% highlight yaml %}
    volumes:
        volume1:
        volume2:
        volume3:
{% endhighlight %}

The services tag defines the three services (applications) to manage: node1, node2, and node3.

{% highlight yaml %}
    services:
        node1:
            ...

        node2:
            ...

        node3:
            ...
{% endhighlight %}

Let’s see in detail the definition of one of these services. The container has a name and it has the image _postgresql_ as a template. If the image doesn’t exist in the local docker registry a new one is built using the [Dockerfile](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster-compose/src/Dockerfile) in ../src.

{% highlight yaml %}
    node1:
        container_name: node1
        build:
            context: ../src
            dockerfile: Dockerfile
            image: postgresql:latest
{% endhighlight %}

The service will use the following environment variable whose values are in the [.env](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster-compose/docker-compose/.env) file.

{% highlight yaml %}
    environment:
        NODE_NAME: node1
        MASTER_NAME: $MASTER_NAME
{% endhighlight %}

Container port 5432 maps on host 5432 port. The other two containers map the local 5432 port host port 5433 and 5434.

{% highlight yaml %}
    ports:
        - "5432:5432"
{% endhighlight %}

All three containers store logs and data directory in _/home/postgres/data_ mapped with docker volumes.

{% highlight yaml %}
    volumes:
        - volume1:/home/postgres/data
{% endhighlight %}

Finally, the container connects to the network bridge driver and has IP 10.0.2.31 and hostname node1.domain.com.

{% highlight yaml %}
    networks:
        cluster:
            ipv4_address: 10.0.2.31
            aliases:
                - node1.domain.com
{% endhighlight %}

Here the definition of the bridge driver with subnet 10.0.2.1/24.

{% highlight yaml %}
    networks:
        cluster:
            driver: bridge
            ipam:
                config:
                    - subnet: 10.0.2.1/24
{% endhighlight %}

## How to test the cluster?

To start the cluster you can type the following command.

{% highlight shell %}
docker-compose up -d
{% endhighlight %}

The test of the upgrade and failover scenarios is exactly the same as the [previous article](how-docker-volumes-works). The only difference is that this time you can use the **docker-compose** command instead of the **docker** one.

To shut down the cluster you can type the following command.

{% highlight shell %}
docker-compose down
{% endhighlight %}

This command does not remove the volume so the data still exists. If you start again the cluster no data loss occurs. If you want to remove the volume **you can add the -d option** to the command.

## What’s next?

In this article, we explained what Docker Compose is and how to use it to deploy multi containers application on a single host. However, have a database cluster with all containers on a single node is ok in development and test environments but makes no sense in production because if the node goes down the whole cluster crash. In the next article, to solve this issue and implement a real High Availability solution we need to leverage on Docker Swarm.