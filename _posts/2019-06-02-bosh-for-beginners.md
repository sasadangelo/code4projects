---
layout: post
title: BOSH for Beginners
slug: bosh-for-beginners
thumbnail: assets/img/bosh_logo.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories:
- Cloud
- DevOps
---

![BOSH for Beginners](assets/img/bosh_logo.png){:width="393" height="200" }

# BOSH for Beginners
_Posted on **{{ page.date | date_to_string }}**_

In this article, I want to explain what Bosh is, its main concepts, and how to use it practically to deploy software.

## What is BOSH?

According to Bosh official documentation:

> BOSH allows individual developers and teams to easily version, package and deploy software in a reproducible manner.
> 
> Any software, whether it is a simple static site or a complex multi-component service, will need to be updated and repackaged at some point. This updated software might need to be deployed to a cluster, or it might need to be packaged for end-users to deploy to their own servers. In a lot of cases, the developers who produced the software will be deploying it to their own production environment. Usually, a team will use a staging, development, or demo environment that is similarly configured to their production environment to verify that updates run as expected. These staging environments are often taxing to build and administer. Maintaining consistency between multiple environments is often painful to manage.

BOSH was originally developed by Cloud Foundry Foundation to manage the deployment of [Cloud Foundry](https://www.cloudfoundry.org/), an open-source platform as a service (PaaS) software. The goal of Cloud Foundry developers was to have a tool to create, test, and deploy the different pieces of the software (microservices) and help the site reliability engineers (SREs) to easily maintain it.

Software deployment requires to address a lot of different items like:

-   software packaging and versioning
-   deploying and upgrade software reproducibly
-   deploying software in a distributed way

Many tools like Chef, Puppet, Docker exist that address one or more of these items. BOSH was designed to do each of these as a whole. It was purposefully constructed to address the four principles of modern [Release Engineering](https://en.wikipedia.org/wiki/Release_engineering).

## BOSH Main Components

The following figure shows the Bosh main components. An administrator can manage Bosh environments using a Bosh Cli that sends commands to the Bosh Director that is a server that keeps track of all the deployment aspects.

![Bosh Architecture](assets/img/bosh-architecture.png)  
_Figure from [https://bosh.io](https://bosh.io/docs/bosh-components/)_

Internally, there is a CPI that is an API that the Director uses to manage IaaS components like VM, storage, network, and so on. Bosh support different IaaS systems (i.e. Softlayer, AWS, Virtual Box, Google Cloud Platform, and so on) and to interact with them he needs the CPI specific for each Cloud provider.

VM that lives in the IaaS environment includes a Bosh Agent that interacts with the Director to manage the software deployment on it. They communicate through a message system based on a publisher-subscriber approach (NATS).

![Bosh Internals](assets/img/bosh-internals-e1594368084446.png)  
_Figure from [http://www.think-foundry.com](http://www.think-foundry.com/cloud-foundry-bosh-introduction/)_

When an administrator sends commands to the Director via Bosh CLI a task is created that is inserted in the Task Queue managed by the Director. Other tasks can be scheduled by the Director itself to manage the infrastructure. These tasks are managed by a pool of workers.

Health Monitor component is used to check periodically the status of different VMs. It communicates with Bosh Agent via heartbeat and if it is unresponsive for a specific period of time the VM is considered not live.

## BOSH Main Concepts

Bosh administrator can administer multiple Cloud environments using a single Bosh CLI. The first concept to understand is the **Environment** that is the Cloud scope where software deployment occurs. Bosh can manage one or more environments.

In each environment, you can have one or more **Deployments**. A Bosh deployment has four main concepts: Manifest, Release, Stemcell, and Instance.

-   **Manifest**: describes how to combine Releases, Stem cells, and Instances to create a deployment.
-   **Release**: A release is a versioned collection of configuration properties, configuration templates, startup scripts, source code, binary artifacts, and anything else required to build and deploy software in a reproducible way.
-   **Stem cell**: A stem cell is a versioned Operating System image wrapped with IaaS specific packaging. A typical stem cell contains a bare minimum OS skeleton with a few common utilities pre-installed, a BOSH Agent, and a few configuration files to securely configure the OS by default.
-   **Instance (VM)**: A deployment is made up of instances. Normally, instances represent long-running servers on your cloud infrastructure. They can also represent “errands” – one-off tasks that can be run inside of temporary servers.

![Bosh Deployment](assets/img/bosh-deployment-1.png)

A Release is deployable on different instances, for example, a PostgreSQL server and CLI could be installed on two separate instances. To manage this distributed deployment method each Bosh Release has one or more jobs. A job contains:

-   configuration metadata
-   ERB configuration file
-   Monit file
-   starts/stop and hooks scripts

and it can be deployed on a specified instance. A Job has one or more template files and one or more packages. A package could be the source code or dependencies.

## BOSH Lite install

Bosh Lite is a Bosh you can install on your local machine to get familiar with the tool. It has a local Director and it uses a Bosh CLI to administer it. You can install the Bosh CLI using the following [procedure](https://bosh.io/docs/cli-v2-install/). To install the Director you need to install [Virtual Box](https://www.virtualbox.org/wiki/Downloads) as a prerequisite and then follow this [procedure](https://bosh.io/docs/bosh-lite/).

In the Director install procedure, there is a step to set the BOSH\_CLIENT and BOSH\_CLIENT\_SECRET environment variable. To avoid running them whenever you start a new terminal I suggest you put them in the _.bash\_profile_.

## BOSH commands cheatsheet

When I start to play with a technology I try to find the minimum set of commands that help me to manage the majority of my activity with it. For this reason, I think that building a personal cheatsheet is the best approach to learn new technology.

Once you installed Bosh Lite you can see that it has a single environment called _vbox_ with the following command:

{% highlight shell %}
bosh envs
{% endhighlight %}

To see all the deployments in the vbox environment you can use the following command:

{% highlight shell %}
bosh -e vbox deployments
{% endhighlight %}

To avoid to specify every time the environment you can set the BOSH\_ENVIRONMENT variable in  
you _.bash\_profile_:

{% highlight shell %}
export BOSH_ENVIRONMENT=vbox
{% endhighlight %}

From this moment on I assume you did it so I don’t specify the -e option anymore. When you list your deployment you can notice that initially, it is empty.

As a first step, we can upload on the Director the stem cell to use for our deployment. BOSH produces official [stemcells](https://bosh.io/stemcells/) for popular operating systems and infrastructures. For example, for Ubuntu 16 Xenial we can use the latest version of the [following one](https://bosh.io/stemcells/bosh-warden-boshlite-ubuntu-xenial-go_agent). Here the command to upload it on the Director:

{% highlight shell %}
bosh upload-stemcell --sha1 632b2fd291daa6f597ff6697139db22fb554204c https://bosh.io/d/stemcells/bosh-warden-boshlite-ubuntu-xenial-go_agent?v=315.13
{% endhighlight %}

List the uploaded stemcell with the command:

{% highlight shell %}
bosh stemcells
{% endhighlight %}

The next step is to upload the release we want to deploy. For this tutorial, I created a simple Release containing an HTTP server that when contacted by a browser returns the “Hello World” message. You can [download the package from here](https://github.com/sasadangelo/simple-bosh-release/archive/master.zip). Uncompress it in the folder _<workdir>._

Here the commands to create and upload the release:

{% highlight shell %}
cd <workdir>/simple-bosh-release
bosh create-release --force
bosh upload-release
{% endhighlight %}

You can list the uploaded release with the command:

{% highlight shell %}
bosh releases
{% endhighlight %}

The last step is to create a VM instance starting from the uploaded stemcell and deploy the release on it. You can do it with the following command:

{% highlight shell %}
bosh -d simple-bosh-release deploy deployments/manifest.yml
{% endhighlight %}

To list the VMs created by Bosh during the deployment you can use the following command:

{% highlight shell %}
bosh vms
{% endhighlight %}

Your HTTP server is now running on 10.243.1.2 address, however, you cannot access to it from your machine unless you do not redirect all the traffic to this IP to the Virtual Machine containing the Director 192.168.50.6.

You can do it with the following commands:

{% highlight shell %}
sudo route add -net 10.244.0.0/16     192.168.50.6 # Mac OS X
sudo ip route add   10.244.0.0/16 via 192.168.50.6 # Linux (using iproute2 suite)
sudo route add -net 10.244.0.0/16 gw  192.168.50.6 # Linux (using DEPRECATED route command)
route add           10.244.0.0/16     192.168.50.6 # Windows
{% endhighlight %}

Open your browser and insert the following IP 10.243.1.2 in the address bar. The “**Hello World!**” message will appear.

To clean up the artifact you uploaded on Bosh you first need to delete the deployment with the command:

{% highlight shell %}
bosh -d simple-bosh-release delete-deployment
{% endhighlight %}

Now you can delete the release with the command:

{% highlight shell %}
bosh delete-release simple-bosh-release
{% endhighlight %}

Finally, you can delete the stem cell with the command:

{% highlight shell %}
bosh delete-stemcell <stemcell name>/<stemcell version>
{% endhighlight %}

Obviously, this is the first set of commands you will use with Bosh, however, there are other useful commands to manage tasks, blob, disk, networking, and much more. You can see a complete list [here](https://gist.github.com/bgandon/6b0826189b8513624e98475bc2f9a538).

## How to create a Bosh release

In the previous paragraph, we played with Bosh commands using the **simple-bosh-release** project as an example of release. The question now is: **how I built it?**

[Simple Bosh Release](https://github.com/sasadangelo/simple-bosh-release) is a project I forked from [here](https://github.com/georgethebeatle/simple-bosh-release) and modified to support Bosh v2, Ubuntu 16 Xenial, and Apache 2.4.39. You can follow, step by step, the instructions to build it [reading the home page of the project](https://github.com/sasadangelo/simple-bosh-release).

## **Final thoughts**

I hope this article, helped you to have a good overview of Bosh’s main concepts and how to use it to deploy software. If you work with Cloud Foundry it is a must-have technology. It can be used in all the situation where it is required to manage the whole application lifecycle and infrastructure. Bosh integrates well with a lot of Cloud providers. To complete your skills on Bosh I suggest you read the [official documentation](https://bosh.io/docs/update-cloud-config/) and good tutorials like [this one](https://ultimateguidetobosh.com/).