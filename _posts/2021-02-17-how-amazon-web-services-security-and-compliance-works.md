---
layout: post
title: How Amazon Web Services Security and Compliance works
post_series_id: getting-started-with-amazon-web-services
slug: how-amazon-web-services-security-and-compliance-works
thumbnail: assets/img/aws-security.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories: Cloud
---

![How Amazon Web Services Security and Compliance works](assets/img/aws-security.png){:width="393" height="200" }

# How Amazon Web Services Security and Compliance works
_Posted on **{{ page.date | date_to_string }}**_

In this article, I will give an overview of how Amazon Web Services Security and Compliance work.

## Introduction to Amazon Web Services Security

Security is one of the main focus of the Amazon Cloud, its goal is to guarantee:

-   **Identity and access management**, only authenticated people can access systems and data and only to the resources they are entitled to use.
-   **Confidentiality**, AWS supports data encryption capabilities. In fact, it offers services and tools to manage keys even at a hardware level.
-   **Integrity**, the platform must guarantee that unauthorized people cannot modify the data and systems.
-   **Compliance**, AWS supports multiple Security compliance programs and there are services that monitor the customer systems and data to raise issues when risks exist.
-   **Availability**, systems must be always available even when failures occur.

Customers need to focus on their business and if they run them on their own infrastructure, they should take care of security. Manage security is not an easy task. It is an ongoing process to find out pitfalls, patch the systems, manage identity and accesses, and so on. For this reason, move the workload on a Cloud infrastructure allows moving the responsibility of much of this work to the Cloud provider and free resources to allocate on the real business.

AWS Security provides the most innovative security services, it will improve them over time, and they will be accessible at a lower cost. It provides the following services and tools:

-   Identity and access management (IAM).
-   Multi-Factory Authentication (MAF).
-   Integration and federations with corporate directories.
-   Amazon Cognito
-   AWS SSO

Moreover, it provides monitoring and logging tools to find risks and understand what’s going on in the environment. In the Amazon Marketplace, there are other 3rd party services and tools that are integrable with the one provided by Amazon.

## Network Security

Amazon Cloud implements network security through a series of features like:

-   **VPC**. In [this article](amazon-web-services), I talked about Amazon VPC as a way to create one or more isolated networks in the customer account. Therefore, you can control or filter network traffic to avoid security issues.
-   **Built-in Firewalls**. It is possible to define the service exposed on EC2 instances, the source, and the target of whatever connection.
-   **Encryption in transit**. Possibility to have TLS network connections where data in transit are encrypted.
-   **Private or Dedicated connections**. For example, the possibility to create a VPN versus your On-Premises world.
-   **Distributed Denial of Services (DDoS) mitigation**. Tools and Services to avoid DDoS attacks.

## Identity and Access Management (IAM)

IAM is the Amazon component responsible to manage Identities and the way they access the AWS resources. The first concepts to learn are user, group, role, and policy documents. For more details about Amazon IAM [read the following article](beginners-guide-identity-access-management).

## Amazon Inspector

### Amazon Inspector Introduction

Security is the most important aspect of whatever technology infrastructure. However, it is an expensive, complex, and time-consuming activity that is hard to track and do effectively. A normal security activity requires:

1.  **assessment** about the status of the infrastructure and data to find vulnerabilities and deviation from the best practices;
2.  **create a report** where there is a list of all the vulnerabilities and deviations with the right priority.

In the AWS Cloud Amazon Inspector is the component that performs this job. However, it doesn’t guarantee the completeness of the report,  because it depends on the Shared Responsibility model. Therefore, it can only show the vulnerabilities and deviations under AWS’s responsibility.

You can access Amazon Inspector via:

-   management console;
-   AWS CLI;
-   AWS SDK;
-   HTTPS API.

### Amazon Inspector benefits

As said above, Amazon allows your organization to find vulnerabilities and deviations in your system and data. The assessment happens in the development and production phases. Moreover, it is an ongoing process that improves the security of the system and data over time.

Amazon Inspector is agent-based, API-driven, delivered as a service. You can easily integrate it into your DevOps activities so that you can decentralize and automate security activities to find security issues during the development, test, and production phases.

The tool improves development agility because security issues are found immediately and it is easy to solve them when you identify them in the early phase of the development process.

The tool leverage the knowledge of AWS expertise so you are sure the most advanced checks are performed in your infrastructure and data.

These activities enforce security standards in the development, test, and operation processes.

![Amazon Inspector Benefits](assets/img/Amazon-Inspector-Benefits.png)

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

## Amazon Shield

Amazon Shield is a managed **Distributed Denial of Service (DDoS)** protection service that safeguards applications running on AWS. Before continuing let’s see what is a DDoS attack and what is the difference with a Denial of Service (DoS) attack.

### What is a DDoS attack?

**DoS attack** is a deliberate attempt to make your website or application unavailable to users. Basically, the attacker sends fake network traffic to the target machine in order to consume as much bandwidth as possible in order to reach its scalability limits, let the system suffers and make its services unavailable to the end-users.

![DoS Attack](assets/img/DoS-Attack.png)

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

The **DDoS attack** has the same goal as the DoS but the attack comes from multiple sources orchestrated via software.

![DDoS Attack](assets/img/DDoS-Attack.png)

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

DDoS attacks can happen at the infrastructure and application layer. The former is an attack on the server node try to limit its network bandwidth and reduce its availability to legitimate users. On the contrary, attacks to the application layer try to request application resources (i.e. HTML pages) in order to consume the bandwidth.

Resolution of DDoS attacks is a complex, time-consuming, and expensive task. It limits the bandwidth of network infrastructure with consequent scalability issues. In an On-Premis world, these tasks require manual intervention.

### Amazon Shield subscriptions

Amazon Shield provides two subscriptions:

-   **Standard**. Automatic protections are available for all AWS customers for all their resources in any region, at no additional charge. You have built-in automated mitigation techniques to avoid latency impacts. There is no need to engage AWS support.
-   **Advanced**. Paid service for a higher level of protection, features, and benefits. It provides additional capacity to protect against larger DDoS attacks. You have visibility and notification when an attack occurs.

These two subscriptions offer a lot of mitigation techniques at the infrastructure and application layers. For example, the **Standard subscription** protects your Amazon Route 53 Hosted Zones from infrastructure layer DDoS attacks, including reflection attacks or SYN floods that frequently target your DNS. A variety of techniques, such as header validations and priority-based traffic shaping, automatically mitigate these attacks. The **Advanced subscription** provides even greater protection, visibility into attacks on your Route 53 infrastructure, and help from the response team for extreme scenarios.

There are other mitigation techniques for EC2, CloudFront, and other resources that we avoid mentioning in this general overview.

Amazon AWS supports customers in a lot of industries. Sometimes these industries create standards in order to create a legal security baseline for the participant in that industries. There are a lot of standards and Amazon AWS helps its customer to be compliant with them.

![Amazon Web Services Security](assets/img/Amazon-Security-Compliance.png)

_Photo from [AWS Cloud Practitioner Essentials (2nd Edition)](https://aws.amazon.com/it/training/course-descriptions/cloud-practitioner-essentials/) course_

Depending on the AWS resource and the Shared Responsibility Model the work to be compliant can be under AWS or customer responsibility. In any case, the customer needs:

-   list the rules of the compliance;
-   understand the deviation of its infrastructure and data from these rules;
-   assess the risk and evaluate the priority of each deviation;
-   create an attack plan to mitigate these risks and meets the compliance rules.

When the Shared Responsibility model assigns these activities to AWS it provides reports about the current infrastructure and data status, the list of deviations with the risk assessment, and the prioritization. In some cases, AWS provides also a resolution for these risks.

## Conclusions

In conclusion, this article provides an overview of how security and compliance are managed by the AWS platform. Its goal is to let you understand how seriously Amazon manages security in its platform, what are the tools that help customer to secure their infrastructure and data.