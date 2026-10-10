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

<!-- chapters -->

## A Note on Docker vs Podman

All commands in this book are shown with the `docker` prefix. If you are using
Podman, every command works identically — simply replace `docker` with `podman`,
or set the alias `alias docker=podman` once and never think about it again.

## Source Code and Updates

The examples in this book are maintained on GitHub at
[github.com/sasadangelo/docker-tutorials](https://github.com/sasadangelo/docker-tutorials).

For corrections, suggestions, or feedback, write to **sasadangelo@gmail.com**
or visit [code4projects.org](https://www.code4projects.org).

\newpage
