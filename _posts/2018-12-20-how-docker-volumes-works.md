---
layout: post
title: How Docker Volumes works
post_series_id: getting-started-with-docker
slug: how-docker-volumes-works
thumbnail: wp-content/uploads/2018/12/types-of-mounts-volume-mini.png
excerpt: In this article, I want to discuss how docker volumes works and how to use them to separate application binaries from data for easy upgrade.
categories: Virtualization
---

![How Docker volumes works]({{ site.baseurl }}/wp-content/uploads/2018/12/types-of-mounts-volume-mini.png){:width="393" height="200" .responsive_img}

# How Docker volumes works
_Posted on **{{ page.date | date_to_string }}**_

This is the sixth article of the [Getting started with Docker]({{ site.baseurl }}/getting-started-with-docker/) series. In this article, I want to discuss how docker volumes work and how to use them to separate an application from its data.

## The upgrade problems

In the [first article]({{ site.baseurl }}/getting-started-with-docker/) of this series, in the **“Why Docker?”** section we discussed why docker technology became so popular in recent years. Docker in modern application infrastructure allows us to easily manage the application lifecycle simplifying its deployment. One of the major pain in application deployment is the upgrade. With Docker, it is a simple container replacement.

However, in our [PostgreSQL cluster]({{ site.baseurl }}/install-postgresql-cluster-docker/), we have a problem. The data folder (_/home/postgres/data_) is inside the container so if we replace a container we lost the data directory and the configuration.

**How we can solve this issue?** Docker allows the separation between binaries, data, and configuration with the **volumes**. Basically, you can allocate space on the host system and share it with the container, when it is destroyed space still exists.

## Docker storage types

Docker has three options for containers to store files in the host machine so that the files are persisted even after the container stops.

- volumes
- bind mounts
- tmpfs mount (only on Linux)

**Volumes** are stored in a part of the host filesystem which is managed by Docker (_/var/lib/docker/volumes_ on Linux). Non-Docker processes should not modify this part of the filesystem. Volumes are the best way to persist data in Docker.

**Bind mounts** are the folder on the host system shared with the container. Non-Docker processes on the Docker host or a Docker container can modify them at any time.

![types of mounts volume]({{ site.baseurl }}/wp-content/uploads/2018/12/types-of-mounts-volume.png){:width="450" height="229" .responsive_img}

_Photo from [https://docs.docker.com](https://docs.docker.com/storage/volumes/)_

**Tmpfs mount** is a disk space in memory very useful when the container needs to quickly manipulate files. Imagine, for example, an application that receives zip files that must be expanded to do some activities. In this scenario, a temporary filesystem is perfect to improve performance.

### Volumes vs Bind mounts

For our PostgreSQL cluster, both volumes and bind mounts are good solutions to persist data outside the container and separate them from the binaries. However, there are some benefits in using volumes over bind mounts. From the [official documentation](https://docs.docker.com/storage/volumes/) here a list of some of them:

- Volumes are easier to back up or migrate than bind mounts.
- You can manage volumes using Docker CLI commands or the Docker API.
- Volumes work on both Linux and Windows containers.
- Volumes can be more safely shared among multiple containers.
- Volume drivers let you store volumes on remote hosts or cloud providers, to encrypt the contents of volumes, or to add other functionality.
- New volumes can have their content pre-populated by a container.

However, if we need to have a storage space of a specific filesystem we cannot use volumes because their filesystem is the one present under the folder_/var/lib/docker/volumes_ on the host system and we cannot change it. If the application needs a specific filesystem we need to allocate it on the host system and share it with the container via bind mounts.

## Docker volumes cheat sheet

The docker commands that we need to learn to manage volumes are few. To create a Docker volume you can use the command:

    {% highlight shell %}
docker volume create <volume name>
    {% endhighlight %}

You can check the volume created with the command:

    {% highlight shell %}
docker volume ls
    {% endhighlight %}

Once created the volume and container lifecycles are unrelated. If the volume is not required any more you can remove it with the command:

    {% highlight shell %}
docker volume rm <volume name>
    {% endhighlight %}

If you want to bind mounts a host folder or a volume to a container use the following command:

    {% highlight shell %}
docker run -it -v <host folder or volume name>:<container folder> <image name> /bin/bash
    {% endhighlight %}

The same -v option can be used with the “docker create” command:

    {% highlight shell %}
docker create -it -v <host folder or volume name>:<container folder> <image name> /bin/bash
    {% endhighlight %}

## How to change PostgreSQL cluster code

In the [fifth article]({{ site.baseurl }}/install-postgresql-cluster-docker/), we discussed how to create a PostgreSQL cluster with three containers. In order to have an upgradable cluster, we need to separate PostgreSQL binaries from data and logs.

### Script for volumes managements

As a first step, we need the script [_build\_volumes.sh_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster-volume/build_volumes.sh) to create the three volumes.

    {% highlight shell %}
NODE1_VOLUME=volume1
NODE2_VOLUME=volume2
NODE3_VOLUME=volume3

docker volume create ${NODE1_VOLUME}
docker volume create ${NODE2_VOLUME}
docker volume create ${NODE3_VOLUME}
    {% endhighlight %}

Here the code of the relative [_clean\_volumes.sh_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster-volume/clean_volumes.sh) script.

    {% highlight shell %}
NODE1_VOLUME=volume1
NODE2_VOLUME=volume2
NODE3_VOLUME=volume3

docker volume rm ${NODE1_VOLUME}
docker volume rm ${NODE2_VOLUME}
docker volume rm ${NODE3_VOLUME}
    {% endhighlight %}

### Modify the start\_containers.sh script

We need to modify the [_start\_containers.sh_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster-volume/start_containers.sh) to bind mount the volumes to the three containers.


    {% highlight shell %}
...
NODE1_VOLUME=volume1
NODE2_VOLUME=volume2
NODE3_VOLUME=volume3
...
docker volume inspect ${NODE1_VOLUME} > /dev/null
if [ $? -ne 0 ]
then
    echo "ERROR: ${NODE1_VOLUME} doesn't exist. Run the script "./build_volumes" first."
    exit 1
fi

docker volume inspect ${NODE2_VOLUME} > /dev/null
if [ $? -ne 0 ]
then
    echo "ERROR: ${NODE2_VOLUME} doesn't exist. Run the script "./build_volumes" first."
    exit 1
fi

docker volume inspect ${NODE1_VOLUME} > /dev/null
if [ $? -ne 0 ]
then
    echo "ERROR: ${NODE1_VOLUME} doesn't exist. Run the script "./build_volumes" first."
    exit 1
fi
...
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE1_PRIVATE_IP} --hostname ${NODE1_NAME} --name ${NODE1_NAME} --env NODE_NAME=${NODE1_NAME} --env MASTER_NAME=${MASTER_NAME} -p ${NODE1_PORT}:5432 -v ${NODE1_VOLUME}:/home/postgres/data postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE2_PRIVATE_IP} --hostname ${NODE2_NAME} --name ${NODE2_NAME} --env NODE_NAME=${NODE2_NAME} --env MASTER_NAME=${MASTER_NAME} -p ${NODE2_PORT}:5432 -v ${NODE2_VOLUME}:/home/postgres/data postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE3_PRIVATE_IP} --hostname ${NODE3_NAME} --name ${NODE3_NAME} --env NODE_NAME=${NODE3_NAME} --env MASTER_NAME=${MASTER_NAME} -p ${NODE3_PORT}:5432 -v ${NODE3_VOLUME}:/home/postgres/data postgresql /bin/bash

...
    {% endhighlight %}

The code first checks that volume exists and then binds mounts them to the containers.

### How to verify if the cluster is working?

The process is exactly the same as the [previous article]({{ site.baseurl }}/install-postgresql-cluster-docker/). This time even if you stop a container, no data loss occurs. The separation of data from binary allows you to run two new scenarios: upgrade and failover. You can find how to implement these scenarios [here](https://github.com/sasadangelo/docker-tutorials/tree/master/postgresql-cluster-volume).

## What's next?

In this article, we discussed how to use volumes or bind mounts to separate binaries from data e logs of an application. You can download the source code [here](https://github.com/sasadangelo/docker-tutorials) in the _postgresql-cluster-volume_ folder. In the [next article]({{ site.baseurl }}/how-docker-compose-works/), we will see how to manage the Docker build and runtime configuration with **Docker Compose** instead of helper scripts (i.e. build\_image.sh, clean\_image.sh, build\_volumes.sh, clean\_volumes.sh, start\_containers.sh, and stop\_containers.sh).
