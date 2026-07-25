---
layout: post
title: "Docker Security Best Practices"
post_series_id: getting-started-with-docker-2025
slug: docker-security-best-practices
image: /assets/img/docker-security.svg
excerpt: Learn how to run Docker containers securely — non-root users, read-only filesystems, capability limits, secret management, and image vulnerability scanning.
categories:
  - Virtualization
---

# Docker Security Best Practices
_Posted on **{{ page.date | date_to_string }}**_

![Docker Security Best Practices]({{ site.baseurl }}/assets/img/docker-security.svg){:width="760" height="400" .responsive_img}

## Introduction

This is the seventh and final article of the **Getting Started with Docker** series. In the [previous article]({{ site.baseurl }}/how-docker-compose-works-2025/) we orchestrated a multi-container application with Docker Compose. Now we turn our attention to **security**.

Containers are isolated — but isolation is not the same as security. A container running as root, with a writable filesystem and full Linux capabilities, is a significant risk if it is ever compromised. The good news is that Docker provides several mechanisms to reduce the attack surface, and most of them require only a few lines of configuration.

![Docker security best practices overview]({{ site.baseurl }}/assets/img/docker-security.svg){:width="760" height="400" .responsive_img}

## 1. Never Run as Root

By default, processes inside a container run as **root** (UID 0). This means that if an attacker exploits a vulnerability in your application, they have root access inside the container — and depending on how the container is configured, they may be able to escape to the host.

The fix is simple: add a `USER` instruction to your Dockerfile.

```dockerfile
FROM nginx:alpine

COPY html /usr/share/nginx/html

# Switch to the non-root user that the nginx image already provides
USER nginx

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

The official `nginx:alpine` image already includes a non-root `nginx` user. For your own images, create a dedicated user:

```dockerfile
FROM alpine:3.20

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --chown=appuser:appgroup app /app

USER appuser

CMD ["/app/start.sh"]
```

The `--chown` flag in `COPY` ensures the files are owned by the correct user from the start.

You can also enforce non-root at runtime without changing the Dockerfile:

```shell
docker run --user 1001:1001 nginx:alpine
```

## 2. Use a Read-Only Filesystem

If your application does not need to write to its own filesystem, make it read-only:

```shell
docker run --read-only -p 8080:80 nginx:alpine
```

If the application needs to write to specific paths (temp files, logs), mount those paths as `tmpfs`:

```shell
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/cache/nginx \
  --tmpfs /var/run \
  -p 8080:80 \
  nginx:alpine
```

A read-only filesystem means that even if an attacker gains code execution inside the container, they cannot modify the application binaries or install tools.

In Docker Compose:

```yaml
services:
  frontend:
    image: nginx:alpine
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
      - /var/run
```

## 3. Drop Linux Capabilities

Linux capabilities are fine-grained divisions of root privileges. By default, Docker grants a container a subset of them. You can drop all capabilities and add back only what your application actually needs:

```shell
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx:alpine
```

`NET_BIND_SERVICE` allows binding to ports below 1024 (like port 80). Most application containers do not need any other capability.

In Docker Compose:

```yaml
services:
  frontend:
    image: nginx:alpine
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

## 4. Never Put Secrets in Environment Variables (or Images)

A common mistake is passing passwords or API keys through environment variables in `docker-compose.yml` or baking them into the image with `ENV`. Both approaches expose secrets in `docker inspect` output and in image layers.

**What to do instead**:

- Use **Docker secrets** (available in Swarm mode) which mount secrets as files in `/run/secrets/`
- Use a **secrets manager** (HashiCorp Vault, AWS Secrets Manager, etc.)
- As a minimum, use a `.env` file that is **never committed to version control** and reference it in Compose

```yaml
# docker-compose.yml
services:
  app:
    image: my-app
    env_file:
      - .env.secrets   # never committed to git
```

Add to `.gitignore`:
```
.env
.env.secrets
*.env
```

## 5. Use Minimal Base Images

Every package in your base image is a potential attack surface. Prefer minimal base images:

- `alpine` — ~5MB, very popular, uses musl libc
- `distroless` (Google) — no shell, no package manager, only the runtime and your app
- `scratch` — completely empty, for statically compiled binaries (Go, Rust)

For our Nginx example we already use `nginx:alpine`. Going even smaller would mean building a custom Nginx binary, which is rarely necessary.

The rule: **if it is not needed, it should not be in the image**.

## 6. Scan Images for Known Vulnerabilities

Even minimal images can contain packages with known CVEs. Docker provides a built-in scanner called **Docker Scout**:

```shell
# Quick vulnerability overview
docker scout quickview nginx:alpine

# Full CVE list
docker scout cves nginx:alpine

# Recommendations to fix vulnerabilities
docker scout recommendations nginx:alpine
```

Docker Scout is available in Docker Desktop and as a CLI plugin. It integrates with Docker Hub and can be added to CI/CD pipelines to fail a build when high-severity vulnerabilities are detected.

An alternative open-source scanner is **Trivy**:

```shell
trivy image nginx:alpine
```

Make image scanning part of your build pipeline, not an afterthought.

## 7. Keep Images Up to Date

A scanned image with no vulnerabilities today may have CVEs tomorrow. Pin your base image to a specific digest rather than a floating tag, and automate rebuild checks:

```dockerfile
# Pin to a specific digest (reproducible, auditable)
FROM nginx:alpine@sha256:...
```

Many teams use tools like **Renovate** or **Dependabot** to automatically open PRs when a newer base image is available.

## Putting It All Together

Here is a Dockerfile for our Nginx image that applies all the practices above:

```dockerfile
FROM nginx:alpine

# Copy content
COPY --chown=nginx:nginx html /usr/share/nginx/html

# Drop to non-root
USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

And the corresponding `docker-compose.yml`:

```yaml
services:
  frontend:
    build: .
    image: my-nginx:secure
    container_name: frontend
    ports:
      - "8080:80"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
      - /var/run
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Conclusion

In this article we covered:

- Running containers as a **non-root user** with `USER` in the Dockerfile
- Using a **read-only filesystem** with `--read-only` and `tmpfs` for writable paths
- **Dropping Linux capabilities** with `--cap-drop=ALL` and adding back only what is needed
- Keeping **secrets out of images and environment variables**
- Choosing **minimal base images** to reduce attack surface
- **Scanning images** for vulnerabilities with Docker Scout or Trivy
- **Keeping images up to date** with pinned digests and automated updates

This concludes the **Getting Started with Docker** series. You now have a solid foundation to build, network, persist, orchestrate, and secure containerized applications. The natural next step is **Docker Swarm** for multi-host deployments, or **Kubernetes** for large-scale container orchestration.

---

If you enjoyed this article, don't forget to **give it a clap 👏**, **share it with your friends 🔗**, and **follow me for more tips and tutorials on software development 📘**. Your support helps me create more content like this — thank you! 🙌
