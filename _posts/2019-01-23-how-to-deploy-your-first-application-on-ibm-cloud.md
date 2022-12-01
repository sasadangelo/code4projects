---
layout: post
title: How to deploy your first application on IBM Cloud
post_series_id: getting-started-with-cloud-computing
slug: how-to-deploy-your-first-application-on-ibm-cloud
thumbnail: assets/img/Tetris_mini.png
excerpt: In this article, I want to show how to deploy your first application on IBM Cloud.
categories: Cloud
---

![How to deploy your first application on IBM Cloud](assets/img/Tetris_mini.png){:width="282" height="200" }

# How to deploy your first application on IBM Cloud
_Posted on **{{ page.date | date_to_string }}**_

This is the third article of the [Getting started with Cloud Computing](getting-started-with-cloud-computing) series. In this article, I want to show how to deploy your first application on IBM Cloud.

How explained in the [previous article](introduction-to-the-ibm-cloud-platform), IBM Cloud allows you to deploy your application written in programming languages like Java, Ruby, Node.js, Javascript, and others.

For this experiment, [I forked a Node.js project](https://github.com/zhongdeliu/multiplayer-tetris) on the Internet and modified it to make it IBM Cloud-ready. To make things funnier I chose a Tetris clone as an example. Here you can download [my version of the game](https://github.com/sasadangelo/multiplayer-tetris).

![Tetris](assets/img/Tetris.png){:width="450" height="395" }

## Introduction to your IBM Cloud workspace

As the first step of this tutorial, you need to create an [IBM Cloud](https://www.ibm.com/cloud/) account. The steps to follow to accomplish this task are very intuitive and I avoid to put a step by step guide here because the web pages changed periodically every month or so.

Before you start you need to understand some basic Cloud Foundry concepts that will help you to feel comfortable when you will start to work with your application.

From your account, you can manage one or more **Organization** that represents your company or the business unit of your company. For each organization, you can have one or more **Space**. You can see a space like development, test, or production environment.

![Organizations and Spaces](assets/img/Org-Spaces.png){:width="450" height="304" }

When you create an account, a default organization will be created with your email address as the name. You can change it if you want. By default, a default space is created called **dev**. You can change it too. In a Space, you can manage resources (i.e. the application) and services.

From the workspace you can click on the **Create Resource** button, select the Runtime Framework **SDK for Node.js**, fill the form with the following values:

-   _application name_: multiplayertetris
-   _hostname_: multiplayertetris

The system automatically will fill the fields Domain, Region, Organization, and Space. Click on the **Create** button. A Start Application (basically a Hello World application) will be deployed and started. It’s time to deploy your application.

## Deploy the application on IBM Cloud with CLI

### How to make your application IBM Cloud-ready

In this section, I will show you how I changed the forked application to make it deployable on IBM Cloud. First of all, I forked the application on my account and clone on my machine with the following commands:

{% highlight shell %}
cd <work_directory>
git clone https://github.com/sasadangelo/multiplayer-tetris
cd multiplayer-tetris
{% endhighlight %}

As a second step, I created a **public** folder and moved all the sources code in it except the package.json file. Then I removed some useless files like **public/bower.json**, **public/db.js**, and **public/Procfile**. The reason I removed these dependencies is to avoid problems with extra dependencies I noticed were not required to play the game.

In the root folder, I added a license and README file and the most important file to deploy the application on IBM Cloud: the **manifest.yml** file. Here the content:

{% highlight yaml %}
applications:
- memory: 64M
  instances: 1
  domain: eu-gb.mybluemix.net
  name: MultiplayerTetris
  host: multiplayertetris
  disk_quota: 1024M
{% endhighlight %}

As you can notice I declared the memory to allocate for the application (64Mb), the number of instances (1), the domain, the application name, disk quota, and the hostname. It’s important that application and host names contain the same value inserted in the previous step.

### How to run the application locally

To test the application on your machine you need to install Node.js from [here](https://nodejs.org/). Then you can do the following steps:

{% highlight shell %}
npm install
npm start
{% endhighlight %}

You can access the application from the browser inserting the following URL in your browser **http://localhost:6003**.

### How to deploy the application on IBM Cloud with CLI

If everything works fine you are ready to deploy the code on IBM Cloud. Before that, you need to download the IBM Cloud CLI and install it. You can read the procedure [here](https://cloud.ibm.com/docs/cli/index.html#overview).

To deploy the application on IBM Cloud using the following commands:

{% highlight plaintext %}
1. bluemix api https://api.<region>.bluemix.net
   where region can be:
       eu-gb, for London datacenter;
       eu-de, for Frankfurt datacenter;
       ng, for Dallas datacenter;
       au-syd, for Sydney datacenter;
       us-east, for Washington datacenter;
2. bluemix login -u <your email> -o <organization> -s <space>
3. bluemix app push MultiplayerTetris
{% endhighlight %}

You can see your application at the URL **https://multiplayertetris.<region>.mybluemix.net**. [Here](https://multiplayertetris.eu-gb.mybluemix.net/) a working demo.

## Deploy the application on IBM Cloud with Eclipse

You can develop your applications with Eclipse and deploy them directly from it. To do that, [you need to download Eclipse Oxygen 3](http://eclipse.bluemix.net/packages/epp.bmt/?cm_mc_uid=86302448733915472421149&cm_mc_sid_50200000=46579901547662801853) that is already bundled with IBM Cloud server called Bluemix Server (Bluemix is the old brand name of IBM Cloud). You can also use Jetbrains IDE (IntelliJ, AndroidStudio, WebStorm, etc.) to develop your applications [and deploy them on IBM Cloud.](https://github.com/IBM-Cloud/ibm-cloud-developer-tools/tree/master/jetbrains)

### How to import the application in Eclipse

When you download the Eclipse Oxygen tar.gz file, extract it and open the Editor. As the first step, you need to install the **nodeclipse** plugin from the Eclipse Marketplace in order to develop the Node.js application. Go on **Help** -> **Eclipse Marketplace**, Search for **nodeclipse,** and install the plugin.

![Nodeclipse](assets/img/Nodeclipse.png){:width="450" height="286" }

Import the project directly from github.com with the following procedure. Right-click on **Project Explorer** and select **File -> Import …**

![Import Project](assets/img/Import-Project-1.png){:width="450" height="644" }

Select **Git -> Project from Git** and click the **Next** button.

![Select Git](assets/img/Select-Git.png){:width="450" height="472" }

Select **Clone URI** and click the **Next** button.

![Select Repository Source](assets/img/Select-Repository-Source.png){:width="450" height="471" }

On the next page, insert the URL **https://github.com/sasadangelo/multiplayer-tetris** and click **Next**.

![Source Git Repository](assets/img/Source-Git-Repository.png){:width="450" height="470" }

Select the **master** branch and click **Next** again.

![Master Branch Selection](assets/img/Branch-Selection.png){:width="450" height="471" }

Insert the folder of your workspace and click **Next**. Select the option **Import using the New Project wizard** and then **Finish**, in this way you can create a Node.js project.

![Import NodeJS Project](assets/img/Import-NodeJS-Project.png){:width="450" height="471" }

Select **Node -> Node.js Project** and click **Next**.

![Select Node Project](assets/img/Select-Wizard.png){:width="450" height="429" }

Insert the project name and click **Finish**.

![Create Node.js Project](assets/img/Create-NodeJS-Project.png){:width="450" height="426" }

### How to run the application locally with Eclipse

Right-click on the multiplayer-tetris project and select **Run as -> npm install** to install locally all the dependencies.

![Install Dependencies](assets/img/Install_Dependencies.png){:width="450" height="410" }

Right-click again on the multiplayer-tetris project and select **Run as ->** **Run Configuration …**

![Run Configurations](assets/img/Run_Configuration.png){:width="450" height="325" }

Select the **Node.js application** and press on the New button to create a new configuration for this application.

![Node.js Application](assets/img/Node.js_Application.png){:width="450" height="361" }

Select the project and its main file (app.js) and click Run. Open your browser and insert in the address bar the address **http://localhost:6003**.

### How to deploy the application on IBM Cloud with Eclipse

Right-click on the multiplayer-tetris project and select **Run as -> Run on Server**.

![Run on Server](assets/img/Run_on_Server.png){:width="450" height="258" }

Select **IBM -> IBM Bluemix** and click the **Next** button.

![Run on Bluemix](assets/img/Run_on_Bluemix.png){:width="450" height="448" }

Insert the email address and password of your account and select the region where your workspace is deployed and click on the **Next** button.

![Insert Cloud Credentials](assets/img/Insert_Cloud_Credentials.png){:width="450" height="364" }

Select your Space and click on the **Next** button.

![Select Organization and Space](assets/img/Select_Organization_Space.png){:width="450" height="200" }

Move the **mutiplayer-tetris** project on the right and click the **Finish** button.

![Add to Workspace](assets/img/Add_to_Workspace.png){:width="450" height="226" }

At the end of the deploy, you can access the application via URL **https://multiplayer-tetris.<region>.bluemix.net**.

## What happens behind the scene?

When we deploy our application via CLI or Eclipse, **what happens behind the scene?** An answer to this question is really important because it allows us to understand internals on how Cloud Foundry works. When we deploy an application on IBM Cloud Foundry executes a push operation and internally the following steps occur.

![Cloud Foundry App Push](assets/img/app_push_flow_diagram_diego.png){:width="450" height="259" }

In the [previous article](introduction-to-the-ibm-cloud-platform), I showed the Cloud Foundry architecture and in this diagram, we can see how the different components interact during a CF PUSH command. When the developer deploys an application via cf push command, the request arrives at the go router that routes it to the Cloud Controller (CC), the brain of Cloud Foundry. Application metadata are stored in the Cloud Controller Database (CCDB). Application files are uploaded on a blob store. A Diego cell is staged where will be the runtime framework (i.e. java, node.js, ruby, ecc.) to run the application. The developer can visualize the staging output to check the result. Once the staging phase is completed, the application is started.