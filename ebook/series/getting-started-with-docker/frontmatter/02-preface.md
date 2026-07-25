# Preface

I started working with Docker in 2018 when containers were already gaining momentum
but most tutorials either assumed too much prior knowledge or buried the practical
steps under layers of theory.

This book is what I wish I had back then.

It is a no-nonsense, hands-on introduction to Docker and Podman. Every chapter
introduces one concept and immediately applies it with a concrete example. By the
time you finish the last chapter, you will have built, networked, persisted, orchestrated,
and secured a real multi-container application — step by step, command by command.

## Who This Book Is For

This book is for developers who:

- Have heard of Docker but have never used it in practice
- Want to understand the fundamentals before jumping into Kubernetes
- Work on a corporate machine where Docker Desktop requires a paid license and need
  a free alternative (Podman)
- Want a single, coherent reference instead of scattered blog posts

No prior knowledge of containers or virtualization is assumed. Basic familiarity
with the command line is all you need.

## How This Book Is Structured

Each chapter of this book corresponds to a foundational Docker concept, introduced
in a deliberate order so that each one builds on the previous:

1. **Getting Started with Docker and Podman** — first contact, core concepts,
   essential commands, your first running container.
2. **Containers vs Virtual Machines** — how containers actually work under the hood,
   what Linux namespaces and cgroups are, and when to use VMs instead.
3. **Dockerfile and Building Custom Images** — write your own Dockerfile, understand
   the layer cache, build and tag images.
4. **How Docker Networking Works** — connect containers so they can talk to each other,
   automatic DNS resolution, network drivers.
5. **How Docker Volumes Work** — separate data from code, persist state across
   container restarts and replacements.
6. **How Docker Compose Works** — manage a multi-container application with a single
   YAML file and a single command.
7. **Docker Security Best Practices** — run containers safely: non-root users,
   read-only filesystems, capability limits, vulnerability scanning.

## A Note on Docker vs Podman

All commands in this book are shown with the `docker` prefix. If you are using
Podman, every command works identically — simply replace `docker` with `podman`,
or set the alias `alias docker=podman` once and never think about it again.

## Source Code and Updates

The examples in this book are maintained on GitHub at
[github.com/sasadangelo/docker-tutorials](https://github.com/sasadangelo/docker-tutorials).

For corrections, suggestions, or feedback, write to **sasadangelo@gmail.com**
or visit [code4projects.com](https://sasadangelo.github.io/code4projects).

\newpage
