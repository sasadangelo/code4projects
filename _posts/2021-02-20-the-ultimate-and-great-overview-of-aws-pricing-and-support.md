---
layout: post
title: The Ultimate and Great Overview of AWS Pricing and Support
post_series_id: getting-started-with-amazon-web-services
slug: the-ultimate-and-great-overview-of-aws-pricing-and-support
thumbnail: assets/img/AWS-Pricing.jpeg
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories: Cloud
---

![The Ultimate and Great Overview of AWS Pricing and Support](assets/img/AWS-Pricing.jpeg){:width="316" height="200" }

# The Ultimate and Great Overview of AWS Pricing and Support
_Posted on **{{ page.date | date_to_string }}**_

In this article, I want to show my understanding of AWS Pricing and Support. We will discuss the Amazon policies about pricing and the tool and services that help customers optimize costs and have them under control.

### Introduction to the AWS Pricing

Amazon Web Services platform uses a **“Pay as You Go”** pricing model. This means you only pay for the AWS resources you use and only for the time period you use them.

In AWS you only pay for three types of resources:

-   **Compute**. You pay only for the compute time (i.e. EC2, Lambda, Beanstalk, etc.) you consume.
-   **Storage**. You pay for the quantity of data stored (i.e. S3, RDS, etc.) in the Cloud.
-   **Data Transfer**. You pay for the data transferred out of a region. Data Transfer IN is free.

Moreover, **the more you consume the greater is the discounts you get**. In the Cloud world, you can start small and grow as your business grow. In fact, add new capacity or resources to your ecosystem is easy.

![AWS Pricing](assets/img/AWS-Pricing-2.jpeg){:width="450" height="285" }

### On-Demand vs Reserved resources

For resources like Amazon Ec2 and RDS, there are two pricing options:

-   **on-demand resources**, you pay what you consume. Therefore, you can start and stop resource usage whenever you want without long-term contracts and complex licenses.
-   **reserved resources**, you reserve the resource usage for a period of time. The benefit of this option is that you can save up to 75% depending on the up-front cost you are willing to pay. Reserved instances are available in three options: All up-front (called **AURI**), Partial up-front (**PURI**), No up-front (**NURI**) payments. Therefore, the larger the payment up-front you make, the greater the discount will be.

In AWS the most fundamental costs are for compute capacity, storage, and Data Transfer Out. Therefore, there is no charge for Data Transfer In.

### Free-Tiers

Some resources like Ec2, S3, EBS, ELB, and others offer free tier usage for the new customers. For example, Ec2 micro offers 1-year of free usage.

## AWS Pricing Details

In this section, I will briefly analyze the pricing details for some main resources.

### Amazon EC2 and EBS Pricing

You can read details about Amazon EC2 and EBS Pricing [in the following article](amazon-ec2-for-beginners).

### AWS Pricing for S3

The pricing for [S3 storage](amazon-web-services) depends on the Storage classes:

-   **Standard**, you pay for the number and size of objects which will have 9.999999999% durability and 9.99% availability.
-   **Standard-Infrequent Access (S-IA)**, where you store infrequent access objects with the same durability and availability of the Standard class but a lower costs.

There are other cost factors like the number and type of requests and the amount of data transferred out of an AWS region.

### Amazon RDS Pricing

Amazon RDS, like EC2, has two pricing options depends whether you use it on-demand or reserving it for a period of time. In the latter case, you can have a discount that is as larger as greater is the up-front cost you’re willing to pay. The service has several cost factors, like:

-   the engine, size, and memory in Gb;
-   database instances;
-   deployment type (with or without redundancy for failover).

There are no additional costs for the storage of your database backup unless the database instance is not terminated. Moreover, there is no charge for inbound data transfer while there are tiered charges for outbound data transfer.

### Amazon CloudFront Pricing

AWS pricing for Amazon CloudFront varies across geographic regions and it is mainly based on the number of requests and the amount of outbound data transfer.

## AWS Trusted Advisor

### The Problem

As your business grows your infrastructure grows as well and with a large number of resources in your environment, it’s hard to keep track of costs and optimize them over time.

![AWS Large Infrastructure](assets/img/AWS-Large-Infrastructure.png){:width="450" height="239" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

### What is AWS Trusted Advisor?

AWS Trusted Advisor is a tool that helps you to monitor the costs of your infrastructure, keep it under control and help you to save money. However, AWS Trusted Advisor is much more than this because it helps you in 4 big areas:

-   cost optimization;
-   performance;
-   security;
-   fault-tolerance.

In fact, AWS Trusted Advisor has a dashboard where it immediately shows you:

-   the passed checks;
-   the suggestion to investigate;
-   the urgent problem to address.

![AWS Trusted Advisory Dashboard](assets/img/AWS-Trusted-Advisory-Dashboard.png){:width="450" height="130" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

According to Amazon data, this tool helped customers to have 500 million suggestions for a 500$ M of cost-saving. You can use it in multiple scenarios. For example, imagine having an underused EC2 instance, in this case, AWS Trusted Advisor can suggest moving to a cheaper instance.

### How AWS Trusted Advisor works?

The tools scan your infrastructure and analyze all your resources and their usage. In addition, it compares this analysis with a set of best practices from which it determines if the resource is correctly used, there are possible optimization to investigate, or there are issues to solve.

![AWS Trusted Advisor](assets/img/AWS-Trusted-Advisor.png){:width="450" height="190" }

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

It is possible to send notifications for issues, you can send events to CloudWatch and run functions in AWS Lambda to automate recovering actions when a problem occurs.

## Support Plans

The AWS support plans assist you in three different situations:

-   you just need to play with the platform, experiment with it, and possibly use it in the future for production or mission-critical businesses;
-   once you have good confidence with the platform, you can decide to move your workload into production;
-   you have mission-critical businesses that you want to run on the AWS platform.

For each of these, respectively,  three types of needs AWS provides the following support plans:

-   **Developer**;
-   **Business**;
-   **Enterprise**.

Moreover, there is also the **Basic plan** that is the default when you subscribe with the platform and you just play a bit with it. It is free of charge. However, you have 24×7 customer support & communities, documentation, and forums. Moreover, AWS Trusted Advisor is available with 7 core checks and, the AWS Personal Health Dashboard to help you to check the healthiness of your services.

The following tables summarize the difference among the above support plans.

![AWS Support Plans](assets/img/AWS-Support-Plans.png){:width="450" height="266" }

_Photo from [https://tutorialsdojo.com](https://tutorialsdojo.com/aws-support-plans/)_

## Conclusion

In conclusion, I hope this article helped you to have a quick overview of the AWS Pricing models and support plans. My suggestion is to start with the Basic Plan, create a free EC2 instance to start playing with it for a year and with time add more resources to your workload and keep practice with the different services.