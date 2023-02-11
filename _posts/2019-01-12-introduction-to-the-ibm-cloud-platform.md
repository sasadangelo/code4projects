---
layout: post
title: Introduction to the IBM Cloud platform
post_series_id: getting-started-with-cloud-computing
slug: introduction-to-the-ibm-cloud-platform
image: /wp-content/uploads/2019/01/IBM-Cloud.png
excerpt: "In this article, I would like to go into the details of Cloud Computing analyzing one of the most important platforms on the market: IBM Cloud."
categories: Cloud
---

![Introduction to the IBM Cloud platform]({{ site.baseurl }}/wp-content/uploads/2019/01/IBM-Cloud.png){:width="327" height="200" .responsive_img}

# Introduction to the IBM Cloud platform
_Posted on **{{ page.date | date_to_string }}**_

In the [previous article,]({{ site.baseurl }}/getting-started-with-cloud-computing/) we talked about Cloud Computing in very general terms. In this article, I would like to go into the details of Cloud Computing to understand how the theoretical concepts apply in practice. The platform I chose for this analysis is [IBM Cloud](https://www.ibm.com/cloud/).  

IBM Cloud is the IBM cloud computing platform that combines Infrastructure as a service  (IaaS), platform as a service (PaaS), container as a service (CaaS), and Function as a Service (FaaS). Additionally, it has a rich catalog of over 170 services that can be easily integrated with PaaS and IaaS to build business applications rapidly.

IBM cloud platform is built on open source technology like Cloud Foundry, Kubernetes, Open Whisk, and others. Its goal is to simplify the delivery of an application by providing hosting capabilities and services that are ready for immediate use.

## IBM Cloud Service Models

The IBM Cloud offering provides five ways to use its platform.

1.  Bare metal server (IaaS).
2.  Virtual server (IaaS).
3.  Container Orchestration with Docker and Kubernetes (CaaS).
4.  Cloud Foundry (PaaS).
5.  Open Whisk (FaaS).

![IBM Cloud Service Models]({{ site.baseurl }}/wp-content/uploads/2019/01/IBM-Cloud-Service-Models.png){:width="450" height="186" .responsive_img}

### Bare metal and virtual servers (IaaS)

With the acquisition of Softlayer in 2013, IBM was able to equip its Cloud with a powerful platform for provisioning bare metal and virtual machines.

Today, by connecting to the IBM Cloud platform, you can order a single-tenant bare metal machine in the appropriate geographic region in just a few clicks. IBM bare metal servers offer performance, flexibility, on-demand provisioning, and control. You will be able to customize its configuration by setting RAM, storage, data center, cores, and much more.

If your workload does not require the potential of a bare metal machine or is very variable then you can opt for a virtual machine. IBM virtual servers can be deployed in minutes from the virtual server images of your choice in the appropriate geographic region. As your workloads drop, you can suspend or shut down these virtual servers so your cloud environment matches your infrastructure needs perfectly. Offered in single or multi-tenant distributions, virtual servers are not subscribed unless indicated to meet all workload requirements. Also for these servers, you can order them specifying vCPUs, RAM, networking, storage, data centers and much more.

### Container Orchestration with Docker and Kubernetes (CaaS)

IBM Cloud Kubernetes Service creates a cluster or host and deploys highly available containers. A Kubernetes cluster lets you securely manage the resources that you need to quickly deploy, update, and scale applications.

Use the tools and APIs you already know for a single, consistent experience, even when working across different cloud infrastructures.

Container infrastructure allows you to easily integrate your application with cognitive solutions through a variety of Watson APIs. IBM provides security features to protect your cluster infrastructure, isolate your resources, and ensure security compliance in your container deployments. You can configure the Kubernetes cluster that auto-scales and recovers containers based on defined policies. Use the built-in logging and metrics service to monitor the performance of both your clusters and containers. Moreover, Kubernetes automatically deploys containers on hosts according to the available resources across the cluster.

### Cloud Foundry (PaaS)

[Cloud Foundry](https://www.cloudfoundry.org/) is an open source PaaS that allows you to build your own application easily thanks to a wide range of available services (i.e. SQL and NoSQL databases, cognitive, blockchain, and others) and framework (i.e. Node.js, Java, PHP, Python, and others). It interfaces easily with a wide range of Cloud systems in different deployment models.

![CloudFoundry Services, Runtimes, and Clouds]({{ site.baseurl }}/wp-content/uploads/2019/01/Cloud-Foundry-Services-Runtime-Cloud.png){:width="450" height="323" .responsive_img}

IBM formerly built its Public Cloud around Cloud Foundry adding software like a web UI console, a billing system, an extended command line, services (i.e cognitive, blockchain, and other).

The following figure shows the Cloud Foundry architecture.

![CloudFoundry Architecture]({{ site.baseurl }}/wp-content/uploads/2019/01/CloudFoundry-Architecture.png){:width="450" height="299" .responsive_img}

Whenever a request comes from IBM Cloud web UI or command line the Router routes it to a Cloud Controller that is the Cloud Foundry brain.

When a push command (push is the command that allows publishing application in the cloud system) arrives, a Garden container is allocated into a Diego cell (that is basically the virtual machine managed by Diego) and the application is deployed in it. The user will no have the perception of where these resources are, everything it’s transparent. The system that manages virtualization is called Diego and Diego Brain is the component that takes controls of it.

All runtime framework blobs are stored in the Blobstore component. If a customer chooses to create a Java application, the Java runtime blob is retrieved from Blobstore and installed in the Garden container.

### IBM Cloud Functions (FaaS)

IBM Cloud Functions (based on Apache OpenWhisk) is a Function-as-a-Service (FaaS) platform that performs functions in response to incoming events and costs nothing when not used.

Functions as a Service (FaaS) enables developers to create and run event-driven apps that scale on demand. Based on the Apache OpenWhisk Project, which provides a core underlying code base for building and deploying FaaS applications. With FaaS, team members can build apps more quickly by working on different pieces of code simultaneously, freed from the concerns around scale and infrastructure.

IBM in its Cloud offering includes some SaaS applications whose portfolio is available [here](https://www.ibm.com/cloud/saas).

## IBM Cloud Deployment Models

IBM Cloud supports four types of deployment:

1.  Public
2.  IBM Cloud Foundry Enterprise Environment
3.  Dedicated
4.  On-Premise

With the **Public IBM Cloud** platform, you can manage with a few clicks from a bare metal server up to serverless applications. You can write your application in several programming languages (i.e. Java, Node.sj, Javascript, Ruby, etc.) and combine it with over 170 services like cognitive, databases, blockchain and much more.

**IBM Cloud Foundry Enterprise Environment** is a single-tenant environment that can be rapidly self-provisioned in the Public IBM Cloud through the public console. It allows you to use the power of Cloud Foundry to manage your enterprise. It has options for hardware isolation and can access IBM Cloud’s full catalog of over 170 services, including the amazing Watson and IoT offerings.

**IBM Cloud Dedicated** is a single-tenant cloud platform for building, running and managing your cloud applications. With IBM Cloud Dedicated, you get the power and simplicity of IBM Cloud in your own isolated infrastructure environment that is securely connected to both the IBM Cloud public environment and your own network. IBM Cloud Dedicated comes with the same set of Cloud Foundry runtimes available in IBM Cloud public and recently IBM Cloud Kubernetes Service joined the offering.

**IBM Cloud on-Premise** is a Cloud Foundry platform that runs in customer data center alongside the core IBM Cloud Private Kubernetes offering.

## What’s Next?

In the next article, we will see how to use a Cloud platform in practice deploying a simple application. To do this, I modify an open source application to make it IBM Cloud ready and how to publish it.