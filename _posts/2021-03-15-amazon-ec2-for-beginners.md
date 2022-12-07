---
layout: post
title: Amazon Elastic Cloud Computing (EC2) for Beginners
post_series_id: getting-started-with-amazon-web-services
slug: amazon-ec2-for-beginners/
thumbnail: assets/img/Amazon-EC2-1.png
excerpt: The following article is an introduction to the Amazon Elastic Cloud Computing (EC2) service for beginners.
categories: Cloud
---

![Amazon Elastic Cloud Computing (EC2) for Beginners](assets/img/Amazon-EC2-1.png){:width="200" height="200" .responsive_img}

# Amazon Elastic Cloud Computing (EC2) for Beginners
_Posted on **{{ page.date | date_to_string }}**_

In the [previous article](beginners-guide-identity-access-management), we created and set up our AWS account. We are ready to introduce the most important IaaS AWS resource: the **Amazon EC2 instance**. This service allows you to create a Virtual Machine (VM) choosing among a broad range of instance types.

## AWS Elastic Cloud Compute (EC2)

The word **Compute** in the AWS EC2 name refers to a virtual or physical computer that can be used as a server for multiple purposes: application server, web server, mail server, etc. The word **Cloud** refers to that this computer is available in the Cloud. This means that this computer is accessible via the Internet with an IP address. The word **Elastic** means that this computer can be replicated on multiple instances to scale the server horizontally in and out depending on the workload.

![Amazon EC2](assets/img/Amazon-EC2.png){:width="450" height="188" .responsive_img} 

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Amazon EC2 Instance Types

You can choose different classes of EC2 instances that are optimized for different use cases like:

-   General-purpose
-   Compute Optimized
-   Memory-Optimized
-   Accelerated Computing
-   Storage Optimized

You can choose your EC2 instance by **selecting a broad range of hardware and software**. Each instance type has a name like this:

-   **t2.micro**

where:

-   **t** (**tiny**) is the **instance class**. We can have general-purpose classes as **t** and **m** (**medium**), compute-optimized (**c**), and so on (see the figure below).
-   **2** is the **generation**. Amazon improves its instances over time.
-   **micro** is the **capacity** of the machine.

![Amazon EC2 Instance Types](assets/img/Amazon-EC2-Instance-Types.png){:width="450" height="136" .responsive_img}

When you select an instance you can choose:

-   **Operating Systems** (i.e. Linux, Windows, Mac);
-   **CPU**. in terms of CPU power and cores;
-   **RAM**. a quantity of memory RAM available;
-   **Storage**. the storage connected to the EC2 instance;
    -   by default, an EC2 instance has a network-attached disk (EBS service) for its root filesystem;
    -   it is possible to attach more than one network-attached disks;
    -   you can attach a Network File System (EFS service) to share data across multiple EC2 instances;
    -   attach a physical disk (Ec2 Instance Store).
-   **Region**. you can select the region where to deploy your EC2 instance.
-   **Network Card**. Network speed and Public IP address.
-   **Security Group**. It’s the mechanism Amazon uses to define a firewall to protect your EC2 instance. By default, only 22 port is open for SSH.

At the end of the configuration, you will have a remote computer up and running in minutes you can access via SSH for configuration. You need a key pair to access your remote instance that you can generate during the configuration.

The following figure shows some examples of Ec2 Instances. For more details, see [here](https://aws.amazon.com/it/ec2/instance-types/).

![Amazon EC2 Instances Examples](assets/img/Amazon-Ec2-Instances-Examples.png){:width="450" height="153" .responsive_img}

### Amazon EC2 Optimized Instances

In addition to the general-purpose EC2 instances (class **t** and **m**). Amazon provides some optimized instances that are particularly useful in some scenarios. Here some examples:

-   **Compute Optimized** (class **c**). They are great for compute-intensive tasks that require high-performance processors:
    -   Batch processing workload;
    -   Media transcoding;
    -   High-performance web servers;
    -   High-performance computing (HPC);
    -   Scientific modeling and machine learning;
    -   Dedicated gaming servers.
-   **Memory-Optimized** (class **r**, **x**). These are useful for workloads that process large data sets in memory:
    -   floating-point number calculation;
    -   graphic processing;
    -   data pattern matching;
-   **Storage Optimized** (class **I**). Great for storage-intensive tasks that require high, sequential read and write access to large data sets on local storage:
    -   Relational and NoSQL databases;
    -   Cache for In-Memory databases (Redis);
    -   Data Warehouse;
    -   Distributed File System.

## Amazon EC2 Pricing

Amazon EC2 instances use a **Pays as You Go** pricing model, so you will pay only for the number of hours you effectively use your instance, its capacity, and the number of instances. **Free-Tier** is available for t2.micro instance type for 720 hours a month for 1 year.

[Amazon Ec2](amazon-web-services) instance is available in four pricing options.

### On-Demand instances

You incur charges only when it is running paying only for the hours and seconds usage. Pricing depends on the region, OS, instance type, capacity (number of cores and RAM size), and instance size. Linux instances are billing by seconds after the first minute. Other instances (Windows and Mac) are billing per hour. It has the highest cost but no upfront payment.

### Reserved instances

You reserve the instances for a period of time from 1 to 3 years. The longer you reserve the greater is the discount. Moreover, the larger the payment up-front you make, the greater the discount will be.  You can pay all (AURI), partial (PURI), or no charge (NURI) up-front. Depending on the pricing option you select the discount can be up to 75% compared to the on-demand instances. This pricing option is useful if you know in advance the period of time you need it and you use this knowledge to get an additional discount (think to a database).

-   -   **Convertible reserved instances**, are reserved instances you can upgrade or downgrade the capacity (compute, storage, bandwidth). You can save up to 54%.
    -   **Scheduled reserved instances**, are reserved instances you can use in a fraction of day/week/month.

### Spot instances

It is useful for short workloads you run on instances unused by other people. You can bid to use an EC2 instance and if the spot price for an Ec2 is less than your bid price you can use it. It is possible you lose the instances at any time if your bid price is less than the spot price. You can save up to 90% with this kind of instance compared to on-demand instances. However, it is not good for a steady-state workload (i.e. database). You can use it for any distributed workload, batch jobs, data analysis, image processing, and so on. [Here](https://aws.amazon.com/ec2/spot/) you can find more details on Spot instances.

### Dedicated hosts and instances

Here briefly the difference between these two pricing options.

-   **Dedicated hosts**, you book an entire physical server. It’s the most expensive EC2 instance but it allows you to reuse your existing server-bound software licenses. You must reserve it for 3 years.
-   **Dedicated instances**, are instances running on hardware dedicated to you. May share hardware with other instances and you don’t have control over instance placement. [Check out here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html) for more details on the differences between Dedicated Hosts and Dedicated instances.

### Amazon EC2 Additional costs

If you have to manage an increase in the workload and you need to increase the number of instances, this will affects the prices as well. In addition, you should consider the use of a load balancer that sets additional costs on your bill.

There are additional services that you could need when you have to manage to scale for a workload increase. First of all, you can have CloudWatch that monitors your Ec2 instance at no additional costs.

If you want to use the Auto-Scaling service to manage the scale-in and scale-out process, there are no additional costs. The same is if you need an Elastic IP Address.

## Amazon EC2 Lifecycle

The lifecycle of Amazon EC2 is quite easy and you can see the state diagram in the following image. When you create an EC2 instance, you select the instance type and the OS to run on it. Initially, the machine goes directly in Running state. You can stop and start it again. Finally, when you don’t need it anymore you can terminate it. A terminated instance cannot go into the Running state again, usually, in few minutes the machine disappears from your instances list in the dashboard.  

![Amazon EC2 Lifecycle](assets/img/Amazon-EC2-Lifecycle-2.png){:width="450" height="332" .responsive_img}

### Amazon EC2 Shared Responsibility Model

The following figure summarizes the Shared Responsibility Model for Amazon EC2.

![AWS EC2 Shared Responsibility Model](assets/img/AWS-EC2-Shared-Responsibility-Model.png){:width="450" height="189" .responsive_img}

## Security Groups

A Security Group is like a built-in firewall for your virtual servers to give you full control over how accessible your instances are. You have to imagine it like a filter that acts in front of the EC2 instance to analyze and filter all the incoming and outgoing traffic. You can define which service to expose via a port, from which machine receives incoming traffic, or to which machine sends outgoing traffic.

![AWS Security Group Example](assets/img/AWS-Security-Group-Example.png){:width="450" height="99" .responsive_img}

_Photo from [http://progressivecoder.com](http://progressivecoder.com/understanding-aws-security-groups-and-best-practices-to-use-them/)_

By default, only port 22 is accessible via SSH using keys for authentication. For outgoing traffic, by default, there is one rule that allows all kinds of traffic. You can allow additional incoming traffic by adding new rules in whitelist mode (there are only ALLOW rules). At the same time, you can restrict the outgoing traffic by removing the default rule and allowing only specific traffic. In each rule you can define:

-   **Type**, indicate the traffic type, for example, HTTP, HTTPS, SSH, and so on.
-   **Protocol**, indicate the transport layer (i.e. TCP/UDP).
-   **Port**, the port range for the service (i.e. 80 for HTTP, 443 for HTTPS, 22 for SSH, and so on).
-   **Source**, from which IP or IP range receives the traffic.
-   **Destination**, to which IP or IP range sends the traffic.

For more details, [check out the following page](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html).

### Security Groups Example Scenario

The following figure shows an example of how to configure security groups in a typical multi-tier web application deployed on AWS.

![AWS Security Groups](assets/img/AWS-Security-Groups.png){:width="450" height="226" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

The three-tiers application is part of the same VPC and each tier belongs to a different subnet. Only the subnet containing the web tier is public while the others are private. On each tier, we can have one or more EC2 instances. All the instances accept ssh incoming traffic for administration.

Instances in the web tier only accept HTTP/HTTPS traffic. This tier calls API on the instances in the Application Tier that only accepts traffic from the instances in the Web Tier. The same occurs between Application and Database Tier.

## EC2 Launch Template

There are scenarios when you need to create multiple EC2 instances having the same characteristics. For example, if you need to run tests always on the same hardware and OS, it’s a waste of time to create the EC2 instances manually every time. If you need to scale in or out EC2 instances using the Autoscaling feature you cannot create them manually. Instead, you need to define their characteristics in a template and let the Autoscaling service use it to create the required machines.

Amazon AWS uses EC2 Launch Template to define the characteristics of an EC2 instance (CPU, RAM, Security Groups, tags, ssh leys, and so on).

## Conclusion

In this article, we introduced Amazon EC2, the service to rent computers in the Cloud. We saw how to secure them with Security Groups. In the [next article](definitive-amazon-ec2-tutorial-step-by-step-guide-beginners), we will do some hands-on lab on these resources.