---
layout: post
title: Amazon EBS Tutorial - Step by step Guide for Beginners
post_series_id: getting-started-with-amazon-web-services
slug: amazon-ebs-tutorial
thumbnail: wp-content/uploads/2021/06/Amazon_EBS.png
excerpt: In the previous article, I talked about Amazon Elastic Block Storage (EBS) service and this is a hands-on tutorial the will help you to learn how to use it.
categories: Cloud
---

![Amazon EBS Tutorial: Step by step Guide for Beginners]({{ site.baseurl }}/wp-content/uploads/2021/06/Amazon_EBS.png){:width="200" height="200" .responsive_img}

# Amazon EBS Tutorial: Step by step Guide for Beginners
_Posted on **{{ page.date | date_to_string }}**_

In the [previous article]({{ site.baseurl }}/amazon-elastic-block-storage/), I talked about Amazon Elastic Block Storage (EBS) service and this is a hands-on tutorial the will help you to learn how to use this service.

## How to create an EBS volume and attach it to your EC2 instance

There could be a scenario when you have to attach a second EBS volume to your EC2 instance. A typical scenario is when you run a database server and you want to use different storage for your data. This approach is particularly useful because you can backup your storage using snapshots.

### Create the Amazon EBS Volume

In the left menu of the EC2 dashboard select the **Volume** link in the **Elastic Block Store** section.

![Amazon EBS Volume Menu]({{ site.baseurl }}/wp-content/uploads/2021/03/1-Amazon-EBS-Volume-Menu.png){:width="450" height="210" .responsive_img}

You’ll see the 8Gb volume attached to your EC2 instance. To create a new volume click on the **Create Volume** button.

![Amazon EBS Create Volume]({{ site.baseurl }}/wp-content/uploads/2021/03/2-Amazon-EBS-Create-Volume.png){:width="450" height="152" .responsive_img}

You can specify the size of your disk. Remember that you only have 30 Gb for your Free Tier and since 8 Gb are already in use you can allocate a max of 22 Gb at no cost. You can also assign tags to your volume. Click on the **Create Volume** button.

![Amazon EBS Configure Volume]({{ site.baseurl }}/wp-content/uploads/2021/03/3-Amazon-EBS-Configure-Volume.png){:width="450" height="240" .responsive_img}

Your volume is now available but not yet attached to your EC2 instance. So, for the moment, it is available but not usable by your instance.

![Amazon EBS Volume Created]({{ site.baseurl }}/wp-content/uploads/2021/03/4-Amazon-EBS-Volume-Created.png){:width="450" height="75" .responsive_img}

### Attach the EBS Volume to the EC2 Instance

Select the volume and click on the **Action**\->**Attach Volume** menu.

![Amazon EBS Attach Volume]({{ site.baseurl }}/wp-content/uploads/2021/03/5-Amazon-EBS-Attach_Volume.png){:width="450" height="271" .responsive_img}

Select your EC2 instance and click the button **Attach**.

![Amazon EBS Attach Volume]({{ site.baseurl }}/wp-content/uploads/2021/03/6-Amazon-EBS-Attach_Volume-2.png){:width="450" height="168" .responsive_img}

In the Block devices dashboard, you can see the new volume attached to your EC2 instance. You can now mount it on a folder.

![Amazon EBS Volume Attached]({{ site.baseurl }}/wp-content/uploads/2021/03/7-Amazon-EBS-Volume-Attached.png){:width="450" height="122" .responsive_img}

### Mount the EBS Volume in Linux

In order to mount your volume on a folder, you need to know its device name in Linux. You can do that by running the command **lsblk**. In the image, you can see its name is **xvdf**.

![Amazon EBS List Block Devices]({{ site.baseurl }}/wp-content/uploads/2021/03/8-Amazon-EBS-List-Block-Devices.png){:width="450" height="132" .responsive_img}

Format the volume with whatever filesystem. For this tutorial, I used the ext3 filesystem using the following command:

_sudo mkfs -t ext3 /dev/xvdf_

![Amazon EBS Format Volume]({{ site.baseurl }}/wp-content/uploads/2021/03/9-Amazon-EBS-Format-Volume.png){:width="450" height="195" .responsive_img}

Now you can mount the volume on a folder with the command:

_sudo mount /dev/xvdf /home/ubuntu/folder/_

![Amazon EBS Mount Volume]({{ site.baseurl }}/wp-content/uploads/2021/03/10-Amazon-EBS-Mount-Volume.png){:width="450" height="37" .responsive_img}

To verify the volume is correctly mounted run the **mount** command.

![Amazon EBS List Volumes Mounted]({{ site.baseurl }}/wp-content/uploads/2021/03/11-Amazon-EBS-List-Volumes-Mounted.png){:width="450" height="347" .responsive_img}

You can start using your volume in the _/home/ubuntu/folder_.

## Move EBS volume cross AZs with Snapshots

In the previous article, I discussed in theory how to move EBS cross AZs using Snapshots. In this section, I will show you how to do it in practice.

Select the **Volume** link in the **Elastic Block Store** section of the left menu in the EC2 dashboard. Select the volume of your EC2 instance, click the **Actions** button and select **Create Snapshot**.

![Create EBS Snapshot]({{ site.baseurl }}/wp-content/uploads/2021/03/1-Create-Snapshot.png){:width="450" height="195" .responsive_img}

Choose a name for your snapshot and one or more tags to classify it (this is optional). Click the **Create Snapshot** button.

![Configure EBS Snapshot]({{ site.baseurl }}/wp-content/uploads/2021/03/2-Configure-Snapshot.png){:width="450" height="169" .responsive_img}

Your snapshot is created. You can see it by selecting the link **Snapshot** in the same menu section above. The snapshot will be visible in all the AZs of the Region.

![EBS Snapshot Created]({{ site.baseurl }}/wp-content/uploads/2021/03/3-Snapshot-Created.png){:width="450" height="124" .responsive_img}

Now you can create a volume in another AZ using this snapshot. Select the snapshot and click **Actions**\->**Create Volume** button.

![EBS Create Volume from Snapshot]({{ site.baseurl }}/wp-content/uploads/2021/06/EBS-Create-Volume-from-Snapshot.png){:width="450" height="175" .responsive_img}

Insert the size of the volume that should be greater than the snapshot’s size. Insert the new AZ (different from the previous one) where create the volume. Click the **Create Volume** button.

![Create EBS Volume from Snapshot]({{ site.baseurl }}/wp-content/uploads/2021/06/EBS-Create-Volume-from-snapshot-another-AZ.png){:width="450" height="279" .responsive_img}

You can see the new volume in a different AZ us-east-1b.

![EBS list volumes]({{ site.baseurl }}/wp-content/uploads/2021/06/EBS-Volume-list.png){:width="450" height="113" .responsive_img}

You can attach the volume to an EC2 instance in us-east-1b AZ.

## Move EC2 instance in another AZ

### Move EC2 instance in another AZ with Snapshots

The procedure to move an EC2 instance in another AZ of the same region is similar to the procedure to move EBS volume. You need to create a snapshot of the boot volume with your customization, then create an Amazon Machine Image (AMI) from that snapshot. You can see the procedure to create the snapshot in the previous section.

To create an AMI from the boot volume snapshot you simply need to select it and then click **Actions**\->**Create Image** on the Snapshot web page. You can assign a name to your image.

![Create AMI]({{ site.baseurl }}/wp-content/uploads/2021/03/4-Create-AMI.png){:width="450" height="238" .responsive_img}

Once the image is created you can see it by clicking the link **Images**\->**AMIs** in the left menu. AMI has regional scope so it is visible in all the AZ.

![Launch EC2 from AMI]({{ site.baseurl }}/wp-content/uploads/2021/03/6-Launch-EC2-from-AMI.png){:width="450" height="76" .responsive_img}

At this point, you can create the EC2 instance from this API as shown in the [first section of this article]({{ site.baseurl }}/definitive-amazon-ec2-tutorial-step-by-step-guide-beginners/). In order to create the EC2 instance from your own AMI in **Step 1: Choose an Amazon Mchine Image (AMI)** page, select the tab **MyAMI**.

If your EC2 instance has more volume attached to it, you can create a snapshot from them and recreate the volumes in the new AZ as shown in the previous section. Then you can attach them to the new EC2 instance.

### Move EC2 instance in another AZ without Snapshots

There is an easier method to create an AMI from an EC2 instance. You can simply go to the EC2 dashboard and stop the instance. Then you can right-click on it and select Image and template->Create image menu. In this way, the AMI will be automatically created from the boot volume without the need to create a snapshot first.

![Create AMI from EC2 instance]({{ site.baseurl }}/wp-content/uploads/2021/06/Create-AMI-from-EC2-instance.png){:width="450" height="347" .responsive_img}

## Conclusion

In the [previous article]({{ site.baseurl }}/amazon-elastic-block-storage/), we talked about EBS and EFS storage from a theory point of view. In this article, we saw how to use all these concepts in practice.

\* _Feature image from [https://data-flair.training](https://data-flair.training/blogs/aws-ec2-tutorial/)_
