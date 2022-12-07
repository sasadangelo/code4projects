---
layout: post
title: How to increase Amazon EC2 Availability and Scalability
post_series_id: getting-started-with-amazon-web-services
slug: how-to-increase-amazon-ec2-availability-and-scalability
thumbnail: assets/img//load-balancer.png
excerpt: In this article, I talk about EC2 Availability and Scalability and how to increase them using AWS services like Load Balancers, Autoscalers, and DNS.
categories: Cloud
---

![How to increase Amazon EC2 Availability and Scalability](assets/img/load-balancer.png){:width="200" height="169" .responsive_img}

# How to increase Amazon EC2 Availability and Scalability
_Posted on **{{ page.date | date_to_string }}**_

In this article, I want to talk about EC2 Availability and Scalability concepts and how to guarantee them using AWS services like Load Balancers, Autoscaling,  and Route53.

## What is Availability?

In Computing, the term _Availability_ is strictly related to the concept of Uptime. Uptime is the amount of time a system is up and running. The term _Availability_ refers to the probability that a system is operational at a given time. Usually, the availability of a system is expressed with a percentage number that represents the amount of time a device is actually operating compared to the total time it should be operating.

For example, the following table list some availability numbers and the relative yearly, monthly, weekly, and daily downtime tolerated.

![Availability Table](assets/img/availability.jpeg){:width="450" height="149" .responsive_img}

A highly available system allows it to stay operational even when faults do occur. In order to do that, the system adds redundancy to its resources so that if a resource fails its redundant counterpart can still guarantee the service operational and give the system to heal itself automatically or with the help of the support team.

Ec2 instance availability can be increased by cloning them in different AZs in the same Region and use Load Balancers as an entry point for all the instances. If AZ A goes down, AZ B guarantees the continuity of the service.

![Ec2 Availability](assets/img/Ec2-Availability.png){:width="450" height="303" .responsive_img}

_Photo from [https://cloudaffaire.com](https://cloudaffaire.com/how-to-create-a-network-load-balancer-using-aws-cli/)_

## What is Scalability?

**Scalability** is the ability of a system to handle a growing amount of work by adding more resources to the system. Scalability can be measured over multiple dimensions, such as number of users, number of requests, number of transactions, and so on. From a scalability point of view, a system can scale horizontally or vertically.

### Horizontal Scalability

**Scaling horizontally** means adding more nodes to (or removing nodes from) a system, such as adding a new computer to a distributed software application. For Ec2 instances, horizontal scaling means add more instances (or remove instances) to a pool of instances where an application runs. In AWS terminology, **Scale-Out** means the increase in the number of EC2 instances while **Scale-In** means the opposite.

In the next sections, we will talk about AutoScaling and Elastic Load Balancers, two services that will help you to implement horizontal scalability.

### Vertical Scalability

**Scaling vertically** an Ec2 instance means adding more capacity (CPU, RAM, Disk spaces) to a computer or reducing it. In AWS terminology, **Scale-Up** means the increase of the EC2 capacity while **Scale-Down** means the opposite. For example, you can go from t2.micro (1 Gb RAM and 1 CPU) to t2.small (1 CPU and 2 Gb RAM).

### Scalability vs Elasticity

Sometimes people confuse Scalability with **Elasticity**. Once a system is scalable, the term Elasticity refers to the ability of a system **to fits the requirements of a workload** as it changes (increasing or decreasing) over time. Usually, the Elasticity concept is connected to the Pay as you go model, where customers pay for the number of the capacity of resources in use.

## **Load Balancers**

When you scale in or out EC2 instances you need a mechanism to:

-   spread all the incoming requests to one of the downstream instances;
-   expose a single entry point (IP address) to the users so that the complexity to manage multiple EC2 instances is hidden;
-   do a regular health check of the instances to detect unhealthy ones.
-   avoid redirecting traffic to unhealthy instances until they are not replaced.

In AWS the Load Balancers provides all these features. A Load Balancer is a machine (typically an Ec2 instance) that redirects the traffic to the downstream EC2 instances and provides all the above features. In addition, in AWS the load balancers provide Multi-AZ deployment for high availability and support for HTTPS.

![AWS Load Balancer](assets/img/elb_instances_1.png){:width="450" height="391" .responsive_img}

Theoretically, a customer can create its own HTTP/HTTPS load balancer by buying an Ec2 instance and deploy a reverse proxy like Nginx. However, in this case, the customer must manage everything by himself like os guest patching, Nginx deployment, maintenance, Multi-AZ deployment, and so on. With AWS Elastic Load Balancers Amazon takes care of all these kinds of stuff at a much lower cost.

AWS supports three load balancers type: **Classic, Networking,** and **Application**.

### Classic Load Balancer

**Classic Load Balancer** is a Layer 4 and 7 load balancer. It publishes a single IP where clients can connect to. It keeps track of all the EC2 instances where the application runs and split the traffic among them. In the case of EC2 instance failure, the component works in sync with Autoscaler to allocate a new one. Classic Load Balancer targets Ec2 instances directly even in different AZ. **AWS si slowly retiring this load balancer type in favor of Application and Network Load Balancers.**

![AWS Classic Loadbalancer](assets/img/AWS-Classic-Loadbalancer.png){:width="450" height="407" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Application Load Balancer

**Application Load Balancer (ALB)** is a Layer 7 only load balancer. It supports:

-   protocols like HTTP, HTTPS, HHTP/2, and WebSocket;
-   enhanced metrics and access logs;
-   native IPV6 support in a VPC;
-   the ability to enable more routing mechanisms for your requests (path and host-based);
-   AWS firewall web application integration, and more target health checks.

ALB introduces three new concepts: **Listeners**, **Target**, **Target Group**. Listeners are the process that listens for incoming requests. They use **Rules** to decide the type of incoming requests to accept. For example, you can decide to accept only HTTPS traffic on the 443 port. Target is the destination of the incoming requests. You can group Targets in a Target Group. The component performs health checks at the Target Group level.

![AWS Application Loadbalancer](assets/img/AWS-Application-Loadbalancer.png){:width="450" height="200" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

Application Load Balancers are useful in a lot of scenarios. One is the ability to use containers to host the microservices of your application and route the traffic from a single load balancer. If your application is a stack of three containers (i.e. web, application, and database servers) all running on the same EC2 instance, it can route the traffic on a different path based on the port number.

### Network Load Balancer

**Network Load Balancer** is a Layer 4 only load balancer. The same concept of Listeners, Target, and Target Groups are valid for these load balancers. It supports:

-   forward TCP and UDP traffic to the Target Groups;
-   higher performance than ALB handling millions of request per second;
-   lower latency than ALB (100 ms vs 400 ms of ALB);
-   a static IP for each AZ instead of a hostname.

## Auto-Scaling

Auto-Scaling allows you to scale EC2 instances based on your needs. Using the Auto-Scaling features you remove the guesswork on how to size your infrastructure because it adjusts capacity as needed avoiding Unused or Over Capacity.

![AWS Autoscaling](assets/img/AWS-Autoscaling.png){:width="450" height="225" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

Imagine you have a web server deployed on two EC2 instances in a VPC with two public subnets in two Availability Zones (AZ). In this scenario, the idea of autoscaling is that you can monitor the application using Amazon CloudWatch and when a resource (i.e. CPU, Memory,  Traffic, etc.) reaches a threshold, it generates an event that you can associate with an EC2 instances increase or decrease. For example,  you can decide that when CPU > 80% you increase EC2 instances by 1 while if CPU <5% you decrease it by 1.

The following figure shows an example of a CloudWatch alarm configuration that triggers an Auto-Scaling event when the CPU reaches 80%.

![AWS CloudWatch Alarm](assets/img/AWS-CloudWatch-Alarm.png){:width="450" height="242" .responsive_img}

Auto-Scaling has three components:

-   **Launch Configuration**;
-   **Auto-Scaling Group**;
-   **Auto-Scaling Policies**.

The Launch Configuration specifies **what to launch**, for example, the Instance type, the OS image, the default number of EC2 instances. The Auto-Scaling Group specifies **where to launch**, for example, the VPC, subnets, min and max capacity, desired capacity, and load balancer. Finally, the Auto-Scaling Policies specify **when to launch**, for example, with scheduling, on-demand, Scale-Out, and Scale-In policies.

![AWS Autoscaling Components](assets/img/AWS-Autoscaling-Components.png){:width="450" height="185" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Elastic IP Addresses

In combination with Load Balancers, AWS uses Elastic IP Addresses for High Availability.  These are static IP addresses that can reference a new resource (i.e. Ec2) when the old one is unavailable.

## **Route 53**

It is the Amazon DNS service designed to provide businesses and developers with a reliable and high scalable way to route end users to internet applications. Think of Route 53 as an address book, if you want to go to Bob’s house (the application www.example.com) it will provide its address, for example, 5555 South Park Street (the IP address 13.11.5.12). You can think of an Internet application as a sort of website running on a computer on the Internet.

In the Internet architecture, you can reach a remote computer using its IP address (i.e. 13.11.5.12), the problem is that these numbers are hard to remember. For this reason, DNS services were introduced a long time ago as a mechanism to replace these numbers harder to remember with a mnemonic name like www.application.com. When a user opens his browser and writes www.application.com in the address bar, the browser contacts the DNS to know how to translate that name into an  IP address.

Sometimes to translate a domain name into an IP address it could be necessary the use more DNS services around the globe, however, it is completely transparent to the end-user.

### Route 53 typical scenario

Suppose you want to access the application example.com hosted on Amazon AWS. Then your browser contacts the Internet Service Provider DNS to translate it into an IP address. This DNS service will contact Route 53 that will convert that name into the IP address 54.85.178.219 that the browser will receive and use it to contact the application running on an EC2 instance in the AWS Cloud.

![Route 53 Examples](assets/img/Route-53-Examples.png){:width="450" height="214" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

In order to translate domain names into IP addresses, Route 53 uses two concepts: **Hosted Zone** and **RecordSet**. Usually, a Hosted Zone is associate with a domain (i.e. example.com) and you can define it as public or private. In our example, the Hosted Zone must be public.

-   **domain**: example.com
-   **type**: public

Then you can associate to the Hosted Zone one or more RecordSet, in our example, one is enough. In the RecordSet you need to specify:

-   **subdomain**: www
-   **type**: A IPV4
-   **value**: 54.85.178.219
-   **Routing policy**: Simple

![Route 53 Hosted Zone](assets/img/Route-53-Hosted-Zone.png){:width="450" height="203" .responsive_img}

Route 53 supports several routing policy:

-   **Simple**
-   **Geolocation**
-   **Weighted Round Robin**
-   **Latency based**
-   **Multivalue answer**

## Conclusion

In this article, we talked about the availability and scalability concepts and how to achieve them using Load Balancers and Austoscalers. [In this article](elastic-load-balancer-tutorial), we will do some hands on on Load Balancers and [in this other article](ec2-auto-scaling-group-tutorial-for-beginners), we will do some hands on Autoscalers.
