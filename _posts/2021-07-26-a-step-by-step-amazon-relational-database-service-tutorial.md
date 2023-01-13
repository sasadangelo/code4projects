---
layout: post
title: A Step by step Amazon Relational Database Service tutorial
post_series_id: getting-started-with-amazon-web-services
slug: a-step-by-step-amazon-relational-database-service-tutorial
thumbnail: wp-content/uploads/rds-logo.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories: Cloud
---

![A Step by step Amazon Relational Database Service tutorial]({{ site.baseurl }}/wp-content/uploads/rds-logo.png){:width="393" height="200" .responsive_img}

# A Step by step Amazon Relational Database Service tutorial
_Posted on **{{ page.date | date_to_string }}**_

This is a step-by-step Relational Database Service tutorial to show you how you can easily create a database with the Amazon platform. In the [previous article]({{ site.baseurl }}/relational-database-service/), I showed you the theory behind the Relational Database Service (RDS), here I will show you how to put those concepts into practice.

## How to Create a MySQL database

### Create the MySQL database

From the Management Console search bar, type the word “RDS” and select the **Managed Relational Database Service**. Click the orange button **Create database**.

![Relational Database Service tutorial]({{ site.baseurl }}/wp-content/uploads/1-RDS-Create-database.png){:width="450" height="260" .responsive_img}

The RDS service provides two ways to create a database, an easy way with very few options and a standard way where you can configure every detail. Select the **Standard Create** radio button.

![RDS Create Database Standard]({{ site.baseurl }}/wp-content/uploads/2-RDS-Create-Database-Standard.png){:width="450" height="170" .responsive_img}

In the **Engine Options,** select the MySQL database engine. MySQL is eligible for free-tier so this tutorial will cost you no money.

![Create MySQL Database]({{ site.baseurl }}/wp-content/uploads/3-Create-MySQL-Database.png){:width="450" height="226" .responsive_img}

Choose the latest MySQL version.

![RDS Select MySQL Version]({{ site.baseurl }}/wp-content/uploads/4-RDS-Select-MySQL-Version.png){:width="450" height="209" .responsive_img}

Now you can choose to deploy a production-ready, a dev/test database, or one eligible for free-tier. Since this is just a demonstration I suggest you select the **Free-Tier** radio button.

![RDS Select Free Tier]({{ site.baseurl }}/wp-content/uploads/5-RDS-Select-Free-Tier.png){:width="450" height="144" .responsive_img}

You can insert the name and the credentials of your database.

### Configure the database credentials

![RDS Insert D Name and Credentials]({{ site.baseurl }}/wp-content/uploads/6-RDS-Insert-DBName-andCredentials.png){:width="450" height="365" .responsive_img}

Now you can select the DB Instance class. Basically, this is the EC2 instance type on top of which the database is deployed. Since we are using the Free-Tier the only EC2 instance we can use is the t2.micro that here is called **db.t2.micro**.

![RDS Select DB Instance Class]({{ site.baseurl }}/wp-content/uploads/7-RDS-Select-DBInstance-Class.png){:width="450" height="228" .responsive_img}

### Configure the database hardware

Amazon RDS allows you to select the storage that will store your database. For our demo, a generic **General Purpose SSD** disk of 5 Gb is enough.

![RDS Choose Storage]({{ site.baseurl }}/wp-content/uploads/8-RDS-Choose-Storage.png){:width="450" height="231" .responsive_img}

The RDS service allows you to create a Multi-AZ configuration, however, in the Free-Tier this option is disabled. For our purpose, a Single-AZ deployment is fine.

![RDS Configure Multi AZ]({{ site.baseurl }}/wp-content/uploads/9-RDS-Configure-Multi-AZ.png){:width="450" height="135" .responsive_img}

You can configure the **Connectivity** for your database. For example, you can choose the VPC and Subnet where to deploy the database. moreover, you can decide if the Subnet should be public or private. In a [typical scenario](relational-database-service) the EC2 instance application will live in a public subnet while the database will live in the same VPC but a private Subnet.

![RDS Configure Connectivity]({{ site.baseurl }}/wp-content/uploads/10-RDS-Configure-Connectivity.png){:width="450" height="304" .responsive_img}

### Configure the database security and authentication

You can declare **Security Group** to allow only traffic coming from a given IP or another Security Group to access the database. This option is particularly useful in the [typical scenario](relational-database-service) to allow only the application EC2 instance to access the database. This is another security best practice to avoid hacking your database instance.

![RDS Configure Security Group]({{ site.baseurl }}/wp-content/uploads/11-RDS-Configure-Security-Group.png){:width="450" height="226" .responsive_img}

In the previous article, I mentioned two authentication methods on RDS: password and IAM;  There is a third method called **Password and Kerberos authentication**, however, to make things simple just select the **Password authentication** radio button. Click the **Create Database** button.

![RDS Choose Authentication Method]({{ site.baseurl }}/wp-content/uploads/12-RDS-Choose-Authentication-Method.png){:width="450" height="181" .responsive_img}

### Explore your new MySQL Database

In the Databases dashboard, you can see the new database. You can click on it to see details about it.

![RDS View Databases]({{ site.baseurl }}/wp-content/uploads/13-RDS-View-Databases.png){:width="450" height="120" .responsive_img}

You can see the Summary with information about the database name, the status, the hardware, the engine, region, and so on.

![RDS Database Summary]({{ site.baseurl }}/wp-content/uploads/14-RDS-Database-Summary.png){:width="450" height="134" .responsive_img}

There is information about Connectivity & Security and much more.

![RDS Connectivity and Security]({{ site.baseurl }}/wp-content/uploads/15-RDS-Connectivity-and-Security.png){:width="450" height="205" .responsive_img}

## Conclusion

In this article, I showed a step-by-step Relational Database Service tutorial to easily create your next MySQL database on the Amazon platform. The [previous article]({{ site.baseurl }}/relational-database-service/) and this tutorial complete our discussion about the Amazon RDS service. For more details, you can check out the [official documentation](https://docs.aws.amazon.com/it_it/AmazonRDS/latest/UserGuide/Welcome.html).
