---
layout: post
title: "The Benefits of Using YAML: An Easy and Flexible Data Serialization Format"
slug: getting-started-with-yaml
thumbnail: assets/img/yaml-logo.webp
excerpt: YAML, short for Yet Another Markup Language, is a popular data serialization format used for various purposes, including configuration files, data storage, and cloud infrastructure management.
categories:
  - Programming
sitemap:
  exclude: 'yes'
---

![YAML]({{ site.baseurl }}/assets/img/yaml-logo.webp){:width="200" height="200" .responsive_img}

# The Benefits of Using YAML: An Easy and Flexible Data Serialization Format

_Posted on **{{ page.date | date_to_string }}**_

## Introduction

YAML, short for YAML Ain't Markup Language, is a popular data serialization format used for various purposes, including configuration files, data storage, and cloud infrastructure management. 

This article will explore the benefits of using YAML, including its ease of use, versatility, and wide adoption, and why it is a good choice for data serialization.

## What is YAML

![What is YAML]({{ site.baseurl }}/assets/img/what-is-yaml.jpeg){:width="450" height="253" .responsive_img}

_Photo from [Youtube](https://www.youtube.com/watch?v=8zOkCl3kgcg)_

YAML is a light-weight, human-readable data-serialization language. It is primarly designed to make the format easy to read while including advanced feature. Its simple and clean syntax, human-friendly design, and support for complex data structures make it a versatile choice for many use cases.

YAML is similar to XML and JSON but it is less verbose, more readable, eand easy to use. Many products like Ansible, Kubernetes, Puppets, Jenkins, Docker, AWS, and others use YAML for managing configuration files because it is much easier to read and less verbose than JSON and XML.

YAML file have ".yaml" or ".yml" extension and you can edit them in whatever text editor.

YAML is similar to JSON inline style, from this point of view it can be considered a superset of of JSON. For example, JSOn doesn't support comments while YAML does.

In addition, YAML is very easy and simple to represent complex objects and data structures. Due to which it is heavily used in configuration management.

You can find more information about YAML in its [official website](https://yaml.org/).

## XML vs JSON vs YAML

![YAML vs JSON vs XML]({{ site.baseurl }}/assets/img/yaml-json-xml.jpeg){:width="450" height="238" .responsive_img}

_Photo from [https://medium.com/](https://medium.com/geekculture/yaml-vs-json-vs-xml-in-go-bf4ebd1066f2)_

XML was introduced in 1996 as a format for "...for storing, transmitting, and reconstructing arbitrary data" according to Wikipedia. 

XML is an extensible markup language that, through a Document Type Definition (DTD), allow to define documents that match different grammars. For many years it has been used in Java and other languages as a data serialization or transmission (SOAP) format. However, it is quite a verbose language because it requires data to be enclosed between two tags and it is not easy to read for a human. Today it is still used as a configuration tool in many languages ​​and operating systems such as Java and Android.

JSON (Javascript Object Notation) is a format created for data transmission between servers and browsers especially when using the Javascript language. Precisely because it is a format that was created for data transmission, its goal is to be as least verbose as possible and clear in representing the data. For this reason, the format does not support comments. This makes JSON less suitable for representing configuration files and management even though it is used for that purpose in many contexts.

YAML in some ways is a superset of JSON, which means all the features in JSON can be found in YAML. The fact that the format is human-readable and easy to use makes it to represent configuration files and management.

![Comparison Table]({{ site.baseurl }}/assets/img/xml-vs-json-vs-yaml.png){:width="450" height="225" .responsive_img}

_Photo from YAML Zero to Master Udemy Course_

Online there are [a lot of tools](https://www.json2yaml.com/) that help you to convert one format in another.

## YAML Basic Concepts

A YAML format to represents data uses the following data type:

* **Scalars**: The content is a primitive type like strings, numbers, boolean, and so on.
* **Timestamp**: The content is date or time.
* **Sequences** (YAML calls them sequences):
The content of a sequence node is an ordered series of zero or more nodes. In particular, a sequence may contain the same node more than once. It could even contain itself. Arrays and Lists are example of sequences.
* **Dictionaries** (YAML calls it mapping): the content of a mapping node is an unordered set of key/value node pairs, with the restriction that each of the keys is unique. YAML places no further restrictions on the nodes.
* **Objeccts**: the content is a record describing a given object.

In addition to this, YAML supports comments.

## Representing Scalars Data in YAML: Key-Value Pairs

YAML files have of a series of key-value pairs, which are used to store data. The keys and values are separated by colons and can represent primitive data types such as strings, numbers, and booleans. For example, the following YAML file represents a person's name and age:

    {% highlight yaml %}
firstname: "John"
lastname: Doe
middlename: 'Sir'
age: 30
height: 176
weight: 75.2
male: true
positive-infinity: .inf
negative-infinity: -.inf
invalid-number: NaN
null-value: null
null-value: ~
null-value:
    {% endhighlight %}

In this example, the name is the key, and "John" is the associated value. The name attribute is a string. YAML strings are Unicode. In most situations, you don't have to specify them in quotes. But if we want escape sequences handled, we need to use double or single quotes. Similarly, age is the key and 30 is an integer value. YAML supports also floating points.

Boolean value are "true" and "false", but you can use also "Yes" and "No" because internally YAML convert them in "true" and "false".

There are special scalar value in YAML you can use like positive and negative infinity number, null value and invalid number.

## Comments

You can comment contents of a YAML file using the # character as shown below.

    {% highlight yaml %}
# This is a comment on the first.
# And this is a commented second line.
    {% endhighlight %}


## Representing Sequences in YAML

YAML also supports lists and arrays, which can be represented as follows:

    {% highlight yaml %}
fruits:
  - apples
  - bananas
  - oranges
    {% endhighlight %}

In this example, the key "fruits" is associated with a list of three items: apples, bananas, and oranges. This simple syntax makes YAML easy to read and write for both humans and machines.

There are two styles to represents sequences: block and flow. The following example shows both: 

    {% highlight yaml %}
# Sequences in Block Style
legumes:
- peas
- beans
- lentils
fruits:
  - apples
  - bananas
  - oranges
fruits:
  - apples
  - bananas
  - oranges
# Sequences in Flow Style
places: [sea, ​​mountain, "hill"]
    {% endhighlight %}

It is possible to nest sequences in the element of a sequence as the follows. In the example, a company could sell three types of products: Cars, Motorbikes, and Bikes. Then in the Car category it can sell Jeep, Ferrari, and Lamborghini. 

    {% highlight yaml %}
# Sequences in Block Style
products:
- Cars:
  - Jeep
  - Ferrari
  - Lamborghini
- Motorbikes:
  - "Harley-Davidson"
  - Honda
  - Ducati
- Bikes:
  - Mountain Bike
  - "Trek bike"
    {% endhighlight %}

## Dictionaries in YAML: Storing Key-Value Pairs in a Collection

In YAML, dictionaries are a collection of key-value pairs that are used to store data. A dictionary is represented by a series of key-value pairs separated by dashes, with the keys and values indented beneath the dashes. For example, consider the following YAML representation of a dictionary of people:

    {% highlight yaml %}
people:
  - name: Mary jane
    age: 30
    male: No
  - name: Jane Doe
    age: 28
    male: Yes
    {% endhighlight %}

In this example, the key "people" is associated with a dictionary of two key-value pairs, each representing a person with a name and age attribute. This syntax allows for the easy representation of collections of data, such as lists of people, products, or any other type of data.

Dictionaries in YAML are useful for grouping related data together and for easily accessing individual items within the collection. The ability to store data in dictionaries and retrieve it based on the keys makes YAML a powerful and flexible data serialization format.

## Representing Objects in YAML: Nested Key-Value Pairs

In addition to primitive data types, YAML also supports the representation of objects or complex data structures. An object in YAML is represented using nested key-value pairs, where each key-value pair represents an attribute of the object. For example, consider the following YAML representation of a person object with name and address attributes:

    {% highlight yaml %}
person:
  name: John Doe
  address:
    street: 123 Main St.
    city: Anytown
    state: CA
    zip: 90210
    {% endhighlight %}

In this example, the key "person" is associated with an object that has two attributes: name and address. The address attribute is itself an object with four attributes: street, city, state, and zip. This syntax makes it easy to represent complex data structures in YAML and allows for a clean and intuitive representation of data.

It is worth noting that the indentation of the lines in YAML is important and determines the hierarchy of the data. In the example above, the indentation of the street, city, state, and zip lines indicates that they are attributes of the address object. Proper indentation is crucial for the correct parsing of YAML files. Indentation is how YAML denotes nesting. The number of spaces can vary from file to file, but tabs are not allowed.

## Conclusion

In conclusion, YAML is a popular and human-readable data serialization format that provides a simple and efficient way to represent data structures and primitive data types. This article covered the basics of YAML, including primitive data types like strings, numbers, and booleans, as well as more complex data structures like dictionaries, arrays, and nested objects. Additionally, we covered more advanced concepts in YAML, such as multiline strings, anchors and aliases, literal and folded scalars, and custom data types.

By understanding these basic concepts, you can effectively use YAML to represent a wide range of data in a clear and concise format. Whether you're working with configuration files, data storage, or application APIs, YAML offers a flexible and straightforward solution for data serialization and representation.

On the Internet there are a lot of tutorials you can use to start using YAML files, here few of my favorites:

* [YAML Tutorial: Everything You Need to Know in 5 Mins](https://levelup.gitconnected.com/yaml-tutorial-everything-you-need-to-know-in-5-mins-14f333a23ed1)
* [YAML Tutorial: A Complete Language Guide with Examples](https://spacelift.io/blog/yaml)
* [YAML Basic to Advance](https://medium.com/globant/yaml-basic-to-advance-36a3046e3bf6)















## Multi-Line Strings in YAML: Representing Large Blocks of Text or Data

String values can span more than one line. YAML supports three types of multi lines string:

* Folding Strings
* Block Strings
* Chomp characters

Let's explore them in detail.

### Folding Strings

With the fold (greater than) character, you can specify a string in a block. But it's interpreted without the newlines. New lines are converted into spaces.

    {% highlight yaml %}
text: >
  this text will be considered on a
  single line
    {% endhighlight %}

The above YAML snippet is interpreted as below.

    {% highlight yaml %}
text: "this text will be considered on a single line"
    {% endhighlight %}

### Block strings

The block (pipe) character has a similar function, but YAML interprets the field exactly as is.

    {% highlight yaml %}
text: |
  this text will be considered on multiple
  lines
    {% endhighlight %}

This is interpreted with the new lines (\n) as below.

    {% highlight yaml %}
text:
  this text will be considered on multiple
  lines
    {% endhighlight %}

### Chomp characters

The chomp characters define how YAML will interpret trailing newlines and spaces at the end of your block and can be one of the following: Strip and Keep modes.

**Clip mode**: this is the default behavior, the one used when you don’t specify any specific chomp indicator in your header. In this mode, the final newline is preserved, but any additional trailing empty lines are ignored.

    {% highlight yaml %}
text: 
  clip: >
    this text will be considered on a single line with a new line
    {% endhighlight %}

**Strip mode**: indicated by a - in the block header, this will strip not only trailing empty lines like in clip mode but also the final newline at the end of the string.

    {% highlight yaml %}
text: 
  strip: >-
    this text will be considered on a single line with no new line
    {% endhighlight %}

**Keep mode**: indicated by a + in the block header, this will keep both the final newline and any potential trailing empty lines too.

    {% highlight yaml %}
text: 
  keep: >+
    this text will be considered on a single line with a new line and trailing new lines
    {% endhighlight %}




## Anchors and Aliases in YAML: Reusing Complex Data Structures

YAML allows for the creation of reusable elements through the use of anchors and aliases. An anchor is a label attached to a specific piece of data, and an alias is a reference to that anchor. This allows for the creation of complex data structures with repetitive elements.

Here's an example of using anchors and aliases in YAML:

    {% highlight yaml %}
person: &person
  name: John Doe
  age: 30

other_person: *person
    {% endhighlight %}

In this example, an anchor &person is attached to a dictionary of key-value pairs representing a person. An alias *person is then created to reference this data. The result is two variables, person and other_person, that both refer to the same dictionary of data.

Anchors and aliases are a powerful feature in YAML, allowing for the reuse of complex data structures and reducing the need for duplication in YAML files. They can be especially useful for creating templates or for sharing common data between multiple parts of an application.

## Custom Data Types in YAML: Extending the Built-in Types

YAML supports the creation of custom data types, allowing developers to extend the built-in data types to handle specific use cases. Custom data types can be used to represent complex data structures, or to enforce constraints on the values of a key-value pair.

The implementation of custom data types varies depending on the YAML parser being used, but a common approach is to use tags to specify the type of a value. For example:

    {% highlight yaml %}
!date
2022-12-31
    {% endhighlight %}

In this example, the !date tag is used to specify that the value 2022-12-31 is of type date. The YAML parser can then use this information to properly interpret the value as a date.

You can create a custom data type to represent email addresses in YAML, such as the following:

    {% highlight yaml %}
!email
example@example.com
    {% endhighlight %}

In this example, the !email tag is used to specify that the value example@example.com is of type email. The YAML parser can then use this information to validate the value as a valid email address.


