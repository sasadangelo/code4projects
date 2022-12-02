---
layout: post
title: A Step by step tutorial to create your first Elastic Load Balancer
post_series_id: getting-started-with-amazon-web-services
slug: elastic-load-balancer-tutorial
thumbnail: assets/img/Elastic-Load-Balancer.png
excerpt: In this article, I want to show you how to create your first AWS Elastic Load Balancer in the Amazon AWS platform.
categories: Cloud
---

![A Step by step tutorial to create your first Elastic Load Balancer](assets/img/Elastic-Load-Balancer.png){:width="215" height="200" }

# A Step by step tutorial to create your first Elastic Load Balancer
_Posted on **{{ page.date | date_to_string }}**_

In this article, I want to show you how to create your first AWS Elastic Load Balancer. Load Balancers are an essentials tool to improve the availability and scalability of the applications running on EC2 instances.

## Create your Application running on two EC2 instances

First of all, create an EC2 instance with a web server running a Hello World application [as shown in this tutorial](definitive-amazon-ec2-tutorial-step-by-step-guide-beginners). If everything works properly you should enter the EC2 public IP address in the browser address bar and show a “Hello World” message with the private IP of your instance.

![ELB Hello World](assets/img/2-ELB-Hello-World.png){:width="450" height="96" }

AWS platform allows you to easily duplicate your EC2 instance by simply right-clicking the EC2 instance in the EC2 dashboard and selecting the menu **Image and template** -> **Launch more like this**.

![ELB Duplicate EC2 Instance](assets/img/1-ELB-Duplicate-Ec2-Instance.png){:width="450" height="455" }

You should see two EC2 instances running in the EC2 dashboard. If you enter the IP of the second EC2 instance you should see a second “Hello World” message with a different IP. This IP later will help you to understand which EC2 instance will reply to your request.

![ELB Two EC2 Instances](assets/img/3-ELB-Two-Ec2-Instances.png){:width="450" height="218" }

Now you can create the Load Balancer that will live in front of your EC2 instances and will forward the requests to one or another to split the workload across them.

### Create the Application Load Balancer

In the EC2 dashboard select the **Load Balancers** item from the main menu. Then select the **Create Load Balancer** button.

![Create the Elastic Load Balancer](assets/img/4-ELB-Create-Load-Balancer.png){:width="450" height="341" }

You can choose to create one of the three load balancer types available: classic, application, or network. Select the **Create** button for **Application Load Balancer**. This load balancer works fine with HTTP/HTTPS applications like our “Hello World”. For more details about the features of these Load-Balancers [read the previous article](how-to-increase-amazon-ec2-availability-and-scalability).

![ELB Select Application Load Balancer](assets/img/5-ELB-Load-Balancer-Type.png){:width="450" height="207" }

### Configure the Elastic Load Balancer

Once you decided on the Elastic Load Balancer to use you need to configure it. Insert the name of the load balancer (i.e. Demo-LB) and leave the default Scheme **internet-facing** in order to make it accessible from the Internet. Leave also the default IP address type **ipv4**. As you can see, this load balancer, by default, uses an HTTP listener. When it receives traffic on 80 port it automatically redirects the request to one of the EC2 instances registered in the Target Group.

![ELB Configuration](assets/img/6-ELB-Configuration.png){:width="450" height="293" }

You can choose to add the fault tolerance to the load balancer itself. If you work with a single load balancer you’ll be affected by a single point of failure and this compromises the availability of your application. Amazon AWS allows you to replicate the load balancer across multiple AZ to improve its availability. Leave the default of 3 AZs.

![ELB Network Configuration](assets/img/7-ELB-Configure-Network.png){:width="450" height="215" }

In the [following article](amazon-ec2-for-beginners), I talked about Security Group as a way to protect traffic incoming or outgoing to an EC2 instance. In [this other article](definitive-amazon-ec2-tutorial-step-by-step-guide-beginners), I explained how to use them in practice. Security Group should be configured on Load Balancer as well in order to allow the incoming or outgoing traffic. For example, in this tutorial, in order to allow HTTP traffic, is fundamental to allow incoming traffic on port 80. It is not necessary to create a new Security Group, you can use the same used for EC2 instances.

![ELB-Security Group Configuration](assets/img/8-ELB-Configure-Security-Group.png){:width="450" height="200" }

### Create the ELB Target Group and register the two EC2 instances

The application load balancer listens on port 80 and redirects the traffic to the EC2 belonging to its Target Group. You need to create now the Target Group and insert the two Ec2 instances in it. Insert a name for the Target Group and leave all the default settings.

![ELB Create Target Group](assets/img/9-ELB-Create-Target-Group.png){:width="450" height="190" }

Add the two EC2 instances to the Target Group.

![Add EC2 to Target Group](assets/img/10-Add-EC2-to-Target-Group.png){:width="450" height="189" }

Review all the settings and click the **Create** button. You need to wait a while to let AWS provision the Load Balancer.

![Review ELB](assets/img/11-Review-ELB.png){:width="450" height="187" }

## How to test the Application Scalability

Once the Application Load Balancer is created you can select it and in the **DSN name** field, you can find the hostname to insert in the browser address bar.

![Get ELB URL](assets/img/12-Get-ELB-URL.png){:width="450" height="253" }

If you click repeatedly the browser **Reload** button you’ll find that the two EC2 instances will reply alternatively. You just tested that the workload is split equally on the two EC2 instances.

![Web Application for ELB](assets/img/14-Web-Application-ELB.png){:width="450" height="229" }

## How to test the Application Availability

In order to test the availability of the application, you should verify what happens when an EC2 instance crash. You can simulate it by stopping manually an EC2 instance.

![ELB Stop EC2 instance](assets/img/15-ELB-Stop-EC2-instance.png){:width="450" height="162" }

If you go on the load balancer Target Group you’ll notice that the load balancer health check detects that one instance is down and it redirects all the traffic to the other EC2 instance. In fact, you’ll see always the same “Hello World” message coming from the same IP.

![ELB Health check](assets/img/ELB-Health-check.png){:width="450" height="255" }

## Conclusion

In this article, I talked about Elastic Load Balancers and how to use them in practice. In particular, our tutorial shows how to use an Application Load Balancer. However, things are not really different if you use a Network Load Balancer that working at layer 4 of the IP stack and offers better performance. This is a good starting point to start using this tool on the Amazon platform. If you want more information refers to the [official documentation](https://aws.amazon.com/it/elasticloadbalancing/?whats-new-cards-elb.sort-by=item.additionalFields.postDateTime&whats-new-cards-elb.sort-order=desc).