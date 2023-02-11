---
layout: post
title: How Docker Networking works
post_series_id: getting-started-with-docker
slug: how-docker-networking-works
image: /wp-content/uploads/2018/07/docker-bridge-network-mini.png
excerpt: In this article, I&#039;ll talk about how Docker networking. You&#039;ll learn how to let two containers communicate when they are on the same or different host.
categories:
- Networking
- Virtualization
---

![How docker networking works]({{ site.baseurl }}/wp-content/uploads/2018/07/docker-bridge-network-mini.png){:width="214" height="200" .responsive_img}

# How docker networking works
_Posted on **{{ page.date | date_to_string }}**_

This is the fourth article of the [Getting started with Docker]({{ site.baseurl }}/getting-started-with-docker/) series. In this article, I want to discuss a bit about how Docker networking works. These concepts will be used to modify the PostgreSQL code to create three containers that communicate with each other via TCP/IP.

## Networking overview in Docker

Docker has a pluggable networking system where plugins are called drivers. Docker provides by default some drivers whose names are:

1. **bridge**;
2. **host**;
3. **overlay**;
4. **macvlan**;
5. **none**.

When a container uses the type **none** the networking is disabled.

### The bridge networking

The **bridge** driver is the default one and it creates a private network that allows containers to communicate with each other. Behind the scenes, the Docker Engine creates the necessary Linux bridges, internal interfaces, IP-tables rules, and host routes to make this connectivity possible.

External access is granted by exposing ports to containers. In the following photo, you can see the containers _web_ and _db_ attached to the same bridge driver on the same host that allow them to communicate.

![Docker Bridge Network]({{ site.baseurl }}/wp-content/uploads/2018/07/docker-bridge-network.png){:width="450" height="420" .responsive_img}

_Photo from [https://blog.docker.com](https://blog.docker.com/2016/12/understanding-docker-networking-drivers-use-cases/)_

### The host networking

The **host** driver allows the container to use directly the host network facility without any mapping. This driver is particularly useful in scenarios where networking sharing between containers is not necessary. In the following image, you can see the containers _C1_ and _nginx_ share the same host network interface.

![Docker Host Networking]({{ site.baseurl }}/wp-content/uploads/2018/07/docker-host-networking.png){:width="450" height="329" .responsive_img}

### The overly networking

The **overlay** driver allows the communication between containers running on different hosts.

![Docker Overlay Networking]({{ site.baseurl }}/wp-content/uploads/2018/07/docker-overlay-networking.png){:width="450" height="235" .responsive_img}

### The macvlan networking

The **macvlan** driver allows assigning a Mac address to a container. Using this driver is sometimes the best choice when dealing with legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host’s network stack.

![Docker macvlan driver]({{ site.baseurl }}/wp-content/uploads/2018/07/docker-macvlan.png){:width="450" height="516" .responsive_img}

In this article series, I want to focus mainly on the bridge driver because we will use it to allow our cluster containers to communicate. If you want more details on Docker network driver you can read the [official documentation](https://docs.docker.com/network/).

## Docker networking commands

The command to create a network using a bridge driver is:

    {% highlight shell %}
docker network create -d bridge --gateway=GATEWAY --subnet=SUBNET/NETWORK_PREFIX_BITS NETWORK_NAME
    {% endhighlight %}

for example, suppose we want to create the subnet 10.1.1.0 we can have the following values:

- GATEWAY=10.1.1.1
- SUBNET=10.1.1.0
- NETWORK\_PREFIX\_BITS=24.

The same command can be used to create other network type specifying the driver name with the -d option.

After the creation of a network, we can create a container attached to it with its own hostname and IP address using the following command.

    {% highlight shell %}
docker create -it --net NETWORK_NAME --ip IP --hostname HOSTNAME--name CONTAINER_NAME --publish HOST_SSH_PORT:22 TAG /bin/bash
    {% endhighlight %}

The TAG is the name of the image used to create the container. CONTAINER\_NAME is the name of the container. NETWORK\_NAME is the name of the network and HOSTNAME and IP are, respectively, the hostname and the IP assigned to the container.

Other containers on the same network can reference the container using the IP address or the hostname. The host system references the container using localhost and services or ports exposed.

## Create the three PostgreSQL containers

In this section, we can modify the [start\_containers.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-network/start_containers.sh) script to create three PostgreSQL containers that communicate with each other via TCP/IP. Each container has a hostname and IP assigned.

    {% highlight shell %}
NODE1_NAME=node1
NODE2_NAME=node2
NODE3_NAME=node3

NODE1_PORT=5432
NODE2_PORT=5433
NODE3_PORT=5434

NODE1_PRIVATE_IP=10.0.2.31
NODE2_PRIVATE_IP=10.0.2.32
NODE3_PRIVATE_IP=10.0.2.33

PRIVATE_NETWORK_NAME=node_private_bridge

docker network create -d bridge --gateway=10.0.2.1 --subnet=10.0.2.1/24 ${PRIVATE_NETWORK_NAME}

docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE1_PRIVATE_IP} --hostname ${NODE1_NAME} --name ${NODE1_NAME} -p ${NODE1_PORT}:5432 postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE2_PRIVATE_IP} --hostname ${NODE2_NAME} --name ${NODE2_NAME} -p ${NODE2_PORT}:5432 postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE3_PRIVATE_IP} --hostname ${NODE3_NAME} --name ${NODE3_NAME} -p ${NODE3_PORT}:5432 postgresql /bin/bash
docker start ${NODE1_NAME}
docker start ${NODE2_NAME}
docker start ${NODE3_NAME}
    {% endhighlight %}

We created the _node\_private\_bridge_ bridge network with subnet _10.0.2.1/24_ and gateway _10.0.2.1_. Then we assigned to each container a hostname and an IP.

We modified the [stop\_containers.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-network/stop_containers.sh) script to clean up the three containers and the network driver.

    {% highlight shell %}
NODE1_NAME=node1
NODE2_NAME=node2
NODE3_NAME=node3

NODE1_PORT=5432
NODE2_PORT=5433
NODE3_PORT=5434

NODE1_PRIVATE_IP=10.0.2.31
NODE2_PRIVATE_IP=10.0.2.32
NODE3_PRIVATE_IP=10.0.2.33

PRIVATE_NETWORK_NAME=node_private_bridge

docker network create -d bridge --gateway=10.0.2.1 --subnet=10.0.2.1/24 ${PRIVATE_NETWORK_NAME}

docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE1_PRIVATE_IP} --hostname ${NODE1_NAME} --name ${NODE1_NAME} -p ${NODE1_PORT}:5432 postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE2_PRIVATE_IP} --hostname ${NODE2_NAME} --name ${NODE2_NAME} -p ${NODE2_PORT}:5432 postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE3_PRIVATE_IP} --hostname ${NODE3_NAME} --name ${NODE3_NAME} -p ${NODE3_PORT}:5432 postgresql /bin/bash
docker start ${NODE1_NAME}
docker start ${NODE2_NAME}
docker start ${NODE3_NAME}
    {% endhighlight %}

You can now access to whatever container with the command:

    {% highlight shell %}
docker exec -it nodeX /bin/bash
    {% endhighlight %}

where X could be 1, 2, or 3, and ping the other two containers using the node name or the IP.

## What's next?

In this article, we explained the docker network capabilities focusing mainly on the bridge driver, we modified the PostgreSQL project code to create three containers that communicate with each other via TCP/IP. In the [next article]({{ site.baseurl }}/install-postgresql-cluster-docker/), we will use these three containers to create a PostgreSQL cluster.
