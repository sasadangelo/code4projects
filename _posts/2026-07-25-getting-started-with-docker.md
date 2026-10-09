---
layout: post
author: sasadangelo
title: "Getting Started with Docker and Podman"
post_series_id: getting-started-with-docker-2025
slug: getting-started-with-docker-2025
image: /assets/img/docker-getting-started.svg
excerpt: Learn what Docker is, understand containers and images, and run your first containerized web server with Docker or Podman — no setup complexity required.
categories:
  - Virtualization
---

![Getting Started with Docker and Podman]({{ site.baseurl }}/assets/img/docker-getting-started.svg){:width="760" height="400" .responsive_img}

## Introduction

This is the first article of the **Getting Started with Docker** series. By the end of this article you will understand what Docker is, what problems it solves, and you will have your first containerized web server running on your machine in minutes — without writing a single line of Dockerfile.

You should read this article if:

- You have heard of Docker but never used it
- You want a practical, no-nonsense introduction that gets you running immediately
- You are on a machine where Docker Desktop is not available and you need an alternative (Podman)

All the commands shown here work identically with both **Docker** and **Podman**. Where there are differences, they are explicitly noted.

## Why Docker?

Before diving into commands, it is worth spending a minute on the problem Docker actually solves.

Imagine you are a developer. You write an application on your laptop, it works perfectly. Then you hand it off to a colleague or deploy it to a server — and it breaks. Different OS version, different library installed, different path. This is the classic **"it works on my machine"** problem, and it has tormented developers for decades.

Docker solves this by packaging your application together with everything it needs to run — runtime, libraries, configuration — into a single portable unit called a **container**. That container runs identically on your laptop, your colleague's machine, and the production server.

This matters not just for individual developers. Modern applications are built as dozens (sometimes hundreds) of independent services — **microservices** — each with its own dependencies. Docker makes it possible to deploy, update, and scale each service independently, without interference.

## Docker vs Podman: Which One Should You Use?

Both Docker and Podman are tools for running containers. For everything covered in this series, they are interchangeable — the CLI commands are identical.

The key differences:

| | Docker | Podman |
|---|---|---|
| **Architecture** | Requires a background daemon (`dockerd`) | Daemonless — runs containers directly |
| **Privileges** | Daemon runs as root | Rootless by default — more secure |
| **License** | Docker Desktop requires a paid license for enterprise use | Fully open source (Apache 2.0) |
| **Installation on Mac** | Docker Desktop | `brew install podman` + `podman machine init` |
| **Compose support** | `docker compose` (v2 plugin) | `podman compose` (from Podman 4.7+) |
| **OCI compatibility** | Yes | Yes — same image format |

**In short**: if Docker Desktop is available and licensed for your use, use Docker. If you are on a corporate machine where Docker Desktop requires a commercial license, or if you prefer an open source rootless alternative, use Podman. The rest of this series works exactly the same either way.

> Throughout this series, all commands are shown with `docker`. If you are using Podman, simply replace `docker` with `podman` — or set the alias `alias docker=podman` once and forget about it.

## Installing Docker or Podman

### Docker

On Linux, install Docker Engine following the [official documentation](https://docs.docker.com/engine/install/). On Mac and Windows, Docker Desktop is the easiest option if your license allows it: download it from [docs.docker.com/desktop](https://docs.docker.com/desktop/).

### Podman (Mac)

On macOS, Podman uses a lightweight Linux virtual machine behind the scenes — the same approach Docker Desktop uses. Install and initialise it with three commands:

```shell
brew install podman
podman machine init
podman machine start
```

After this, `podman` is ready and behaves exactly like `docker`.

## Core Concepts: Images and Containers

Before running anything, two concepts are essential.

### Docker Image

A **Docker image** is a read-only, layered package that contains everything needed to run a specific application: the OS filesystem, runtime, libraries, configuration files, and the application itself.

Images are stored in registries. The most popular is [Docker Hub](https://hub.docker.com), which hosts thousands of official and community images. When you run a container, Docker (or Podman) downloads the image from the registry if it is not already present on your machine.

Images are built in **layers**. Each instruction that modifies the filesystem adds a layer on top of the previous ones. Layers are cached and shared between images — this is what keeps images small and builds fast.

### Docker Container

A **container** is a running instance of an image. You can think of the image as a class and the container as an object instantiated from it. Multiple containers can run from the same image simultaneously, each fully isolated from the others.

Containers share the host OS kernel but are isolated from each other using Linux kernel features: **namespaces** (for process, network, filesystem isolation) and **cgroups** (for resource limits like CPU and memory).

This is the fundamental difference from a Virtual Machine: a VM emulates an entire hardware stack and runs a separate OS kernel. A container shares the host kernel and is much lighter as a result.

![Container vs VM]({{ site.baseurl }}/assets/img/docker-logo.webp){:width="450" height="200" .responsive_img}

We will explore this topic in depth in the [next article]({{ site.baseurl }}/containers-vs-virtual-machines-2025/).

## Essential Commands

Here is the minimal set of commands you need to start working with Docker. These are the ones you will use every day.

### List local images

```shell
docker image ls
```

At the beginning, the list is empty.

### Pull an image from Docker Hub

```shell
docker pull nginx:alpine
```

This downloads the official Nginx image based on Alpine Linux — a very small (~40 MB) but fully functional web server image.

### Run a container

```shell
docker run -d -p 8080:80 --name my-nginx nginx:alpine
```

Breaking down the options:

- `-d` — runs the container in detached mode (in the background, shell does not hang)
- `-p 8080:80` — maps port 8080 on your host to port 80 inside the container
- `--name my-nginx` — gives the container a friendly name instead of a random one
- `nginx:alpine` — the image to use

Open your browser at `http://localhost:8080` and you will see the Nginx welcome page. You just ran a web server without installing anything on your machine.

### List running containers

```shell
docker container ls
```

To see all containers including stopped ones:

```shell
docker container ls -a
```

### View container logs

```shell
docker logs my-nginx
```

### Execute a command inside a running container

```shell
docker exec -it my-nginx /bin/sh
```

The `-it` flags attach an interactive terminal. Note: Alpine-based images use `sh` instead of `bash`.

### Stop and remove a container

```shell
docker stop my-nginx
docker rm my-nginx
```

Or in one command:

```shell
docker rm -f my-nginx
```

### Remove an image

```shell
docker image rm nginx:alpine
```

### Clean up everything unused

```shell
docker system prune
```

This removes all stopped containers, dangling images, and unused networks. Add `-a` to also remove unused images that are not referenced by any container.

## Your First Containerized Application

Let us put it all together with a practical example. You will serve a custom HTML page through Nginx — without installing Nginx, without a Dockerfile, using only the official image and a single `docker run` command.

Create a file called `index.html` anywhere on your machine:

```html
<!DOCTYPE html>
<html>
  <head><title>Hello from Docker</title></head>
  <body>
    <h1>Hello, World!</h1>
    <p>This page is served by Nginx running inside a container.</p>
  </body>
</html>
```

Now run Nginx and mount that file into the container:

```shell
docker run -d \
  -p 8080:80 \
  --name hello-nginx \
  -v $(pwd)/index.html:/usr/share/nginx/html/index.html:ro \
  nginx:alpine
```

The `-v` option **bind mounts** your local file into the container's web root. The `:ro` suffix makes the mount read-only inside the container (a good practice).

Open `http://localhost:8080` in your browser:

> **Hello, World!**
> This page is served by Nginx running inside a container.

You served a custom page without installing a web server, without writing a Dockerfile, and without touching your system configuration. When you are done:

```shell
docker rm -f hello-nginx
```

Your machine is exactly as it was before. Nothing installed, nothing left behind.

## How This Series Is Structured

This first article introduced the core concepts and got you running immediately. In the upcoming articles we will progressively build on this foundation:

- **Containers vs Virtual Machines** — deep dive into isolation mechanisms, namespaces, cgroups, and the difference from hypervisor-based virtualization
- **Dockerfile & Building Custom Images** — write your own `Dockerfile`, build and tag a custom image, understand the layer cache
- **How Docker Networking Works** — user-defined bridge networks, automatic DNS resolution between containers, network isolation
- **How Docker Volumes Work** — named volumes vs bind mounts, persisting data across container restarts
- **How Docker Compose Works** — manage multi-container applications with a single `docker compose up`
- **Docker Security Best Practices** — run containers as non-root, drop capabilities, scan images for vulnerabilities

Each article builds on the previous one around the same practical Nginx application, adding one concept at a time.

## Conclusion

In this article we covered:

- The problem Docker solves and why containers matter
- The difference between Docker and Podman, and when to use each
- The two fundamental concepts: **images** and **containers**
- The essential CLI commands for daily use
- Running a custom web page with Nginx using only the official image

The [next article]({{ site.baseurl }}/containers-vs-virtual-machines-2025/) goes deeper into the conceptual foundations: what actually makes a container different from a virtual machine, and what Linux kernel mechanisms make it all work.
