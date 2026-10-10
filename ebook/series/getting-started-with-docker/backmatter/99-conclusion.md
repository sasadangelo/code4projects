# What's Next?

You have reached the end of this book. If you have worked through each chapter,
you now know how to:

- Pull and run containers from Docker Hub
- Explain the difference between containers and virtual machines at a kernel level
- Write Dockerfiles, build custom images, and understand the layer cache
- Create user-defined bridge networks and let containers resolve each other by name
- Persist data with named volumes and bind mounts
- Orchestrate a multi-container application with Docker Compose
- Harden a container image with security best practices

That is a complete, practical foundation. Most day-to-day Docker work does not
require anything beyond what you have learned here.

## Where to Go From Here

### Docker Swarm

Docker Swarm is Docker's built-in clustering and orchestration mode. It lets you
deploy multi-container applications across multiple hosts with a single
`docker stack deploy` command. If you need high availability without the
complexity of Kubernetes, Swarm is the right next step.

### Kubernetes

Kubernetes (K8s) is the industry-standard container orchestrator for large-scale
production deployments. It builds on the same container concepts you now know
and adds automated rollouts, self-healing, horizontal scaling, and much more.
The [Getting Started with Kubernetes](https://www.code4projects.org/getting-started-with-kubernetes/)
series on Code4Projects is a natural continuation.

### CI/CD with Docker and GitHub Actions

Automating the build, test, and push of your images in a CI/CD pipeline is the
next productivity leap. GitHub Actions has first-class Docker support and can
build multi-platform images (arm64 + amd64) with a single workflow file.

### Docker Security (deeper)

This book covered the essentials. For production workloads, the next steps are:
image signing with Docker Content Trust, runtime security with Falco,
network policies, and secrets management with HashiCorp Vault or AWS Secrets Manager.

## Stay in Touch

If this book helped you, consider:

- Subscribing to the **Code4Projects newsletter** on Substack for new articles
  and future ebook releases
- Starring the GitHub repository at
  [github.com/sasadangelo/docker-tutorials](https://github.com/sasadangelo/docker-tutorials)
- Sharing the book with a colleague who is just getting started with containers

Thank you for reading.

— *Salvatore D'Angelo*
\hfill code4projects.org

\vspace{2em}
\begin{center}
\textit{The best way to learn Docker is to use it every day.\\
Start with one container. Build from there.}
\end{center}
