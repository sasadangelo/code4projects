---
layout: post
title: "Mastering DNS Commands: A Guide to Managing DNS with nslookup, dig, and more"
slug: mastering-dns-commands
image: assets/img/rds-logo.png
excerpt: DNS (Domain Name System) is the backbone of the internet, enabling users to access websites and other resources using easy-to-remember domain names, instead of IP addresses.
categories:
  - Networking
sitemap:
  exclude: 'yes'
---

![Docker]({{ site.baseurl }}/wp-content/uploads/2018/06/Docker-logo.png){:width="258" height="200" .responsive_img}

# Mastering DNS Commands: A Guide to Managing DNS with nslookup, dig, and more
_Posted on **{{ page.date | date_to_string }}**_

## Introduction

"DNS, or Domain Name System, is an essential component of the internet that translates domain names into IP addresses. Managing DNS can be a complex task, but by mastering a few key commands, you can easily troubleshoot and manage your DNS records. In this article, we'll cover some of the most commonly used DNS commands, including nslookup, dig, and more, and show you how to use them to manage your DNS records effectively."

Here's a list of commonly used DNS commands and their descriptions:

nslookup: nslookup is a command-line tool that is used to query DNS servers for information about a domain name. It can be used to query for various types of DNS records, including A, MX, and CNAME records.

dig: dig is a command-line tool that is similar to nslookup, but it provides more detailed information about a domain name and its DNS records. It can also be used to query specific DNS servers for information.

host: host is a command-line tool that is similar to nslookup, but it is more lightweight and is often used on Linux and Unix systems. It can be used to query for various types of DNS records, including A, MX, and CNAME records.

whois: whois is a command-line tool that is used to retrieve information about a domain name, including the registered owner and contact information. It can also be used to check the availability of a domain name.

dns-tools: dns-tools is a set of command-line tools that provides a variety of DNS-related functionality, including the ability to perform zone transfers, check for open resolvers, and more.

nsupdate: nsupdate is a command-line tool that is used to update DNS records on an authoritative DNS server. It allows you to add, delete, and modify DNS records in real-time.

These are just a few examples of the DNS commands available and each of them have their own specific use cases. By mastering these commands, you'll be able to manage your DNS effectively and troubleshoot any issues that may arise.

## Using nslookup: Basic Examples and Common Use Cases

"nslookup is a powerful command-line tool for querying DNS servers and managing DNS records. In this section, we'll provide some basic examples of how to use nslookup and explore some common use cases for the tool. We'll cover how to query for different types of DNS records, how to query specific DNS servers, and how to troubleshoot and diagnose common DNS issues."

This section will provide examples and step-by-step instructions for using nslookup to query for various types of DNS records, such as A, MX, and CNAME records. It will also cover how to query specific DNS servers, and how to troubleshoot and diagnose common DNS issues. The examples and use cases provided in this section will help readers to understand the basic functionality of nslookup and learn how to use the tool effectively.

Here are a few basic examples of nslookup commands, what the command does, and how the output should be interpreted.

    {% highlight shell %}
$ nslookup example.com

nslookup example.com
Server:  UnKnown
Address:  192.168.1.1

Non-authoritative answer:
Name:    example.com
Addresses:  192.0.2.1
          198.51.100.1
    {% endhighlight %}

This command will query the default DNS server for information about the domain "example.com". The output will show the IP address and name of the server that is authoritative for the domain, as well as the IP address associated with the domain. In this example, the output shows that the DNS server used is "UnKnown", likely because the nslookup command is not able to determine the DNS server that it is using. In general, "Server: Unknown" message doesn't affect the functionality of the nslookup command and the output will still show the information that is being queried for. The IP address of the DNS server is "192.168.1.1", This is not an authoritative answer, which means that the DNS server you are querying does not host the domain in question, but it holds a cached copy of the DNS record. The name of the domain is "example.com" and its IP addresses are "192.0.2.1" and "198.51.100.1".

    {% highlight shell %}
$ nslookup example.com 8.8.8.8

Server:  google-public-dns-a.google.com
Address:  8.8.8.8

Non-authoritative answer:
Name:    example.com
Addresses:  192.0.2.1
          198.51.100.1
    {% endhighlight %}

This command will query the DNS server at IP address 8.8.8.8 for information about the domain "example.com". The output will show the IP address and name of the server that is authoritative for the domain, as well as the IP address associated with the domain. In this example, the output shows that the DNS server used is "google-public-dns-a.google.com" which is Google public DNS server and its IP address is 8.8.8.8. Like the previous example, this is not an authoritative answer. The name of the domain is "example.com" and its IP addresses are "192.0.2.1" and "198.51.100.1".

    {% highlight shell %}
$ nslookup -type=mx example.com

Server:  UnKnown
Address:  192.168.1.1

Non-authoritative answer:
example.com    MX preference = 10, mail exchanger = mail.
{% endhighlight %}

This command will query the default DNS server for the MX (Mail Exchange) records associated with the domain "example.com". The output will show the name of the server that is authoritative for the domain and the MX records for that domain.

    {% highlight shell %}
$ nslookup -type=txt example.com
    {% endhighlight %}

This command will query the default DNS server for the TXT (Text) records associated with the domain "example.com". The output will show the name of the server that is authoritative for the domain and the TXT records for that domain.

    {% highlight shell %}
$ nslookup -type=ns example.com
    {% endhighlight %}

This command will query the default DNS server for the NS (Name Server) records associated with the domain "example.com". The output will show the name of the server that is authoritative for the domain and the NS records for that domain.

By reading the output of these commands, you should be able to see the information returned by the DNS server, such as the IP address of the domain, the name of the authoritative server, MX records, TXT records and NS records.

It's important to note that the output may vary depending on the DNS server you're querying and the records that are configured for the domain in question.

Please let me know if you need further examples or more details




nslookup -type=mx example.com
Copy code





### Decentralized system

Each DNS server has a specific zone of authority, which is a portion of the domain namespace that it is responsible for. These zones can be organized hierarchically, with the root domain at the top, and subdomains branching out beneath it. This hierarchical structure enables a distributed system where each server is responsible for a specific portion of the domain namespace.

This decentralization ensures that the internet can continue to function even if one or more DNS servers are down. For example, if a DNS server responsible for a specific domain goes down, other servers can take over the responsibility of resolving domain names within that domain. This ensures that the internet remains accessible even in the event of a server failure.

Additionally, as the internet grew, the number of requests to DNS servers also grew, so to distribute the traffic and avoid a central point of failure, a concept called "Anycast" was introduced. This makes it possible to have multiple servers with the same IP address on different location, this way the request of the client is directed to the closest server with the same IP address, reducing the response time and avoid the bottleneck of a single server.

Overall, the decentralized system feature of DNS plays a crucial role in ensuring the reliability and accessibility of the internet.

### Exploring the Hierarchical Structure of DNS

The hierarchical structure of DNS refers to the way in which domain names are organized and managed within the DNS system. At the top of the hierarchy is the root domain, represented by a single dot ".", and beneath it, various levels of subdomains branch out.

The root domain does not correspond to any specific website or IP address, but rather serves as the starting point for resolving domain names. The root domain is managed by a group of organizations known as the Internet Corporation for Assigned Names and Numbers (ICANN).

There are currently thirteen known root servers in the world, identified by the letters A through M. These servers are operated by various organizations and are distributed around the world to ensure that the DNS system is robust and resilient.

It's worth noting that each of these 13 servers are not a single physical server, but rather it's a cluster of servers working together, providing redundancy, and high availability. The idea is to have multiple copies of the same information so that if one server goes down, another one can take its place, minimizing the impact on the users.

Beneath the root domain, there are top-level domains (TLDs), such as .com, .org, and .net. These TLDs are managed by various organizations and are responsible for maintaining a list of authoritative DNS servers for the domains within their TLD.

Underneath the TLDs, there are second-level domains, such as example.com, these domains are registered by individuals or organizations, and are responsible for maintaining the DNS records for the specific domain names.

The hierarchical structure of DNS enables the efficient organization and management of domain names, as well as allows for the delegation of responsibilities among different organizations. This structure ensures that each level of the hierarchy is responsible for a specific portion of the domain namespace, and allows for the distribution of the workload among different servers.

For example, when a user types "www.example.com" into their browser, the request is first sent to the root server, which then directs the request to the TLD server, which then directs the request to the authoritative server for the domain example.com. This hierarchical structure allows for the efficient resolution of domain names and helps to prevent a single point of failure.

It's worth noting that the DNS system is designed to be distributed

### Caching

caching is one of the key features of the DNS system that enables it to operate efficiently and quickly. Caching refers to the temporary storage of DNS information on a local DNS resolver or client, so that it does not have to be queried from the root servers or authoritative servers every time it is needed.

When a local DNS resolver receives a request to resolve a domain name, it first checks its cache to see if it already has the information for that domain name. If the information is present in the cache, the resolver can respond to the request immediately, without having to send a request to the root servers or authoritative servers.

Caching reduces the number of requests sent to the root servers and authoritative servers, which can help to reduce traffic on the internet and speed up the resolution of domain names.

Caching also helps to improve the availability of the DNS system, as it allows the local DNS resolver to respond to requests even if the root servers or authoritative servers are unavailable. For example, if a root server or an authoritative server is down, the local DNS resolver can still respond to requests for domain names that are in its cache, which ensures that the end-user can still access the website.

It's worth noting that the DNS cache has a time to live (TTL) value, which is the amount of time that the information is stored in the cache before it is considered stale. This value is specified in the DNS record and it's set by the authoritative DNS server. Once the cache entry reaches its TTL, the resolver will discard the entry and request an updated version from the authoritative server.

### Who manage the DNS system?

The root servers are managed by a group of organizations known as the Internet Corporation for Assigned Names and Numbers (ICANN). ICANN is a non-profit organization that was created in 1998 with the mission of maintaining the stability, security and global interoperability of the Internet's unique identifier systems, including the Domain Name System (DNS).

ICANN is responsible for coordinating the allocation and assignment of various Internet resources, such as IP addresses and domain names. With regards to the DNS, ICANN coordinates the management of the root zone file, which is the file that contains the information for the root domain of the DNS namespace and delegations of TLDs.

The ICANN's role is to ensure that the root servers are managed in a stable and secure manner, and that the root zone file is updated regularly. This is accomplished by working with other organizations, such as Internet Service Providers (ISPs), governments, and other stakeholders in the Internet community to maintain the stability and security of the Internet's unique identifier systems.

ICANN also coordinates the IANA (Internet Assigned Numbers Authority) functions, which includes the allocation of IP addresses and management of the root zone file. The IANA is responsible for the global coordination of the Internet's system of unique identifiers, such as IP addresses and domain names.

Root servers are maintained by different organizations, such as ICANN, VeriSign, and the United States Department of Defense. These organizations are responsible for ensuring that the root servers are stable, secure and always available to the public. They are connected to the internet via multiple paths, hosted in multiple locations and replicated many times to ensure that the root servers are always available and can handle high levels of traffic.

Top-level domains (TLDs) are managed by various organizations known as domain name registries. These registries are responsible for maintaining the master list of domain names within their respective TLDs, as well as for providing the authoritative DNS servers for those domains.

The organization that manages each TLD varies and can be divided in two types:

Generic Top-level domains (gTLDs) - these are TLDs that are not specific to a certain country or territory, such as .com, .org, .net. They are managed by ICANN-accredited registries. These registries are subject to a set of policies and procedures set by ICANN, and are required to comply with certain technical and operational requirements.

Country Code Top-level domains (ccTLDs) - these are TLDs that are specific to a certain country or territory, such as .fr (France) or .cn (China). They are managed by organizations that are typically based in the respective country or territory, and are subject to the laws and regulations of that country or territory.

Examples of registries that manage gTLDs are Verisign for .com and .net, PIR for .org, and many more.

Authoritative DNS servers are typically managed by the registrant or owner of a domain name. When a domain name is registered, the registrant must specify the names of the authoritative DNS servers for that domain. These servers are responsible for maintaining the DNS records for the domain, such as the IP address associated with the domain name.

The authoritative DNS servers can be hosted by the registrant or the owner of the domain, or it can be managed by a third-party DNS service provider. Some registrars provide DNS hosting as part of the domain registration package, others do not.

The organization that manages the authoritative DNS server for a domain name is responsible for ensuring that the DNS records for that domain are accurate and up-to-date. This includes adding, modifying, or deleting DNS records as necessary, and ensuring that the servers are configured and maintained in a secure and stable manner.

It's important to note that the authoritative DNS servers are different from the root and TLD servers, they're the ones that have the specific information of the domain name, IP address, mail exchange, etc.

## Understanding the Differences Between Root, Authoritative, and Local Resolvers

In the DNS system, there are three main types of servers: root servers, authoritative servers, and local resolvers.

Root servers: The root servers are the first point of contact when a domain name is entered into a browser. These servers are responsible for the top-level domains (TLDs), such as .com, .org, and .net. They contain information about the authoritative servers for each TLD, but not the actual DNS records for specific domain names.

Authoritative servers: Authoritative servers are responsible for specific domains within a TLD. They contain the actual DNS records for those domains, such as the IP address associated with a domain name. When a local resolver receives the IP address of an authoritative server from a root server, it sends a request to that authoritative server to get the actual DNS record for the domain name in question.

Local resolvers: Local resolvers, also known as recursive resolvers, are the DNS servers that are most commonly used by end-users. These servers are typically provided by internet service providers (ISPs) or organizations. They handle requests from clients, such as browsers, and are responsible for sending requests to root servers and authoritative servers to resolve domain names to IP addresses.

Here is a summary of the differences among the root, authoritative, and local servers:

Root servers: Responsible for the TLDs, contains information about the authoritative servers for each TLD, but not the actual DNS records for specific domain names.
Authoritative servers: Responsible for specific domains within a TLD, contains the actual DNS records for those domains, such as the IP address associated with a domain name.
Local resolvers: Responsible for handling requests from clients and sending requests to root servers and authoritative servers to resolve domain names to IP addresses.
It's important to note that all these servers work together to translate domain names into IP addresses, and they are all essential to the functioning of the internet.

### How does DNS works?

1. A user types "www.example.com" into their browser. The browser sends a request to a local DNS resolver, which is responsible 
for resolving domain names to IP addresses. The local DNS resolver first checks its cache to see if it has previously resolved the 
domain name. If it does not find the domain name in its cache, it sends a request to the root DNS server. Example of local DNS servers
are the one typically reported in the resolv.conf file in Linux, Mac, or Unix systems. They are also called local DNS resolvers or recursive resolvers. These are the DNS servers that are responsible for handling requests from clients such as browsers and other applications, and sending requests to root servers and authoritative servers to resolve domain names to IP addresses. The nameservers specified in the resolv.conf file are used by the operating system to determine which DNS server to query when attempting to resolve a domain name.

2. The root DNS server is responsible for the top-level domain (TLD), in this case, the ".com" TLD. The root server looks up the IP 
address of the authoritative DNS server for the ".com" TLD and sends that information back to the local DNS resolver.

3. The local DNS resolver then sends a request to the authoritative DNS server for the ".com" TLD, which is responsible for the 
example.com domain. The authoritative server looks up the IP address associated with the domain name "www.example.com" and sends it 
back to the local DNS resolver.

4. The local DNS resolver then caches the IP address for the domain name "www.example.com" and sends it back to the user's browser. 
The browser then uses the IP address to connect to the web server hosting the website "www.example.com".

In this example, the different DNS servers each had a specific role to play in resolving the domain name "www.example.com" to an IP 
address. If one of the DNS servers were to go down, the system would still be able to function as other DNS servers would take over 
its responsibilities.

Another example of this feature is when a user access a website from different locations. The DNS servers are distributed all over 
the world, so the request of the client is directed to the closest server with the same IP address, reducing the response time and avoid 
the bottleneck of a single server.

In summary, the decentralized system feature of DNS enables multiple servers to work together to resolve domain names to IP 
addresses, ensuring that the internet remains accessible even in the event of a server failure.

## Different Record Types

DNS records are the fundamental building blocks of the DNS system. They contain information about a domain name, such as its IP address, mail server, and name servers. In this section, we will discuss the different types of DNS records and their purpose.

A (Address) Record: Maps a domain name to an IP address. This is the most basic and essential record type. It is used to connect a domain name to its corresponding IP address. For example, when a user types "www.example.com" into their browser, the browser sends a request to the DNS system to resolve the domain name to an IP address. The A record for "www.example.com" would contain the IP address of the web server hosting the website.

MX (Mail Exchange) Record: Specifies the mail server responsible for a domain. This record type is used to route email to the correct mail server for a domain. For example, an MX record for the domain "example.com" might contain the hostname "mail.example.com" and a priority value indicating the order in which mail servers should be contacted.

CNAME (Canonical Name) Record: Specifies an alias for a domain name. This record type is used to create an alias for a domain name, allowing multiple domain names to point to the same IP address. For example, a CNAME record for "www.example.com" might point to "example.com".

NS (Name Server) Record: Specifies the name server for a domain. This record type is used to specify the authoritative DNS servers for a domain. For example, an NS record for the domain "example.com" might list the hostnames of the name servers responsible for the domain.

PTR (Pointer) Record: Maps an IP address to a domain name. This record type is used in reverse DNS lookups, which is the process of resolving an IP address to a domain name. For example, a PTR record for the IP address "192.0.2.1" might contain the hostname "example.com"

It's important to note that these records types are not used in all cases, depending on the specific needs, some records may not be necessary or may not exist.

There is another special A record to talk about: the A (apex) record. The A (apex) record, also known as an "apex domain" or "naked domain" record, is a type of A (Address) record that maps the "naked" domain name (e.g., example.com) to an IP address, as opposed to a subdomain (e.g., www.example.com).

Apex domain is the domain name without the "www" or any subdomain in front of it, it's the base domain name. It's the most basic level of the domain name and it's the only one that doesn't have a subdomain in front of it. The A record that maps the apex domain to an IP address is called the A (apex) record

For example, if a user types "example.com" into their browser, the browser sends a request to the DNS system to resolve the domain name to an IP address. The A (apex) record for "example.com" would contain the IP address of the web server hosting the website.

It's important to note that sometimes, the A (apex) record is not necessary, as the CNAME (Canonical Name) record can be used to point the apex domain to the www domain, and the A record for the www domain is already present, but in cases where the website does not have a www version, the A (apex) record will be necessary.

TXT and SRV are additional types of DNS records that are less commonly used than the ones I described earlier such as A, MX, and CNAME, but they do have specific use cases.

A TXT record is a type of DNS record that allows you to associate text with a domain name or hostname. These records are often used to store information such as SPF (Sender Policy Framework) records, which are used to prevent email spoofing, or DKIM (DomainKeys Identified Mail) records which are used for email authentication.

An SRV record is a type of DNS record that allows you to specify the location of a specific service on a network. These records are often used in conjunction with the _tcp or _udp subdomain to specify the location of a specific service, such as LDAP, Kerberos, or SIP. SRV records contain several fields including priority, weight, port, and target hostname, which provide information about the service and its location.

There are a few other types of DNS records that I haven't mentioned yet, such as:

NS (Name Server) records, which specify the name servers that are authoritative for a domain.
PTR (Pointer) records, which map an IP address to a hostname, and are used for reverse DNS lookups.
SOA (Start of Authority) records, which provide information about the zone of authority for a domain, including the primary name server and the administrator email.
AAAA (Quad-A) records, similar to A record, but it's used for IPv6 addresses.
CAA (Certification Authority Authorization) records, it's used to specify which certificate authority is allowed to issue certificates for a domain.
These records are less commonly used but are still important to understand in order to manage and troubleshoot DNS effectively.

## Tools and Commands for Querying DNS

Managing and troubleshooting DNS can be a complex task, but there are several tools and commands available that can make it easier. In this section, we will take a look at some of the most commonly used tools and commands for querying DNS.

nslookup: is a command-line tool that allows users to query DNS servers for information about a specific domain name. It can be used to query a specific DNS server or to perform a lookup using the default DNS server of the operating system. For example, "nslookup example.com" will return the IP address associated with the domain name example.com.

dig: is a command-line tool that is similar to nslookup, but it provides more detailed information about a domain name and its DNS records. It can be used to query a specific DNS server or to perform a lookup using the default DNS server of the operating system. For example, "dig example.com" will return information about the DNS records for the domain name example.com, including the IP address, name servers, and other information.

host: it's a command-line tool that allows users to perform DNS lookups on a specific domain name. It can be used to query a specific DNS server or to perform a lookup using the default DNS server of the operating system. For example, "host example.com" will return the IP address associated with the domain name example.com.

whois: is a command-line tool that allows users to look up information about a specific domain name, such as the registrant, contact information, and when the domain was registered. For example, "whois example.com" will return information about the registration of the domain name example.com.

online web-based tools: there are several web-based tools available that can be used to perform DNS lookups, such as DNS Checker, DNSdumpster, and MX Toolbox. These tools allow users to perform a variety of DNS-related tasks, such as looking up DNS records, checking DNS propagation, and troubleshooting DNS issues.

These are just a few examples of the tools and commands that can be used to manage and troubleshoot DNS. Depending on the specific needs, other tools may also be used to perform more advanced tasks.

## Conclusion:

DNS is a fundamental part of the internet, enabling users to access websites and other resources using domain names. Understanding the different features of DNS, such as its decentralized structure and caching mechanisms, as well as the different record types, can help with the effective management and troubleshooting of domain names. Additionally, familiarizing yourself with tools and commands for querying DNS, such as nslookup, dig, host, and whois, can also be useful in managing and troubleshooting domain names.
