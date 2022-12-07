---
layout: post
title: How to install PostgreSQL cluster on Docker
post_series_id: getting-started-with-docker
slug: install-postgresql-cluster-docker
thumbnail: assets/img/database-cluster.png
excerpt: This article series will teach you the main Docker concepts and how to use it in practice to install and configure a PostgreSQL cluster.
categories: 
- Virtualization
- Database
---

![How to install PostgreSQL cluster on Docker](assets/img/database-cluster.png){:width="385" height="200" .responsive_img}

# How to install PostgreSQL cluster on Docker
_Posted on **{{ page.date | date_to_string }}**_

This is the fifth article of the [Getting started with Docker](getting-started-with-docker) series. In this article, I am going to show how to install a PostgreSQL cluster on three Docker containers.

The cluster will be configured in master/slave mode with one master and two slaves. PostgreSQL supports two cluster type: **hot** and **warm standby**. The former allows the slave to receive connections in read-only, the latter doesn’t allow the slaves to receive connections. In this tutorial, we will configure the cluster as hot standby.

## Modify the start\_containers.sh script

The first step to create a PostgreSQL cluster is to modify the [start\_containers.sh](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster/start_containers.sh) script to create two environment variables that we pass to the _docker create_ command.

{% highlight shell %}
...
MASTER_NAME=${NODE1_NAME}
...
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE1_PRIVATE_IP} --hostname ${NODE1_NAME} --name ${NODE1_NAME} --env NODE_NAME=${NODE1_NAME} --env MASTER_NAME=${MASTER_NAME} -p ${NODE1_PORT}:5432 postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE2_PRIVATE_IP} --hostname ${NODE2_NAME} --name ${NODE2_NAME} --env NODE_NAME=${NODE2_NAME} --env MASTER_NAME=${MASTER_NAME} -p ${NODE2_PORT}:5432 postgresql /bin/bash
docker create -it --net ${PRIVATE_NETWORK_NAME} --ip ${NODE3_PRIVATE_IP} --hostname ${NODE3_NAME} --name ${NODE3_NAME} --env NODE_NAME=${NODE3_NAME} --env MASTER_NAME=${MASTER_NAME} -p ${NODE3_PORT}:5432 postgresql /bin/bash
...
{% endhighlight %}

These variables will be used by the startup scripts to start the master and the two slaves.

## Modify the startup scripts

The two environment variables defined in the previous section will be used by the startup scripts to understand if the container contains the master of one of the two slaves.

Here the code of the _src/postgresql/entrypoint.sh_ script. We added a sleep command for slave nodes.

{% highlight shell %}
#!/bin/bash
...
while [ -f /var/run/recovery.lock ]; do
    sleep 1;
done;
...
{% endhighlight %}

Here the code of the _src/postgresql/bin/entrypoint.sh_ script.

{% highlight shell %}
#!/bin/bash
DATA_DIRECTORY="/home/postgres/data/postgres"
LOGS_DIRECTORY="/home/postgres/data/logs"

echo ">>> TEST IF DATA DIRECTORY IS EMPTY"
if [ -z "$(ls -A $DATA_DIRECTORY)" ]; then
    echo ">>> PREPARE NODE $NODE_NAME FOR FIRST STARTUP"
    if [ "$NODE_NAME" = "$MASTER_NAME" ]
    then
        echo ">>> CREATE DATA DIRECTORY ON THE MASTER NODE"
        /usr/lib/postgresql/9.5/bin/initdb -D $DATA_DIRECTORY
        echo ">>> COPY CONFIGURATION FILES"
        cp /usr/local/bin/cluster/postgresql/config/postgresql.conf $DATA_DIRECTORY
        cp /usr/local/bin/cluster/postgresql/config/pg_hba.conf $DATA_DIRECTORY
    else
        echo ">>> $NODE_NAME IS WAITING MASTER IS UP AND RUNNING"
        while ! nc -z $MASTER_NAME 5432; do sleep 1; done;
        sleep 10
        echo ">>> REPLICATE DATA DIRECTORY ON THE SLAVE $NODE_NAME"
        /usr/lib/postgresql/9.5/bin/pg_basebackup -h 10.0.2.31 -p 5432 -U postgres -D $DATA_DIRECTORY -X stream -P
        echo ">>> COPY recovery.conf ON SLAVE $NODE_NAME"
        cp /usr/local/bin/cluster/postgresql/config/recovery.conf $DATA_DIRECTORY
        sed -i "s/NODE_NAME/$NODE_NAME/g" $DATA_DIRECTORY/recovery.conf
        sed -i "s/MASTER_NAME/$MASTER_NAME/g" $DATA_DIRECTORY/recovery.conf
    fi
fi
echo ">>> START POSTGRESQL ON NODE $NODE_NAME"
/usr/lib/postgresql/9.5/bin/postgres -D $DATA_DIRECTORY > $LOGS_DIRECTORY/postgres.log 2>&1
{% endhighlight %}

The code checks whether the data directory is empty or not. In the latter case, the code assumes the data directory already exists and then we only startup PostgreSQL. In the former case, the code is different for the master and slaves.

For the master, the code is similar to the previous article. The data directory is initialized and the configuration files postgresql.conf and pg\_hba.conf are copied in it.

For the slaves, the code will wait for the master is up and running and then they replicate the data directory from it with the _pg\_basebackup_ command. Finally, we copy the recovery.conf file and let it refers to the master node.

## Configure the PostgreSQL cluster

To configure the PostgreSQL cluster as hot standby we need to uncomment the following lines in the [_postgresql.conf_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster/src/postgresql/config/postgresql.conf) file.

{% highlight properties %}
hba_file = '/home/postgres/data/postgres/pg_hba.conf'
wal_level = hot_standby
listen_addresses = '*'
max_wal_senders = 5
hot_standby = on
{% endhighlight %}

In the [_pg\_hba.conf_](https://github.com/sasadangelo/docker-tutorials/blob/master/postgresql-cluster/src/postgresql/config/pg_hba.conf) we will specify the host from which the replication is allowed.

{% highlight plaintext %}
host     replication     postgres        node1                   trust
host     replication     postgres        node2                   trust
host     replication     postgres        node3                   trust
{% endhighlight %}

## How to verify if the cluster is working?

An easy way to verify if the cluster is working is to create a database on the master node and verify its replication on slaves. Run the following commands on the master node.

{% highlight sql %}
psql -h localhost -p 5432 -U postgres
CREATE DATABASE mydb;
\list
\quit
{% endhighlight %}

Verify on slave nodes if the database has been replicated using the following commands. To verify the database is replicated on node3 use the same commands and replace 5433 port with 5434.

{% highlight shell %}
psql -h localhost -p 5433 -U postgres 
\list
\q
{% endhighlight %}

## What’s next?

In this article, we learned how to use the three containers created in the [previous article](http://code4projects.altervista.org/how-docker-networking-works/) to install a PostgreSQL cluster. You can download the source code [here](https://github.com/sasadangelo/docker-tutorials/tree/master/postgresql-cluster) in the _postgresql-cluster_ folder. In the [next article](http://code4projects.altervista.org/how-docker-volumes-works/), we will discuss another important Docker concept: **volumes**.