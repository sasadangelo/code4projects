---
layout: post
title: "The Benefits of Using YAML: An Easy and Flexible Data Serialization Format"
slug: getting-started-with-yaml
thumbnail: assets/img/rds-logo.png
excerpt: bla bla bla
categories:
  - Programming
sitemap:
  exclude: 'yes'
---

![Docker]({{ site.baseurl }}/wp-content/uploads/2018/06/Docker-logo.png){:width="258" height="200" .responsive_img}

# Mastering the Basics of CSS: A Beginner's Guide

_Posted on **{{ page.date | date_to_string }}**_

## Introduction

YAML, short for Yet Another Markup Language, is a popular data serialization format that is used for various purposes, including configuration files, data storage, and cloud infrastructure management. Its simple and clean syntax, human-friendly design, and support for complex data structures make it a versatile choice for many use cases. This article will explore the benefits of using YAML, including its ease of use, versatility, and wide adoption, and why it is a great choice for data serialization.

A YAML format primarily uses 3 node types:

* **Literals** (Strings, numbers, boolean, etc.):
The content of a scalar node is an opaque datum that can be presented as a series of zero or more Unicode characters.
* **Maps/Dictionaries** (YAML calls it mapping):
The content of a mapping node is an unordered set of key/value node pairs, with the restriction that each of the keys is unique. YAML places no further restrictions on the nodes.
* **Arrays/Lists** (YAML calls them sequences):
The content of a sequence node is an ordered series of zero or more nodes. In particular, a sequence may contain the same node more than once. It could even contain itself.

## Representing Literals Data in YAML: Key-Value Pairs

YAML files consist of a series of key-value pairs, which are used to store data. The keys and values are separated by colons and can represent primitive data types such as strings, numbers, and booleans. For example, the following YAML file represents a person's name and age:

    {% highlight yaml %}
name: "John Doe"
age: 30
male: true
    {% endhighlight %}

In this example, name is the key and "John Doe" is the associated value. The name attribute is a string. YAML strings are Unicode. In most situations, you don't have to specify them in quotes. But if we want escape sequences handled, we need to use double quotes. Similarly, age is the key and 30 is an integer value. YAML file supports floating points type value too. 

Finally, male is a boolean with value true. YAML indicates boolean values with the keywords True, On and Yes for true. False is indicated with False, Off, or No. 

## Multi-Line Strings in YAML: Representing Large Blocks of Text or Data

String values can span more than one line. 

### Folding Strings

With the fold (greater than) character, you can specify a string in a block. But it's interpreted without the newlines. 

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

## Representing Lists in YAML

YAML also supports lists and arrays, which can be represented as follows:

    {% highlight yaml %}
fruits:
  - apples
  - bananas
  - oranges
    {% endhighlight %}

In this example, the key fruits is associated with a list of three items: apples, bananas, and oranges. This simple syntax makes YAML easy to read and write for both humans and machines.

Sometimes in a single YAML file there could be several file sections each one starting with three dashes.

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

In this example, the key person is associated with an object that has two attributes: name and address. The address attribute is itself an object with four attributes: street, city, state, and zip. This syntax makes it easy to represent complex data structures in YAML and allows for a clean and intuitive representation of data.

It is worth noting that the indentation of the lines in YAML is important and determines the hierarchy of the data. In the example above, the indentation of the street, city, state, and zip lines indicates that they are attributes of the address object. Proper indentation is crucial for the correct parsing of YAML files. Indentation is how YAML denotes nesting. The number of spaces can vary from file to file, but tabs are not allowed.

## Dictionaries in YAML: Storing Key-Value Pairs in a Collection

In YAML, dictionaries are a collection of key-value pairs that are used to store data. A dictionary is represented by a series of key-value pairs separated by dashes, with the keys and values indented beneath the dashes. For example, consider the following YAML representation of a dictionary of people:

    {% highlight yaml %}
people:
  - name: John Doe
    age: 30
  - name: Jane Doe
    age: 28
    {% endhighlight %}

In this example, the key people is associated with a dictionary of two key-value pairs, each representing a person with a name and age attribute. This syntax allows for the easy representation of collections of data, such as lists of people, products, or any other type of data.

Dictionaries in YAML are useful for grouping related data together and for easily accessing individual items within the collection. The ability to store data in dictionaries and retrieve it based on the keys makes YAML a powerful and flexible data serialization format.

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

## Conclusion

In conclusion, YAML is a popular and human-readable data serialization format that provides a simple and efficient way to represent data structures and primitive data types. This article covered the basics of YAML, including primitive data types like strings, numbers, and booleans, as well as more complex data structures like dictionaries, arrays, and nested objects. Additionally, we covered more advanced concepts in YAML, such as multiline strings, anchors and aliases, literal and folded scalars, and custom data types.

By understanding these basic concepts, you can effectively use YAML to represent a wide range of data in a clear and concise format. Whether you're working with configuration files, data storage, or application APIs, YAML offers a flexible and straightforward solution for data serialization and representation.