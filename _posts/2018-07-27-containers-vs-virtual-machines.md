---
layout: post
title: Containers vs Virtual Machines
post_series_id: getting-started-with-docker
slug: containers-vs-virtual-machines
thumbnail: assets/img/virtual-machine-architecture-mini.jpeg
excerpt: If you&#039;re in trouble getting the differences between Containers vs Virtual Machines, this article will explain the pros and cons of both.
categories: Virtualization
---

![Containers vs Virtual Maachines](assets/img/virtual-machine-architecture-mini.jpeg){:width="200" height="211" .responsive_img}

# Containers vs Virtual Machines
_Posted on **{{ page.date | date_to_string }}**_

This is the second article of the [Getting started with Docker](getting-started-with-docker) series. Here I would like to explain my understanding of the differences between **containers** and **virtual machines** (VMs).

## Introduction

When I started working with Docker understanding the main differences between containers and VMs was not an easy task. In the [first article of this series](getting-started-with-docker) I talked a bit about this, in this article, I would like to go deep into the subject and listing pro and cons of the two technologies.

Virtualization can be achieved in two ways:

-   **Full virtualization**, where basically the hypervisor can simulate via software or hardware assisted, enough hardware facilities to run a whole copy of a guest operating system. This is the Virtual Machine approach.
-   **Operating system virtualization**, where operating system facilities are used to create isolated environments, called “containers”, that share the same kernel. This is the Container approach.

### A bit of history

Historically, as server processing power and capacity increased, applications running on bare metal machines weren’t able to exploit the new abundance of resources. Thus, VMs were born, designed by running software on top of physical servers to emulate a particular hardware system.

A hypervisor, or a virtual machine monitor, is software, firmware, or hardware that creates and runs VMs. It’s what sits between the hardware and the virtual machine and is necessary to virtualize the server. History of virtual machines goes back to ’60, you can [find more details here](https://en.wikipedia.org/wiki/Virtual_machine).

![Virtual Machine Architecture](assets/img/virtual-machine-architecture.jpeg){:width="450" height="475" .responsive_img}

_Photo from [http://vitolavecchia.altervista.org](http://vitolavecchia.altervista.org/come-funziona-caratteristiche-del-virtual-machine-monitor-vmm/)_

### The pros and cons

The system on top of which VMs run is called the “host” system, while the systems running in VMs are called “guests”.

VMs introduced the possibilities to run multiple different operating systems on the same host system increasing resource usage by applications. This features improved productivity in all the area where a lot of machines with a different operating system was required.

As a software developer, I experienced a lot of benefits to having a virtualized test environment where it was possible to create and destroy VMs on the fly and make snapshots of VMs at any given point of time.

Here a complete list of pros and cons of the new technology introduced in the computer world.

Pros

-   Use the system resources in a more efficient way by applications.
-   Run multiple different OS on the same host system.
-   Possibility to create and destroy virtual machines on-demand in a few minutes.
-   Make a snapshot of a virtual environment at any point in time.
-   Faster system boot compared to bare metal.

Cons

-   Add overhead in application execution due to the hypervisor.
-   Manage an additional software layer (the Hypervisor).
-   Slower system boot compared to containers.

As Hypervisor technologies improved over time new companies started to appear on the market providing the possibilities to rent one or more machines in the Cloud with specific resources like RAM, disk space, CPU core and so on.

The **Infrastructure as a Service** (IaaS) market was born and companies like Amazon, Microsoft, IBM (Softlayer/Red Hat) and others compete today in this market to provide better infrastructure and let their customers concentrate on their own business.

Today a startup does not need to buy a machine, attach it to the power, configure disks, network cables, operating systems, and middleware. It simply connects to an IaaS provider, registers an account, orders a machine with the required specification (i.e. 4Gb RAM, 1 disk of 250 Gb, 4 core CPUs), pays the bill and it is ready to run his business.

![IaaS](assets/img/iaas.png){:width="450" height="399" .responsive_img}

## Containers

According to a recent [study](https://451research.com/images/Marketing/press_releases/Application-container-market-will-reach-2-7bn-in-2020_final_graphic.pdf) by 451 Research, the adoption of application containers will grow by 40% annually through 2020. Containers are facilitating rapid and agile development like never before.

A Docker **Container** is an isolated environment created on top of the operating system kernel. Usually, it contains a single application and its dependencies that run as it was in a separated environment giving the illusion to be a different machine.

This container is saved in a template called **Image** that allows replicating this environment on whatever host system where Docker runs. For more details about the container definition, read the [first article of this series](getting-started-with-docker).

![Container](assets/img/Container.png){:width="289" height="258" .responsive_img}

But a question still persists on container basics, namely: **how do they differ from virtual machines?** A good starting point to answer this question is to list the pros and cons of the technology, the reason why it was born and use case scenarios where it can be used.

Here a list of the pros and cons of the Container technology.

Pros

-   It is lighter than a virtual machine;
-   the bootstrap is fast;
-   it does not add much overhead when the application runs;
-   it is replicable and avoids the “work on my machine” problem;
-   update an application is easier because it requires only to deploy the new container version and start it.
-   it avoids dependencies problems during application deploy.

Cons

-   it does not simulate a whole guest operating system;
-   works only on Linux host operating system, on Windows and Mac a Linux virtual machine is required to run the containers;
-   difficult to manage when the number of containers increases;
-   security issues if you do not know what you are doing;

Sometimes on the web, we read that containers are a lightweight virtual machine but this definition is wrong. The two concepts are completely different. A virtual machine simulates perfectly a guest operating system inside a host system. It is possible to run a Windows system inside a Linux one and vice versa.

Containers leverage on isolation Linux facilities like Namespaces and Cgroups, which give us the illusion of an isolated environment while it shares the kernel with other containers. Docker to run on Windows and Mac system needs to run a Linux virtual machine where the containers live.

![cgroups and namespaces in docker](assets/img/cgroups-namespaces-docker.png){:width="450" height="107" .responsive_img}

These isolation mechanisms make the containers lightweight and do not add too much overhead to the application execution, the boot is faster than VMs and the environment configuration is replicable. These features opened to new forms of applications, the **containerized applications**.

Containerized applications are easy to deploy because dependencies problems are already solved by the container. The patching is easier than the past because patching a containerized application means simply to deploy the new container and remove the old one.

Maintenance is simplified because you do not need to replicate the customer environment anymore because the container environment is the same everywhere.

Containers fit well in new **Micro Services** architecture where each service can leave in a container,  which exposes the interface via REST APIs and managed by a single Agile team.

Containerized applications are not the only area where the containers can be used. For example, I use containers to unit test my applications on my development machine.

The test team can leverage on containers to simplify the test environments for system, performance and scalability tests.

## The Analogy

Mike Coleman on [Docker official blog](https://blog.docker.com/2016/03/containers-are-not-vms/) provides a good analogy to understand the differences between Containers and VMs:

> The analogy I use (because if you know me, you know I love analogies) is comparing houses (VMs) to apartment buildings (containers).
> 
> Houses (the VMs) are fully self-contained and offer protection from unwanted guests. They also each possess their own infrastructure – plumbing, heating, electrical, etc. Furthermore, in the vast majority of cases houses are all going to have at a minimum a bedroom, living area, bathroom, and kitchen. I’ve yet to ever find a “studio house” – even if I buy the smallest house I may end up buying more than I need because that’s just how houses are built.  (for the pedantic out there, yes I’m ignoring the [new trend in micro-houses](http://tinyhousetalk.com/top-10-shipping-container-tiny-houses/) because they break my analogy)
> 
> Apartments (the containers) also offer protection from unwanted guests, but they are built around shared infrastructure. The apartment building (Docker Host) shares plumbing, heating, electrical, etc. Additionally, apartments are offered in all kinds of different sizes – studio to the multi-bedroom penthouse. You’re only renting exactly what you need. Finally, just like houses, apartments have front doors that lock to keep out unwanted guests.

## Final Toughs

As you understand there is no one size fits all with virtualization technology. Containers and VMs are two different technologies that are useful in different contexts.

VMs are perfect to create virtual environments that can be created and destroyed on demand depending on the workload. Containers are perfect in microservices architecture to create containerized applications or services and to manage their lifecycle.

## What’s Next?

In this article, you learned the differences between containers and VMs. In the [next article](how-to-install-postgresql-on-docker), I’ll show you how to install PostgreSQL on a container.