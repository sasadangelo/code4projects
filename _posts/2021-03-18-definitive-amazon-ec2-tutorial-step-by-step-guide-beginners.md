---
layout: post
title: The Definitive Amazon EC2 Tutorial - Step by step Guide for Beginners
post_series_id: getting-started-with-amazon-web-services
slug: definitive-amazon-ec2-tutorial-step-by-step-guide-beginners
thumbnail: assets/img/Amazon-EC2-Tutorial.png
excerpt: In this Amazon EC2 Tutorial, I will show you how to create an EC2 instance, attach an EBS volume to it, and secure it with Security Groups.
categories: Cloud
---

![The Definitive Amazon EC2 Tutorial: Step by step Guide for Beginners](assets/img/Amazon-EC2-Tutorial.png){:width="341" height="200" }

# The Definitive Amazon EC2 Tutorial: Step by step Guide for Beginners
_Posted on **{{ page.date | date_to_string }}**_

In this Amazon EC2 Tutorial, I will show you how to create an EC2 instance and secure it with Security Groups. I will also show how to create Ec2 instances easily with EC2 launch templates.

Before to start you need to know that the Amazon dashboard can change over time and the screenshot in this article could not perfectly correspond to the one you see. Usually, when the dashboard change there is a period of time where a button appears on the top left that allows you to switch back to the old version.

## Create your first amazon EC2 instance

### Access to the EC2 Dashboard

Login to your AWS account with the administrative account you set up in a [previous tutorial](beginners-guide-identity-access-management). In the search bar write “EC2” and choose the Ec2 service.

![Amazon EC2 Hands On Lab](assets/img/1-Amazon-EC2-Hands-On-Lab.png){:width="450" height="166" }

The EC2 Dashboard will appear. On the home page, there is a summary of AWS resources allocated in your account directly related to EC2 resources. Select the link **Instances** to access the Instances management dashboard.

![Amazon EC2 Dashboard](assets/img/2-Amazon-EC2-Dashboard.png){:width="450" height="251" }

### Create the EC2 instance

Select the **Launch Instances** button to start the launching of your first Ec2 instance.

![Amazon EC2 Instances](assets/img/3-Amazon-EC2-Instances.png){:width="450" height="68" }

As a first step, select the operating system to install on your instance. Amazon AWS uses the concept of **Amazon Machine Image (AMI)** that are prebuilt images with a given operating system. The default image is the Amazon Image and here how Amazon defines it:

> _Amazon Linux 2 comes with five years support. It provides Linux kernel 4.14 tuned for optimal performance on Amazon EC2, systemd 219, GCC 7.3, Glibc 2.26, Binutils 2.29.1, and the latest software packages through extras. This AMI is the successor of the Amazon Linux AMI that is approaching end of life on December 31, 2020 and has been removed from this wizard._

The one I use in this tutorial is an image with Ubuntu 20 for 64-bit x86 architecture. Click on the **Select** button.

![Amazon EC2 Select Operating System](assets/img/4-Amazon-EC2-Select-Operating-System.png){:width="450" height="54" }

Select the **t2.micro** instance type because it is the only one eligible for Free Tier. This instance has 1 CPU, 1 Gb RAM, and up to 30 Gb of storage you can attach to it. This is enough for our tests. Click on the **Next: Configure Instance Details** button.

![Amazon EC2 Select T2 Micro](assets/img/5-Amazon-EC2-Select-T2-Micro.png){:width="450" height="180" }

In the next panel, you can configure your EC2 instance. For example, if you select a subnet in your VPC you can force your EC2 instance in a specific AZ. However, for our test leave all the defaults and enter the following code in the **User Data** text field at the end of the page. Click the **Next: Add Storage** button.

{% highlight shell %}
#!/bin/bash
# Use this for your user data (script from top to bottom)
# install httpd (Linux 2 version)
sudo apt-get update
sudo apt-get install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
echo "<h1>Hello World from $(hostname -f)</h1>" > /var/www/html/index.html
{% endhighlight %}

![Amazon EC2 Configure Instance](assets/img/6-Amazon-EC2-Configure-Instance.png){:width="450" height="184" }

Now you can create volumes to attach to your EC2 instances. By default, EC2 has a volume of 8 Gb attached that will be mounted as a root file system. You can change the capacity of the disk up to 30 Gb in the Free Tier. Click the **Next: Add Tags** button.

![Amazon EC2 Add Storage](assets/img/7-Amazon-EC2-Add-Storage.png){:width="450" height="185" }

Tags are a useful way to classify your AWS resources. It is really important when you have a lot of resources to manage. For example, in this test, we associate a “department” tag with the value “engineers”. Click the **Next: Configure Security Group** button.

![Amazon EC2 Add Tags](assets/img/8-Amazon-EC2-Add-Tags.png){:width="450" height="184" }

In this step, you can configure the EC2 Security Groups. By default, port 22 is open in order to allow you to access the machine remotely via SSH. In the next steps, you have to generate Keys to access the instance because they are more secure than passwords. Click the **Next** button. I opened also port 80 that is accessible only from my IP. In order to know which is my public IP, [I use this website](https://www.whatismyip.com/ip-whois-lookup/). This is required to access the website running on the EC2 instance. Click the **Review and Launch** button.

![Amazon EC2 Configure Security Group](assets/img/10-Amazon-EC2-Configure-Security-Group.png){:width="450" height="182" }

You can review now your EC2 instance and click the **Launch** button.

![Amazon EC2 Review Instance](assets/img/9-Amazon-EC2-Review-Instance.png){:width="450" height="183" }

![Amazon EC2 Review Instance Launch](assets/img/11-Amazon-EC2-Review-Instance-Launh.png){:width="450" height="181" }

Now, in order to access remotely to your EC2 instance, you need to generate a Key Pair. Click the button **Download Key Pair** to save them on your computer. It’s important you do it immediately because it is your only chance to see your keys. You can click the **Launch Instances** button and wait until your EC2 instance is up and running.

![Amazon EC2 Create Key Pairs](assets/img/12-Amazon-EC2-Create-Key-Pairs.png){:width="450" height="329" }

Now you can see the instance running. Select it and in the below box you can see the IP address and the domain name you will use later to access the Ec2 instance via SSH. This image has been taken for another EC2 instance. Assume the IP is **19.15.10.10** and the domain name is **ec2-19-15-10-10.compute-1.amazonaws.com**.

![AWS EC2 IPs Domain name](assets/img/AWS-EC2-IPs-Domain-name.png){:width="450" height="211" }

## How to access the EC2 instance

### How to access the EC2 instance via SSH

Save your key under whatever folder in **~/.ssh**. For example, I save it in **~/.ssh/aws/sasadangelo\_keys.pem**. Make sure permissions are 400 with the following command:

_chmod 400 ~/.ssh/aws/sasadangelo\_keys.pem_

![Amazon EC2 Download Keys](assets/img/13-Amazon-EC2-Download-Keys.png){:width="450" height="63" }

Now you can access the Ec2 instance with the following command:

ssh -i _~/.ssh/aws/sasadangelo\_keys.pem ubuntu@19.15.10.10_

The “**\-i”** option tells SSH to use the key to access the EC2 instance instead of a password. The user **ubuntu** is the default user for Ubuntu images. Finally, 19.15.10.10 is the IP address to access the instance. To avoid typing this long command every time, you can add the text in the following image in the _~/.ssh/config_ file.

![Amazon EC2 Configure SSH](assets/img/14-Amazon-EC2-Configure-SSH.png){:width="450" height="105" }

Then you can access the Ec2 instance using the command:

_ssh aws_

### How to access the “Hello World” application via browser

Type in the address bar of your browser the URL **http://19.15.10.10** (in your case use the public IP of your EC2 instance). You should see the following output.

![Hello World Web Application](assets/img/Hello-World-Web-Application.png){:width="450" height="97" }

## Secure your EC2 instance with Security Groups

At whatever moment you can change the Security Group associated with your EC2 instance by selecting the link **Security Groups** in the **Network & Security** section of the left menu.

![Security Groups Menu](assets/img/1-SecurityGroups-Menu.png){:width="450" height="379" }

Select the Security Group you want to change.

![List Security Groups](assets/img/2-List-Security-Groups.png){:width="450" height="131" }

Click on the tabs **Inbound** or **Outbound rules** depending on which rules you want to change. Click then the **Edit Inbound** (or Outbound) **rules**. You can add or remove rules depending on your needs as shown above.

![Edit Security Groups](assets/img/3-Edit-Security-Groups.png){:width="450" height="228" }

## EC2 Launch Template

In the previous article, I talked about the EC2 launch template and why it is important. Let’s see how to create a launch template and use it to create Ec2 instances. From the console search bar, looks for **EC2** and select the link **launch templates**. Click on the **Create launch template** button.

![EC2 LaunchTemplate Home Page](assets/img/EC2-LaunchTemplate-1.png){:width="450" height="297" }

Insert the name of the template and the version.

![EC2 Launch Template Form](assets/img/EC2-LaunchTemplate-2.png){:width="450" height="375" }

Select the Amazon Machine Image (AMI) to use, the instance type (t2.micro for Free Tier), and the key pairs. In this example, we use the Ubuntu Server 20.04 LTS as AMI.

![EC2 Launch Template Data](assets/img/EC2-LaunchTemplate-3.png){:width="450" height="414" }

Choose if you want to deploy the EC2 instance in a VPC or a classic network. Then select a previously created Security Group to use, the one created above with SSH and HTTP incoming traffic. If you want, you can modify the root file system volume by changing its type, size, encryption, and delete on terminate attribute. You can even add more volumes if you need. For this tutorial leave all the defaults.

![EC2 Launch Template Settings](assets/img/EC2-LaunchTemplate-4.png){:width="450" height="357" }

In the **Advanced details** section, insert the script below that will be run during the first boot of the machine. The script installs a web server and publishes a “Hello World” web page. Click the **Create launch template** button to save the template.

![EC2 Launch Template User Data](assets/img/EC2-LaunchTemplate-6.png){:width="450" height="345" }

Click the **View launch template** button, select the template and then select **Actions**\->**Launch instance from template** and then the **Launch instance from template** button.

## Conclusion

In the [previous article](amazon-ec2-for-beginners), we talked about EC2 instances, Security Groups, and Launch Templates. In this article, we saw how to use all these concepts in practice. This will be the starting point for future articles to start playing with the Amazon platform.

\* _Feature image from [https://data-flair.training](https://data-flair.training/blogs/aws-ec2-tutorial/)_