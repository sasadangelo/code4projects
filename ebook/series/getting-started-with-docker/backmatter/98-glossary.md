# Glossary

**Bind Mount**
: A Docker storage mechanism that maps a specific file or directory on the host
  filesystem directly into a container. Unlike named volumes, bind mounts are not
  managed by Docker and depend on the host's directory structure.

**BuildKit**
: The modern build engine for Docker, enabled by default since Docker 23.0.
  BuildKit provides faster builds, better caching, and new features such as
  cache mounts and secret mounts in Dockerfiles.

**cgroups (Control Groups)**
: A Linux kernel feature that limits, accounts for, and isolates the resource
  usage (CPU, memory, disk I/O, network) of a collection of processes.
  Docker uses cgroups to enforce per-container resource limits.

**Container**
: A runnable instance of a Docker image. Containers are isolated from each other
  and from the host using Linux namespaces and cgroups, but share the host OS kernel.

**containerd**
: The industry-standard container runtime that Docker Engine uses under the hood
  since Docker 1.11. containerd manages the complete container lifecycle:
  image transfer, storage, execution, and supervision.

**Docker Compose**
: A tool for defining and running multi-container Docker applications using a
  declarative YAML file (`docker-compose.yml`). The current version is
  `docker compose` (v2, a Go plugin); the older `docker-compose` (v1, Python)
  was deprecated in May 2023.

**Docker Desktop**
: A GUI application for Mac and Windows that bundles Docker Engine, Docker CLI,
  Docker Compose, and Kubernetes. Requires a paid subscription for enterprise use.

**Docker Hub**
: The default public registry for Docker images. Hosts official images maintained
  by Docker and thousands of community images.

**Docker Scout**
: A vulnerability scanning tool integrated into the Docker CLI and Docker Desktop.
  Analyses images for known CVEs and provides remediation recommendations.

**Dockerfile**
: A plain-text file containing a sequence of instructions that tell Docker how to
  build an image. Each instruction creates a new layer in the image.

**Image**
: A read-only, layered template used to create containers. Images are built from
  Dockerfiles and stored in registries. Each layer represents a filesystem change.

**Layer Cache**
: The mechanism by which Docker reuses unchanged layers from previous builds.
  Layers are rebuilt only when an instruction or its inputs change, making
  subsequent builds significantly faster.

**Namespace**
: A Linux kernel feature that provides isolation for system resources. Docker uses
  multiple namespaces per container: PID (processes), NET (network interfaces),
  MNT (filesystem mounts), UTS (hostname), IPC, and USER.

**OCI (Open Container Initiative)**
: A set of open industry standards for container formats and runtimes.
  Both Docker and Podman produce OCI-compliant images, which means images built
  with one tool can be run by the other.

**Podman**
: A daemonless, rootless container engine that is fully compatible with the Docker
  CLI. An open-source alternative to Docker Desktop, particularly useful on
  corporate machines where Docker Desktop requires a commercial licence.

**Registry**
: A service that stores and distributes Docker images. Docker Hub is the default
  public registry. Private registries include AWS ECR, GitHub Container Registry,
  and self-hosted solutions.

**Reverse Proxy**
: A server that sits in front of backend services and forwards client requests to
  them. Nginx is commonly used as a reverse proxy in containerised applications.

**tmpfs Mount**
: A Docker storage mechanism that stores data in the host's RAM. The data is
  never written to disk and is lost when the container stops. Useful for
  sensitive data and high-speed temporary storage.

**Volume**
: A Docker-managed storage unit that persists data outside the container's
  filesystem. Volumes survive container removal and can be shared across
  multiple containers.

**WSL2 (Windows Subsystem for Linux 2)**
: A compatibility layer in Windows 10/11 that runs a real Linux kernel inside
  a lightweight VM. Docker Desktop uses WSL2 as its Linux backend on Windows.
