---
layout: post
title: Relational Database Service (RDS) - What Is It and How Does It Work?
post_series_id: getting-started-with-amazon-web-services
slug: relational-database-service
thumbnail: assets/img/Amazon-RDS.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories: Cloud
---

![Relational Database Service (RDS): What Is It and How Does It Work?](assets/img/Amazon-RDS.png){:width="200" height="200" }

# Relational Database Service (RDS): What Is It and How Does It Work?
_Posted on **{{ page.date | date_to_string }}**_

In this article, I am going to discuss Amazon Relational Database Service, a managed service to quickly deploy a database for your application. You will learn what is available in the AWS platform and how you can reduce your application time to market.

Amazon Relational Database Service (RDS) is a managed database service that allows, with a single click, to create a database, configure it (also in HA), and manage backups automatically. If you have experience in building applications you know that you can keep data in several places (file, remote storage, etc.) included a database. However, managing the database infrastructure is not easy. You need to manage the following items:

1.  server hardware (cable, power, network, disks, etc.);
2.  operating system (install, upgrade, and patches);
3.  database engine software (install, upgrade, and patches);
4.  create and manage the database containing data (create, data optimization, etc.);
5.  create and manage backups for disaster recovery;
6.  manage security;
7.  if you need high availability you need to replicate the above effort for a number of replicas you need to manage.

You can install your own database service on an EC2 instance, however, you save only items 1 and partially 2, but you still need to manage items 3-7.

## Amazon RDS Configuration

The basic idea of the Amazon RDS is to let the customer choose the database to create its engine (i.e. PostgreSQL, MySQL, MariaDB, etc), configure it for disaster recovery, and high availability with a few mouse clicks. The application can live inside Amazon Cloud or outside it, it depends on the customer’s choice. The goal here is that customers focus on their own applications letting Amazon manage the whole database infrastructure.

![Amazon Relational Database Service](assets/img/Screenshot-2021-01-21-at-09.46.47.png){:width="450" height="193" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

RDS service will provide the following benefits:

-   automatic provisioning and OS patching;
-   continuos backup and restore to specific timestamp (Point in Time Restore);
-   monitoring dashboard;
-   read replica configuration for horizontal scalability;
-   multi AZs setup for high availability;
-   quick restore from backup for disaster recovery;
-   horizontal and vertical scaling;
-   Storage on EBS.

The only limit is that you cannot SSH on the EC2 instance where the service is deployed.

In order to create a database in Amazon RDS, you need to create a database instance. Basically, you need to define the **DB Instance Class** where you choose the number of CPUs, the memory, and the network performance of the EC2 machine hosting the instance. Then, you need to define the DB Instance Storage, for example, the disk type (SSD gp1 or io1). Amazon RDS supports six Db engines: MySQL, Amazon Aurora, SQL Server, PostgreSQL, MariaDB, and Oracle. Depending on how you configure the DB Instance class and storage and the DB Engine the price change.

![Amazon Relational Database Service Instance](assets/img/Amazon-RDS-Instance.png){:width="450" height="224" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

## Amazon RDS typical scenario

In a typical scenario, you should deploy your application and the database service on the same VPC, in a single AZ, on different subnets. Traffic from the Internet only reaches the application subnet that must be public, while the database subnet is private. Usually, you have to configure the private subnet to only accept connections from the public subnet.

![Amazon Relational Database Service in a VPC](assets/img/Amazon-RDS-VPC.png){:width="450" height="256" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

## Amazon RDS in High Availability (HA) scenario

### Amazon RDS Multi-AZ configuration

You can configure Amazon RDS to work in HA, in this case, you will have a DB Replica on a different AZ connected in Synchronous mode to the master database. In this way, you will not have any data loss because a transaction is closed only if it is present on both the DB Instance.

![Amazon RDS HA](assets/img/Amazon-RDS-HA.png){:width="450" height="288" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

If for some reason the Amazon RDS master copy is unavailable, the application automatically connects to the Synchronous instance.

![Amazon RDS Failover](assets/img/Amazon-RDS-Failover.png){:width="450" height="286" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Amazon RDS from Single-AZ to Multi-AZ

It is possible to move the RDS Database instance from a Single-AZ to a Multi-AZ configuration with few clicks of the mouse. Here is what happens behind the scene:

1.  the RDS service creates a snapshot of the Master database.
2.  the snapshot is restored in another AZ of the same Region.
3.  the Master starts to replicate itself on the Replica node.

![Move RDS Cross AZ](assets/img/Move-RDS-Cross-AZ.png){:width="450" height="462" }

## Relational Database Service in Scalability scenario

Amazon RDS supports also Read Replica for MySQL, PostgreSQL, MariaDB, Amazon Aurora DB engines. Basically, the service automatically uses the standby copy for read-only queries. This allows splitting the read database traffic on both nodes. Updates are available only on the master node. This configuration is particularly useful on massive database read applications. However, the stand-by node works in an asynchronous mode so if you want to promote it to master a manual action is required.

You can configure up to 5 Read Replicas, within the same AZ, cross AZ, or cross Region.

![Amazon RDS Read Replica](assets/img/Amazon-RDS-Read-Replica.png){:width="450" height="409" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

Usually, there is a network cost when your data goes from one AZ to another. However, for managed services like RDS if the traffic is inside the same region no extra fees are applied.

A typical application of the Read Replica scenario is when you have an application working with a database and you want to add an analysis service that only needs to read data from it. In this scenario, you create a replica node and your analysis service only reads data from it.

## Amazon RDS Backup and Snapshot

When you create a Database instance it enables automatically the backup feature. Every day an automatic full backup runs and every 5 minutes it saves transaction logs. Full backup and transaction logs allow you to restore the backup at any point in time with the granularity of 5 minutes. By default, the retention policy is 7 days but you can increment up to 35 days.

In RDS there is also the concept of a Database snapshot. The main difference with backup is that users can trigger it manually and retention policy can be as long as you want.

## Relational Database Service Storage Autoscaling

This feature helps you to increase the storage of your RDS instance dynamically. When RDS detects you are running out of free space, it scales the size automatically. In order to have this feature working you need to set a Maximum Storage Threshold (max limit for DB storage) then RDS scales automatically when:

1.  free space < 10% of the allocated storage;
2.  low storage lasts at least 5 minutes;
3.  6 hours passed since the last modification;

This feature is supported on MariaDB, MySQL, PostgreSQL, SQL Server, and Oracle.

## Relational Database Service Security

### Database encryption

You can secure your data into the database mainly using two types of encryption:

-   **at rest encryption**;
-   **in-flight encryption**;

With the at-rest encryption, you encrypt data into your database and its replica. You can do that at launch time with few mouse clicks using AWS KMS AES 256 encryption. You can encrypt Replicas only if the Master is encrypted too. Transparent Data Encryption (TDE) is only available for Oracle and SQL Server database engines.

Moreover, you can encrypt data that your application sends to the database service using SSL certificates. When the application connects to the database its should provide options to configure SSL certificates and this varies from a database engine to another.

### How to encrypt an unencrypted database?

Before I said that you can encrypt a database only at launch time. However, what I can do to encrypt an already existing unencrypted database? Suppose your requirements change and you need to encrypt your database. Amazon RDS service doesn’t provide a direct way to do this, however, you can achieve the same result using a very simple procedure.

First of all, you need to remember some critical rules:

-   snapshots of an unencrypted database are unencrypted;
-   snapshots of an encrypted database are encrypted;
-   you can convert an unencrypted snapshot into an encrypted one;

With these elements in mind, it’s easy to figure out the procedure to encrypt an already existing not encrypted database. Here is the procedure:

-   stop your existing database instance;
-   create a snapshot of your unencrypted master database;
-   convert the snapshot into an encrypted one;
-   restore the snapshot into a new database instance;
-   start your new database instance;
-   eventually start replica nodes;
-   move the application to the new database instance.

![RDS Encrypt Database](assets/img/RDS-Encrypt-Database.png){:width="450" height="462" }

### Network Security

At the beginning of this article, I showed a typical scenario of an application that uses a database instance. Usually, while the application lives in a public subnet because it must be accessible from the outside, the database usually lives in a private subnet in the same VPC in order to protect data from unauthorized access.

The second level of protection of your database instance is through the use of **Security Groups**. You can use Security Group with RDS instance in the same way you use them with EC2 instance. For example, you can specify the IP or Security Group that can access your database instance.

![Amazon RDS in a VPC](assets/img/Amazon-RDS-VPC.png){:width="450" height="256" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Access Management

Another level of security is to control who can access the RDS instance. In the AWS platform, you can implement this through the IAM policies and RDS APIs. Another alternative is to use a traditional username and password.

Database engines like MySQL and PostgreSQL support IAM-based authentication. You can do this simply using a Role and a token retrieved from RDS API calls. This token will have a lifetime of 15 seconds. The benefits of this approach are to leverage IAM and Roles for user management.

![RDS IAM Authentication](assets/img/RDS-IAM-Authentication.png){:width="450" height="513" }

## Amazon Aurora

The list of DB engines mentioned above contains open-source (i.e. MySQL, MariaDB, and PostgreSQL) and commercial databases (i.e. Oracle and SQL Server), the only exception is Aurora an Amazon proprietary database engine that works like a PostgreSQL or MySQL database.

It is a Cloud-optimized database engine and claims a 5x performance improvement over MySQL on RDS and over 3x the performance of PostgreSQL on RDS. The database size grows from 10 GB up to 64 TB with an increment of 10 GB.

This database engine is HA native and automatic failover is instantaneous, it supports up to 15 replicas with a lag of less than 10 ms. In the figure below you can see that each data (i.e. block blue) is replicated 6 times across 3 AZs. Self-healing is achieved with peer-to-peer replication.

![Amazon Aurora Architecture](assets/img/Amazon-Aurora-Architecture.png){:width="450" height="341" }

As a Database Cluster Amazon Aurora has only one master that writes the data and multiple replicas that read them. In order to establish connections with these databases, there are two endpoints: one for the master and another one to load balance all the replicas. You can imagine these Writer/Reader endpoints like DNS names to use to write/read data into/from the databases. Adding and removing replicas is as easy as click a button.

![Amazon Aurora DB Cluster](assets/img/Amazon-Aurora-DB-Cluster.png){:width="450" height="224" }

Moreover, there are other features like backup and restore, isolation and security, industry compliance, automatic patching with zero downtime, advanced monitoring, backtrack (restore data at any point in time without using backups).

All of these features come at a cost as Amazon Aurora costs, on average, 20% more than Amazon RDS.

## Conclusion

In this article, I explained how to use Amazon RDS to easily deploy a database for your application.  I discussed several typical deployments you could find useful for your scenarios. In the next article, I will show you a step-by-step tutorial to use this service in practice.