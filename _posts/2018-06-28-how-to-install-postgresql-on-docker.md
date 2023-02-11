---
layout: post
title: How to install PostgreSQL on Docker
post_series_id: getting-started-with-docker
slug: how-to-install-postgresql-on-docker
image: /wp-content/uploads/2018/06/postgres_and_docker.png
excerpt: This is the second article of Getting started with Docker series. You&#039;ll learn how to install PostgreSQL on a Docker container.
categories: 
- Virtualization
- Database
---

![How to install PostgreSQL on Docker]({{ site.baseurl }}/wp-content/uploads/2018/06/postgres_and_docker.png){:width="422" height="200" .responsive_img}

# How to install PostgreSQL on Docker
_Posted on **{{ page.date | date_to_string }}**_

This is the third article of the [Getting started with Docker]({{ site.baseurl }}/getting-started-with-docker/) series. Here I want to show you how to use Docker to create a container where you can install PostgreSQL.

## Create the Docker image with Dockerfile

The first step of this tutorial is to write the Dockerfile for our PostgreSQL application. This is the code of our [Dockerfile](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql/src/Dockerfile).

    {% highlight docker %}
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y postgresql iputils-ping net-tools \
    netcat vim
RUN mkdir -p /home/postgres/data/postgres && \
    mkdir -p /home/postgres/data/logs && \
    mkdir -p /usr/local/bin/cluster/postgresql && \
    chown -R postgres:staff /home/postgres/ && \
    chmod 700 /home/postgres/data/postgres
USER postgres
COPY ./postgresql /usr/local/bin/cluster/postgresql
EXPOSE 5432
ENTRYPOINT /usr/local/bin/cluster/postgresql/entrypoint.sh
    {% endhighlight %}

Line 1 specifies that Ubuntu 16.04 is the starting point for our image. On line 2 we have the **RUN** command that installs the PostgreSQL package plus some additional packages containing useful tools for developing and debugging (i.e. ping, nc, vim, and netstat). Line 4 contains another **RUN** command we will use to create the PostgreSQL data and log directories plus a folder that will contain the startup scripts. Line 9 has the **USER** command that switches the current user to **postgres**. From this moment on all the commands will be executed by the postgres user. On line 10 the **COPY** command copy all the startup scripts in the container folder _/usr/local/bin/cluster/postgresql_.  Line 11 the **EXPOSE** command exposes the 5432 port that is the port on which PostgreSQL will listen. Finally, line 12 the **ENTRYPOINT** command specifies the script that will be launched at startup.

To create the image we define the script [_build\_image.sh_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql/build_image.sh) that will use the “_docker build”_ command to create the image. Here the content of the script.

    {% highlight shell %}
docker build src -t postgresql
    {% endhighlight %}

The image name is **postgresql** and you can see it with the “_docker image ls”_ command. I created a second script called [_clean\_image.sh_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql/clean_image.sh) to drop the image when it is not necessary anymore. Here the code of this script.

    {% highlight shell %}
docker image rm -f postgresql
    {% endhighlight %}

## How to create the Docker container

The Docker container is created with the script [start\_containers.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql/start_containers.sh):

    {% highlight shell %}
NODE1_NAME=node1
NODE1_PORT=5432
docker create -it --name ${NODE1_NAME} -p ${NODE1_PORT}:5432 postgresql /bin/bash
docker start ${NODE1_NAME}
    {% endhighlight %}

The script uses the “_docker create_” command to create the container starting from the image **_postgresql_**. This command creates the container in a detached mode so you can access it or exit it without losing changes. The internal port 5432 on which PostgreSQL listens will be mapped on the same port on the host environment. The command “_docker start_” will start the container. The container can be destroyed by the script [stop\_container.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql/stop_containers.sh) that stop and remove the container.

    {% highlight shell %}
NODE1_NAME=node1
docker stop ${NODE1_NAME}
docker rm ${NODE1_NAME}
    {% endhighlight %}

The container is created and it is up and running, to access it use the following command.

    {% highlight shell %}
docker exec -it CONTAINER_ID /bin/bash
    {% endhighlight %}

As usual, you can get the CONTAINER\_ID with the command “_docker container ls_” and use the one related to the _postgresql_ image.

## The startup and config scripts

When Docker starts the container, it executes the script [_/usr/local/bin/cluster/postgresql/entrypoint.sh_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql/src/postgresql/entrypoint.sh). This script runs the _/usr/local/bin/cluster/postgresql/bin/entrypoint.sh_ script and wait for its completion.

    {% highlight shell %}
#!/bin/bash
set -e
echo '>>> STARTUP POSTGRESQL ...'
/usr/local/bin/cluster/postgresql/bin/entrypoint.sh & wait ${!}
EXIT_CODE=$?
echo ">>> POSTGRESQL TERMINATED WITH EXIT CODE: $EXIT_CODE"
exit $EXIT_CODE
    {% endhighlight %}

The _/usr/local/bin/cluster/postgresql/bin/entrypoint.sh_ script will be responsible to create the data directory (line 3), copy the configuration files (lines 5 and 6), and start PostgreSQL (line 8).

    {% highlight shell %}
#!/bin/bash
echo ">>> CREATE DATA DIRECTORY"
/usr/lib/postgresql/9.5/bin/initdb -D /home/postgres/data/postgres
echo ">>> COPY CONFIGURATION FILES"
cp /usr/local/bin/cluster/postgresql/config/postgresql.conf /home/postgres/data/postgres
cp /usr/local/bin/cluster/postgresql/config/pg_hba.conf /home/postgres/data/postgres
echo ">>> START POSTGRESQL ON NODE $NODE_NAME"
/usr/lib/postgresql/9.5/bin/postgres -D /home/postgres/data/postgres > /home/postgres/data/logs/postgres.log 2>&1
    {% endhighlight %}

## Test the Docker Container

As a prerequisite to testing the Docker container, you need to install PostgreSQL client on your host system. I use Mac and the command to install it is:

    {% highlight docker %}
brew install libpq
    {% endhighlight %}

Windows and Linux systems have an equivalent command you can search by google. Build the image and start the container:

    {% highlight shell %}
./build_image.sh
./start_containers.sh
    {% endhighlight %}

Now you can access PostgreSQL with the command:

    {% highlight shell %}
psql -h localhost -p 5432 -U postgres
    {% endhighlight %}

Once you logged in PostgreSQL you can create a database.

    {% highlight sql %}
CREATE DATABASE mydb;
    {% endhighlight %}

You can check its creation with the command **\\list**. To quit from _psql_ command line use the command **\\q**.

## What's next?

In this article, we created a simple Docker container where we installed a PostgreSQL database server.  You can [download the sample code here](https://github.com/sasadangelo/docker-tutorials) in the _postgresql_ folder. In the [next article]({{ site.baseurl }}/how-docker-networking-works/), I will explain how Docker networking works. This step is a prerequisite to creating our cluster.
