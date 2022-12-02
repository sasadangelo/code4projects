---
layout: post
title: Amazon Integrated Services (part 2)
post_series_id: getting-started-with-amazon-web-services
slug: amazon-integrated-services-3
thumbnail: assets/img/CloudWatch-CloudFront-SNS-CloudFormation.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories: Cloud
---

![Amazon Integrated Services (part 2)](assets/img/CloudWatch-CloudFront-SNS-CloudFormation.png){:width="200" height="200" }

# Amazon Integrated Services (part 2)
_Posted on **{{ page.date | date_to_string }}**_

In this article, I am going to continue my overview of the Amazon Integrated Services, trying to explain my understanding of the following services:

-   Simple Notification Service (SNS)
-   CloudWatch
-   CloudFront
-   CloudFormation

Before reading this, make sure [you read this](amazon-web-services) and [this](amazon-integrated-services-2).

## **Simple Notification Service** (**SNS**)

The Simple Notification Service (SNS) is a notification system that allows decoupling microservices or sends notifications (i.e. email) when an event occurs. For a better understanding of this service let’s consider the following items:

-   SNS is a flexible, fully-managed publish/subscribers messaging and mobile notification system;
-   coordinates the delivery of messages to subscribing  endpoints and client;
-   easy to set up, operate and send reliable communications;
-   decouple and scale microservices, distributed systems, and serverless applications.

The following figure shows the two typical usages of Amazon SNS: **Amazon SNS Pub/Sub Messaging** and **Amazon SNS Mobile Notifications**. In the former, the publisher sends notifications to subscribers that could be Lambda, SQS, or HTTP/S services. In the latter, Publisher sends a notification to the mobile subscribers via ADM, Baidu, and others.

![Amazon SNS](assets/img/Amazon-SNS.png){:width="450" height="252" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

## CloudWatch

Amazon CoudWatch is a real-time monitoring system for Amazon Web Services (AWS) resources and applications. The system. CloudWatch works with the following elements:

-   **Metrics**, collect and track metrics;
-   **Logs**, collect and monitor log files;
-   **Alarms,** it set alarms;
-   **Events**, automatically react to changes;
-   **Dashboards**, to view the metrics and logs.

For each AWS resource, CloudWatch monitors a set of metrics. For example, for EC2 instances it monitors CPU, Status, Memory, etc. These statistics are visible to customers via the management console. When a metric reaches a threshold an alarming turn on and an action (SNS, Autoscaling, etc.) starts.

![Amazon CloudWatch](assets/img/Amazon-CloudWatch.png){:width="450" height="195" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

In [this article](ec2-auto-scaling-group-tutorial-for-beginners), you can see an example of EC2 scale up when CPU > 80%. There are other useful use cases where you can use CloudWatch:

-   respond to a state change in an AWS resource  (see the example of EC2 instance scale up when CPU > 80%).
-   when an EC2 scale-up occurs an AWS Lambda function can update DNS for the new IP.
-   take a snapshot of volumes when an event occurs;
-   run s3 event when a CloudWatch alarm is on;
-   much more.

### CloudWatch Metrics

Each AWS resource has its own set of metrics customers can monitor. For example, CPU and Memory for an EC2 instance, disk usage for an S3 bucket, and so on. A metric is a time-ordered set of data points that monitor resource usage and performance. At the default metrics, customers can add custom metrics that enrich the system monitoring.

### CloudWatch Logs

Customers can monitor CloudWatch Logs to search for string or pattern and take an action when a match occurs. CloudWatch Logs keep track of AWS Ec2 logs, monitor AWS CloudTrail logged events, archive or rotate log data.

### CloudWatch Alarms

An alarm monitors a single CloudWatch metrics and when it reaches a threshold, one or more actions are invoked. An action could be an SNS notification, an AWS Lambda function, an Autoscaling action, and so on. In the example above, for the CPU metric, we can define an Alarm that when CPU > 80% for 5 minutes an Autoscale action starts.

### CloudWatch Events

CloudWatch events are near real-time stream of system event that describes changes in AWS resources. You can use simple rules to match these events and route them to one or more target functions or streams. With these events, you are aware of operational changes occurring in the environment and react to them accordingly. Customers can set up automatic actions to react to these events.

An example of Events is when an EC2 instance is created due to a scale-up action. In this case, you can associate this event with a CloudWatch action that calls a Lambda function that sends an email to the administrator to inform him that a new EC2 instance exists in his environment.

### CloudWatch Dashboards

You can monitor AWS resources via dashboards in the management console. Configure the CloudWatch home page to monitor, in a single view, the most important metrics of your system. Create a customized view of a dashboard using the management console, AWS CLI, or _PutDashboard_ APIs.

## **Cloudfront**

Amazon CloudFront is the Content Delivery Network (CDN) of the Amazon platform. The basic idea is that if you have an application (i.e. a video stream like Netflix) in San Paolo and your end-users are in New York, in order to reduce the video stream latency, the video replicated in a location near New York.

In the [second article of this series]amazon-web-services), I talked about the AWS Global Infrastructure and its 210 Edge Locations where customers can replicate their content. The advantages for a customer to use this service are the following:

-   leverage on the AWS Global Infrastructure;
-   deep integration with all the AWS services;
-   secure content at the edge;
-   high performance because critical data (i.e. video, music, etc.) are cached.;
-   leverage on a number of scales to reduce costs;
-   easy to use.

CloudFront supports two types of content to cache:

-   **RTMP**, for media content like video and music;
-   **Web**, for images and other application assets used in normal websites.

When you create a CDN for your application you need to specify:

-   the **domain** of your application;
-   the **origin path** and **id**, necessary to create an address for your CDN content;
-   SSL support;
-   and others.

CDN is useful in a lot of scenarios, for example:

-   media (video and music) distribution;
-   asset caching for web applications;
-   software distribution;
-   API acceleration;
-   much more.

## **Amazon CloudFormation**

### Overview

AWS CloudFormation simplifies the task of repeatedly and predictably creating groups of related resources that power your application. Basically, it is the pipeline system you can use to manage application resources lifecycle like deploy, remove, and update. It is the basic component to manage DevOps activities on the system.

You can use the management console, AWS CLI, or SDK to provision AWS resources in your account environment. For example, you can create a pipeline that creates a VPC in your account with a Public subnet and an EC2 instance that runs a web server. You can create an S3 bucket where, periodically, you can store the application logs, and so on. Users can access the web server via an Internet GAteway (IGW) The scenarios you can create are endless.

![Amazon CloudFormation Stack](assets/img/Amazon-CloudFormation-Stack.png){:width="450" height="200" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### Template file and Stack

In order to deploy, update, or remove AWS resources in a customer account, CloudFormation uses a Template file that contains a description of the resources that compose the customer environment. This template represents the customer’s “desired state” and CloudFormation takes care that the environment keeps it. It is in JSON or YAML format and it is self-explanatory.

![Amazon CloudFormation Template and Stack](assets/img/Amazon-CloudFormation-Template-Stack.png){:width="450" height="200" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

An important concept in CloudFormation is Stacks, which are the resources generated by a template file. Stacks are units of deployment you can create, update, or remove. CloudFormation creates Stacks in random order unless the customer doesn’t specify dependencies among resources.

Usually, customers use development, test, and production environment. In order to create them, customers can use a single template file where it uses different variables, parameters, and conditions for each environment. Template files and CloudFormation is the way the Amazon platform implements its **Infrastructure as a Code** (**IaaC**).

If you are new to CloudFormation you can use the **CloudFormation Designer** to define the template for your infrastructure. CloudFormation Designer is a drag and drop tool where you can design your environment and the tool automatically create the relative template for you.

## **Conclusion**

With this article, we terminated our AWS Integration Services overview. We analyzed Amazon SNS, CloudFront, CloudWatch, and CloudFormation. In the [next article](amazon-well-architected-framework), we will continue our overview of the AWS platform.