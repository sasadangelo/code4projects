---
layout: post
title: Amazon Elastic Block Storage (EBS) vs Elastic File Storage (EFS)
post_series_id: getting-started-with-amazon-web-services
slug: amazon-elastic-block-storage
image: /wp-content/uploads/2021/03/HDD-SDD-mini.png
excerpt: In this article, I am going to talk about Amazon Elastic Block Storage (EBS) and Elastic File Storage (EFS).
categories: Cloud
---

![Amazon Elastic Block Storage (EBS) vs Elastic File Storage (EFS)]({{ site.baseurl }}/wp-content/uploads/2021/03/HDD-SDD-mini.png){:width="356" height="200" .responsive_img}

# Amazon Elastic Block Storage (EBS) vs Elastic File Storage (EFS)
_Posted on **{{ page.date | date_to_string }}**_

In this article, I am going to talk about Amazon Elastic Block Storage (EBS) and Elastic File Storage (EFS). **Storage** is the second most important service category in AWS after Compute. AWS supports three Storage categories: **Block**, **File**, and **Object Storage**. Object Storage will be the subject of a future article.

### Amazon EBS Service

The AWS EBS service allows you to create **network-attached volumes** for your EC2 instance. Since it uses the network to communicate with the Compute node there could be a bit of latency. The word Elastic means that it is possible to **scale up or down the volume size depending on needs**. By default, the EC2 instance uses one EBS volume as a root filesystem. You can decide if it should persist after the EC2 instance termination using the **delete on termination** attribute.

However,  you can attach more EBS volumes to an EC2 instance depending on your needs. For example, if you are running a database service on your EC2 instance you can choose to create a volume for your data. The service allows you to choose the **Block Storage type** between **Hard Disk Drive** (**HDD**) or **State-Solid Drive** (**SSD**). For your storage data, for example, choose an SSD is better because it provides better performance, while for logs you can decide to use HDD because cheaper.

![Amazon Elastic Block Storage]({{ site.baseurl }}/wp-content/uploads/2021/01/HDD-SDD.png){:width="450" height="253" .responsive_img}

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

As a general rule of thumb, **you can attach an EBS volume to a single EC2 instance at a time in the same AZ**. However, recently Amazon introduced the **EBS Multi-Attach feature** that enables you to attach a single Provisioned IOPS SSD (`io1` or `io2`) volume to multiple instances that are in the same Availability Zone. Each instance has full read and writes permission to the shared volume. Finally, EBS supports encryption in a way transparent to the end-user.

### Amazon Elastic Block Storage Lifecycle

When you create an EBS Volume it is in an unattached state. In order to use it in an EC2 instance, you first need to attach it so that it is visible as a block device. Then you can mount it to a folder and start using it. Once you finished working with the volume and you don’t need it anymore, you can unmount it from the folder and detach it from the EC2 instance.

When you attach the EBS volume to an EC2 instance you can decide to connect its lifecycle with the EC2 one using the **delete on termination** attribute mentioned above. In this case, if you terminate the EC2 instance the volume will terminate as well.

![Amazon Elastic Block Storage Lifecycle]({{ site.baseurl }}/wp-content/uploads/2021/03/Amazon-EBS-Lifecycle.png){:width="450" height="450" .responsive_img}

### Amazon EBS is AZ locked

You **must create EBS volumes on the same AZ** of the EC2 instance.

The following figure shows the US-EAST Region with two AZs US-EAST-1A and US-EAST-1B. In these AZs there are 3 EC2 instances. Two instances have a single EBS volume attached, the third EC2 has two volumes attached. Finally, there is an EBS volume in US-EAST-1B unattached.

![Elastic Block Storage is AZ locked]({{ site.baseurl }}/wp-content/uploads/2021/03/AWS-EBS-Topology.png){:width="450" height="206" .responsive_img}

### Amazon EBS Pricing

For [EBS service the pricing](https://aws.amazon.com/ebs/pricing/) change depending on the:

-   size of the volume in Gb;
-   the type of volume, for example, General Purpose (SSD), Provisioned IOPS (SSD), Magnetic;

Amazon EBS service allows you to create backups of your volumes and there is an additional cost for this option. Moreover, there are costs for data transfer. Moreover, Outbound Data Transfer charges are tiered, while Inbound Data Transfer is always free.

## Amazon EBS Snapshots

Amazon EBS Snapshots are a point-in-time copy of your block data. For the first snapshot of a volume, Amazon EBS saves a full copy of your data (only blocks containing data) to Amazon S3. EBS Snapshots are stored incrementally, which means you are billed only for the changed blocks stored.

### Move EBS volume across AZs

If you want to move an EBS volume from one AZ to another you need to create a **snapshot** and create a volume from it in the new AZ because they are visible in the whole region. You can copy a snapshot in another region so you can easily create a volume from it in this new region.

![AWS EBS Snapshots]({{ site.baseurl }}/wp-content/uploads/2021/03/AWS-EBS-Snapshots.png){:width="450" height="154" .responsive_img}

### Move EC2 instance cross AZs

You can use EBS snapshot also to move an EC2 instance from one Az to another. In this case, you create a snapshot for EC2 instance EBS volume, then create a custom Amazon Image (AMI) from it. The AMIs like Snapshots have a regional scope and you can use it in another AZ to recreate the EC2 instance. Copying the AMI in another region you can even move the EC2 instance volume to another region.

![Move EC2 instance cross AZs]({{ site.baseurl }}/wp-content/uploads/2021/03/EC2-instance-cross-AZ.png){:width="450" height="175" .responsive_img}

## AWS Elastic File Storage

It is a Network Filesystem that you can use when you need to share the same filesystem over multiple EC2 instances. You can attach an EFS up to 100s EC2 instances. The word Elastic means that you don’t need capacity planning since you can increase or decrease the filesystem size based on your needs. This filesystem works only with Linux EC2 instances and it is accessible to EC2 instances in multiple AZs in the same region.  

![Amazon EFS]({{ site.baseurl }}/wp-content/uploads/2021/03/Amazon-EFS.png){:width="450" height="533" .responsive_img}

It is possible to associate a Security Group with an EFS service so that you can control its inbound and outbound traffic. EFS service is more expensive than EBS (almost three times more) but you only pay for the capacity in use.

## AWS EC2 Instance Store

EC2 Instance Store volumes are physical-attached storage that provides better performance than EBS volumes. Basically, they are physical SSD or Magnetic disks attached to EC2 instances. By definition, they can only live in the same AZ of the attached EC2 instance. However, even if they perform better they are not durable because the data are lost when the EC2 instance terminates. Data are lost even for hardware failure. For this reason, they are a good solution for a buffer, cache, and temporary data.

## Conclusion

In this article, we introduced Amazon EBS and EFS, two storage services in the Amazon Cloud. We saw also how to attach volumes to these computers using the EBS service. Moreover, we analyzed briefly other Storage services like Amazon EFS and EC2 Instance Store. In the [next article]({{ site.baseurl }}/amazon-ebs-tutorial/), we will do some hands-on lab on these services.