---
layout: post
title: Amazon Web Services (AWS) Introduction
post_series_id: getting-started-with-amazon-web-services
slug: amazon-web-services
thumbnail: assets/img/Amazon-Web-Services.png
excerpt: This article is an introduction to the Amazon Web Services (AWS) platform. Read it to have a platform and its core services overview.
categories: Cloud
sitemap:
  lastmod: 2021-01-14
  priority: 0.7
  changefreq: 'weekly'
---

![Amazon Web Services (AWS) Introduction](assets/img/Amazon-Web-Services.png){:width="200" height="200" .responsive_img}

# Amazon Web Services (AWS) Introduction
_Posted on **{{ page.date | date_to_string }}**_

This article is an introduction to the Amazon Web Services (AWS) platform.

## What is the Amazon Web Services platform?

AWS is the Cloud platform developed by Amazon and [available at the following address](https://aws.amazon.com/). The platform was born in 2006 in Virginia (USA),  it satisfies the [Cloud definition and its five essentials characteristics](getting-started-with-cloud-computing), and it implements all the five service models of Cloud Computing (IaaS, CaaS, PaaS, FaaS, and SaaS).

## A Bit of History

There are a lot of [myths about of AWS was born](https://www.networkworld.com/article/2891297/the-myth-about-how-amazon-s-web-service-started-just-won-t-die.html), however, if you want to read the full story you can read [this blog post on Tech Crunch](https://techcrunch.com/2016/07/02/andy-jassys-brief-history-of-the-genesis-of-aws/). Basically, the platform was launched internally in 2002. In 2003 the Amazon Infrastructure was one of the company’s core strengths and from here the idea to sell it to other companies to drive their businesses. One year later, in 2004, the company launched publicly the AWS SQS service. Two years after, in 2006, the platform was officially launched with SQS, Ec2, and S3 services. In 2007 the platform was launched in Europe too. A lot of companies like Dropbox, Netflix, Airbnb, and NASA started to create their SaaS business on the AWS platform. The rest is history.

![AWS History](assets/img/AWS-History.png){:width="450" height="176" .responsive_img}

## AWS Global Infrastructure

Today Amazon has a Global Infrastructure of 24 **Regions** and other 5 Regions that will be available soon. Each Region has a name like **us-east-1**, **eu-west-3**, etc. In these regions, there are 77 **Availability Zones** (AZ) and 216 **Points of Presence** (205 **Edge Locations** and 11 **Regional Caches**). Edge locations are part of the AWS Content Delivery Network (CDN) necessary to bring content (eg video, music, etc.) close to the end-users. For more details, [see this page](https://aws.amazon.com/it/about-aws/global-infrastructure/).

![Amazon Web Services Global Infrastructure](assets/img/aws-global-infrastructure.png){:width="450" height="244" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

In AWS a Region **has two or more Availability Zones (AZ)** (usually 3, min 2, max 6) that allow replicating services in such a way that they can be up and running even if a data center is down. AZs have high-speed and low latency network connections. In each AZ we can **have one or more datacenter**. All traffic between AZ’s is encrypted.

![Amazon Web Services Region](assets/img/AWS-Region.png){:width="450" height="356" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

The following services have Global scope:

-   Identity and Access Management (IAM).
-   Route 53.
-   Web Application Firewall (WAF).
-   CloudFront.

All the other services have Regional scope and they are not available in all the Regions. We will analyze these services in the next sections and articles.

When you need to choose a Region for a regional scope service you need to take into consideration 4 elements:

-   **Compliance**. Data governance and legal requirements data never leave a region without your explicit permission.
-   **Proximity**. In order to reduce latency.
-   **Available services**. Services are not available in all the regions, if you need a regional scope service [make sure it is available in the Region you choose](https://aws.amazon.com/it/about-aws/global-infrastructure/regional-product-services/).
-   **Pricing**. Prices for a service can be different in different regions.

## The Amazon Web Services Interface

You can access AWS via three interface types:

-   **AWS Management Console**. An easy-to-use graphical interface protected by password and MFA that supports the majority of services. This is the preferred method to administer your AWS account and it is available on mobile phones as well. You can access the console using the following [web address](https://aws.amazon.com/), create an account, and choose the region where you want to create your resources. To use the platform Amazon force you to insert your credit card in order to validate your identity. No cost will be charged unless you create resources. Consider that AWS allows you a period of free trial for a lot of resources (i.e. EC2, S3, etc.).
-   **AWS Command Line Interface.** It is an open-source tool for interacting with AWS services via discrete command. It runs on operating systems like macOS, Linux, and Windows. This is an alternative access method to the AWS Management console. It is programming language agnostic and particularly useful when you want to create automation via scripts. The access to the resources is protected by **access key id** (like user name but less mnemonic) and **secret access key** (like a password).
-   **AWS Software Developer Kit (SDK)**. It incorporates the connectivity and functionality of the wide range of AWS Cloud services into your code. You can embed into your code administrative tasks to manage AWS resources. Lots of programming languages are supported like Java, C++, Go, Node.js, Ruby, PHP,  .NET, Python, and Javascript. The access to the resources is protected by **access key id** (like user name but less mnemonic) and **secret access key** (like a password).

![AWS Management Console](assets/img/AWS-Management-Console.png){:width="450" height="224" .responsive_img}

In AWS, services are divided into two big categories:

-   **Core Services**;
-   **Integrated Services**.

### AWS Core Services

**Core Services** includes:

-   **Elastic Compute Cloud** (**EC2**), you can create remote virtual or bare metal computers with a given number of CPUs, RAM, and Operating Systems.
-   **Elastic Block Storage** (**EBS**), you can attach to your EC2 system one or more filesystems on a mount point. AWS supports several file system types to format your partition.
-   **Simple Storage Service** (**S3**), is the Object Storage of the AWS platform. Unlike block storage where files are divided into blocks, Object Storage is a container of objects (usually files) where each is identified by an ID accessible worldwide through a URI, a series of metadata (e.g. permissions), and the data of the object itself.
-   **Virtual Private Cloud** (**VPC**), enterprises can create in their account **one or more VPC** so that their environment and resources are isolated by one of the other customers. Each VPC can have one or more subnet where customers can deploy their resources (EC2, EBS, S3, and so on).

### AWS Integrated Services

**Integrated Services** are additional services very useful for application scale up and down, to easily manage databases in High Availability (HA), for monitoring, for DevOps activities, integration, and much more. They include the following services:

-   **Load Balancers**, when you scale up and down EC2 instances you need a single IP address as an endpoint and a way to split the traffic on both instances. Load Balancers are the AWS components that allow this task. AWS supports three types of Load Balancers: Classic, Network, and Advanced.
-   **Autoscaling** is the component that allows to scale EC2 instances up and down based on the workload.
-   **Route S3**, is the Amazon DNS service.
-   **Relational Database Service** (**RDS**), is the Amazon relation database service. It supports several engines like MySQL, MariaDB, PostgreSQL, and others. It allows the customer to create a database with a mouse click, you can configure it in high availability with automatic backup.
-   **Lambda** is the Amazon **FaaS** solution.
-   **Beanstalk** is the Amazon **PaaS** solution.
-   **Simple Notification Service** (**SNS**), allows the applications to integrate each other with a notification message system.
-   **CloudWatch** is the Amazon monitoring system.
-   **Cloudfront** is the main component of the Amazon Content Delivery Network (CDN). In the Global Infrastructure, AWS has edge locations where content is replicated in order to be as close as possible to the end-users to reduce latency. Cloudfront allows content replication on these locations.
-   **CloudFormation** is the pipeline system you can use to manage the application lifecycle like deploy, remove, and update. It is the basic component to manage DevOps activities on the system.

## AWS Core Services

In this section, we will start to go more in-depth in the overview of the AWS Core Services. An overview of AWS Integrated Services will be part of the [next article](amazon-integrated-services-2).

### AWS Elastic Cloud Compute (EC2)

The word **Compute** in the AWS EC2 name refers to a virtual or physical computer that can be used as a server for multiple purposes: application server, web server, mail server, etc. **Cloud** means that this computer is available in the Cloud, so it is accessible via the Internet with an IP address. Finally, the word **Elastic** means that this computer can be replicated on multiple instances to scale the server horizontally up and down depending on the workload. For more details [read the following article](amazon-ec2-for-beginners).

![Amazon EC2](assets/img/Amazon-EC2.png){:width="450" height="188" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### AWS Elastic Block Storage (EBS)

The AWS EBS service allows you to create network-attached volumes for your Ec2 instance. By default, the Ec2 instance has its own root filesystem but you can mount more volumes depending on your needs. The service allows you to choose the **Block Storage type** between **Hard Disk Drive** (**HDD**) or **State-Solid Drive** (**SSD**). For more details [read the following article](amazon-ec2-for-beginners).

![HDD and SDD](assets/img/HDD-SDD.png){:width="450" height="253" .responsive_img}

### AWS Simple Storage Service (S3)

AWS S3 is the Amazon Object Storage service. This service is useful in scenarios where you write objects once and read them any time, from anywhere. An object has three elements:

1.  **key**, to identify the object into the storage;
2.  **data**, the data itself;
3.  **metadata**, set of permissions, and other useful information associated with the data.

You can use Object Storage in a lot of use cases like static web hosts, store application assets, and backup for disaster recovery.

You can upload your objects using the three interfaces available in Amazon AWS: management console, CLI, and SDK. Once the file is available you can download it using the same three interfaces or via HTTP/HTTPS using a **URI**.

In order to use the AWS S3 service with your account, you need to create one or more **buckets** where you will store the objects. A **bucket** is simply a logical separation of your objects.  In order to store an object in the bucket, you need to associate a **key**.

For example, I can define the bucket **my-bucket-name** and store a file in it with key **media/welcome.mp4** (that is the folder and filename).

![AWS S3 Bucket](assets/img/AWS-S3-Bucket.png){:width="450" height="215" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

The service itself takes care of replicate this information on other AZ to create redundancy and implement high availability.

![AWS S3 bucket replication](assets/img/AWS-S3-bucket-replication.png){:width="450" height="237" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

AWS supports scalability for the system allowing to access this object from a large number of users using a URI that contains the bucket name, the object storage service domain, and the object key.

![AWS S3 URI](assets/img/AWS-S3-URI.jpeg){:width="450" height="106" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Virtual Private Cloud (VPC)

Amazon VPC allows you to create a virtual private network in AWS Cloud and associate it with your account. **You can configure one or more VPC within your account**. VPC allows you to use many of the same concepts and constructs available in the on-premises network, but it removes much of the complexity of setting up a network without sacrificing control, security, and usability.

A VPC can have one or more subnets where you can deploy services (eg. EC2, RDS, etc.) and resources deciding which one to isolate and which one to expose. A single subnet is available in a single AZ, but more subnets of the same VPC can belong to the same or different AZ.

You can deploy EC2 instances in a VPC with an IP address associated with them. They have the ability to access the Internet via an Internet Gateway (IGW). VPS uses routing tables to drive traffic among the subnets.

The following figure shows a VPC example.

![AWS VPC](assets/img/AWS-VPC.png){:width="450" height="345" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

In the us-west-2 (Oregon) region we define the Test-VPC network which provides an address space between 10.0.0.0 to 10.255.255.255. In AZ A, we define two subnets:

1.  **Public Subnet A1**, with an IP range between 10.0.0.0 to 10.0.0.255;
2.  **Private Subnet B1**, with an IP range between 10.0.1.0 to 10.0.1.255.

Resources in Public Subnet A1 are accessible via the Internet through the Test-IGW Internet Gateway. As said above in your account you can define multiple VPC and subnets in a VPC that can be on different Availability Zone too.

## Conclusion

The goal of this article is just to provide an overview of the AWS platform with a brief description of its Core Services. [In the next article](beginners-guide-identity-access-management), I will explain the basics of the **Identity and Access Management** component, and a hands-on lab to create your first account and do the initial setup using some best practices.