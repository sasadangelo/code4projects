---
layout: course
title: Kubernetes Cluster IP vs NodePort vs LoadBalancer vs Ingress
course_id: getting-started-with-kubernetes
---
# Kubernetes Cluster IP vs NodePort vs LoadBalancer vs Ingress

This is the second article of the [Getting Started with Kubernetes](/code4projects/) article series. In this article, I want to explain a concept that confused me when I started working with Kubernetes: **Cluster IP vs NodePort vs LoadBalancer vs Ingress**.

## Kubernetes Service types

In the first article of this series, we said that a **Service** is an abstraction level that Kubernetes uses to make a deployed application accessible from the internal and external of the cluster. Kubernetes supports three different types of services:

* Cluster IP;
* NodePort;
* Load Balancer.

It is extremely important to understand the difference between them to correctly design your applications. It’s also important to understand the difference between these concepts and the Ingress.

## Cluster IP vs NodePort vs LoadBalancer

### Cluster IP Service

A ClusterIP service is the default Kubernetes service. It gives you a service inside your cluster that other apps inside your cluster can access. **There is no external access**. The YAML for a ClusterIP service looks like this:

```
apiVersion: v1
kind: Service
metadata:
    name: my-internal-service
spec:
    selector:
        app: my-app
    type: ClusterIP
    ports:
    - name: http
      port: 80
      targetPort: 80 
      protocol: TCP
```

It’s possible to access, for debugging purposes, from the external to the Cluster IP using the Kubernetes proxy as the following figure shows. As you can notice, an application App2 can internally communicate with the application App1 via the Cluster IP.

IMAGE

Start the Kubernetes Proxy:

    `kubectl proxy --port=8080`

Now, you can navigate through the Kubernetes API to access this service using this scheme:

**http://localhost:8080/api/v1/proxy/namespaces/<NAMESPACE>/services/<SERVICE-NAME>:<PORT-NAME>/**

So to access the service we defined above, you could use the following address:

**http://localhost:8080/api/v1/proxy/namespaces/default/services/my-internal-service:http/**

In the YAML file, the service map the HTTP port 80 to the container port 80 (targetPort).

### NodePort

A NodePort service is the easiest way to get external traffic directly to your service. I use it also for debugging purposes when I want easily test my service from the external. A NodePort service, as the name implies, opens a specific port on all the Worker Nodes (the VMs), and any traffic that is sent to this port is forwarded to the service.

The range of the ports available for this kind of service is 30000-32767, in the YAML you can specify it or let Kubernetes assign a value to it. Usually, I prefer the second option to avoid conflicts and let Kubernetes do the right choice. You can know the value assigned with the command:

`kubectl get services --all-namespaces`

IMAGE

As you can notice from the image above the external traffic can arrive on the IP of one of the three nodes on port 30036, it will arrive to the NodePort service that will forward the traffic to a specific Pod.

The YAML for a NodePort service looks like this:

```
apiVersion: v1
kind: Service
metadata:
    name: my-nodeport-service
spec:
    selector:
        app: my-app
    type: NodePort
    ports:
    - name: http
      port: 80
      targetPort: 80
      nodePort: 30036
      protocol: TCP
```

In the YAML file, the service map the HTTP port 80 to the container port 80 (targetPort), but it is accessible from the external using IP:PORT, where IP is one of the Worker Node (VMs) IP and PORT is the nodePort. As said above, if you don’t specify the nodePort field Kubernetes will assign a value to it.

I think NodePort is really convenient when you want to test immediately your service but you don’t have the possibility to create a Load Balancer service (i.e. on a local Kubernetes used for tests purpose). The main issue is that you have to deal with the Worker Node IP changes and use a port number in the range 30000-32767 not really convenient for production systems.

### Load Balancer

A LoadBalancer service is the standard way to expose a service to the internet. On the Cloud of most vendors, this will create a Network Load Balancer that will give you a single IP address that will forward all traffic to your service.

IMAGE

The problem with this type of service is that it is only available on the Cloud platform of some vendors and you should pay for it. If you are using a local Kubernetes cluster (i.e. using Kubespray or my ad-hoc solution) on your laptop there is no chance you can use this type of service. In this case, the only way to go is via NodePort.

### Kubernetes Ingress

Unlike all the above examples, Ingress is NOT a type of service. Instead, it sits in front of multiple services and acts as a “reverse proxy” for them. You can do a lot of different things with an Ingress, and there are many types of Ingress controllers that have different capabilities.

The most important thing you can do with an Ingress is to do both path-based and subdomain based routing to backend services as shown by the following figure.

### Kubernetes Ingress

The YAML for an Ingress looks like this:

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
name: my-ingress
spec:
    backend:
        serviceName: other
        servicePort: 8080
    rules:
    - host: foo.mydomain.com
      http:
          paths:
          - backend:
                serviceName: foo
                servicePort: 8080&nbsp;
    - host: mydomain.com
      http:
          paths:
          - path: /bar/*
            backend:
                serviceName: bar
                servicePort: 8080
```

The following YAML file specifies that all the traffic to foo.mydomain.com is redirected to the foo service on the 8080 port. All the traffic to *mydomain.com/bar/** path will be redirected to the bar service on 8080 port.

## When should I use what?

Once we understand the differences between the three types of services and the Ingress, we need to understand when should I use what? The following sections summarize this for you.

### Cluster IP:

Here my thoughts about this service type:

1. Debugging your services, or connecting to them directly from your laptop for some reason using Kubernetes proxy.
2. Allowing internal traffic so that other applications in the same cluster can contact the service.
3. Designed to be NOT accessible from the external of the cluster. 

###NodePort:

Here my thoughts about this service type:

1. Very convenient to create a service easily contactable from the external on your laptop during the tests.
2. You can only have one service per port.
3. You can only use ports 30000–32767.
4. If your Node/VM IP address change, you need to deal with that.

For reasons 3 and 4, don’t use this method in production. If you are running a service for demo purpose or temporary that doesn’t have to be always available, this method will work for you.

### Load Balancer

Here my thoughts about this service type:

1. If you have the possibility to use this type of service, go fo it.
2. All traffic on the port you specify will be forwarded to the service. There is no filtering, no routing, etc.
3. The big downside of it is that it is usually only available on a Cloud environment where you have to pay to allocate a Load Balancer for your service.
4. You have an IP for each service.
5. It’s expensive.

### Ingress

Here my thoughts about the Ingress:

1. Ingress is the most useful if you want to expose multiple services under the same IP address using path-based or subdomains routing.
2. On the local Kubernetes cluster, it is useful to bypass some NodePort limitation like the port number (you can use 80 port), use a hostname to bypass the VM IP change.
3. On a production system, where Load Balancer is not available, you can bypass the problem exposing one or more services via NodePort and then use an Ingress in front of them to manage the traffic.

## Final Thoughts

This article contains a lot of useful information that for me are very important to understand how Kubernetes works. There are other important concepts to explain. In the next article, I will explain how to separate configuration from code and data using **Kubernetes ConfigMaps**.