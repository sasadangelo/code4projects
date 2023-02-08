---
layout: post
title: "Exploring the Depths of YAML: Advanced Features and Functionality"
post_series_id: getting-started-with-yaml
slug: yaml-advanced-feature
thumbnail: assets/img/yaml-advanced.webp
excerpt: Dive deeper into YAML with this comprehensive guide to advanced concepts. Learn tips and techniques to fully unlock its power and functionality.
categories:
  - Programming
sitemap:
  exclude: 'yes'
---

![YAML]({{ site.baseurl }}/assets/img/yaml-advanced.webp){:width="356" height="200" .responsive_img}

# Exploring the Depths of YAML: Advanced Features and Functionality

_Posted on **{{ page.date | date_to_string }}**_

## Introduction

In a [previous article]({{ site.baseurl }}/getting-started-with-yaml/), we covered the basics of YAML, a popular human-readable data serialization format that is widely used in various applications and technologies. However, there is much more to YAML than just the basics. In this article, we will take a deeper dive into advanced YAML concepts. This comprehensive guide will cover tips, techniques, and best practices for fully leveraging the power and functionality of YAML, making it a valuable resource for both new and experienced users alike.

## Multi-Line Strings in YAML: Representing Large Blocks of Text or Data

Strings are an important data type in YAML and were discussed briefly in the [previous article]({{ site.baseurl }}/getting-started-with-yaml/). As a reminder, strings are sequences of characters that don't necessarily have to be enclosed in quotes or single quotes. However, if you use special characters such as \"{, }, [, ], ,, &, :, *, #, ?, \|, -, <, >, =, !, %, @, \" you will need to enclose the string in quotes.

String values can span more than one line. YAML supports three types of multi lines string:

* **Folding Strings**
* **Block Strings**
* **Chomp characters**

Let's explore them in detail.

### Folding Strings

With the fold (greater than) character, you can specify a string in a block. But it's interpreted without the trailing newlines. New lines are converted into spaces. We can use the Fold style to remove new lines within a string.

    {% highlight yaml %}
text: >
  this text will be considered on a
  single line


    {% endhighlight %}

The above YAML snippet is interpreted as below. Notice how only a single new line remains at the end of the string.

    {% highlight yaml %}
text: "this text will be considered on a single line\n"
    {% endhighlight %}

### Block strings

The block (pipe) character has a similar function, but YAML interprets the field exactly as is.

    {% highlight yaml %}
text: |
  this text will be considered 
  on multiple
  lines


    {% endhighlight %}

This is interpreted with the new lines (\n) in the middle preserved and only one new line at the end.

    {% highlight yaml %}
text: "this text will be considered\non multiple\nlines\n"
    {% endhighlight %}

### Chomp characters

The chomp characters define how YAML will interpret trailing newlines at the end of your block and can be one of the following: Clip, Strip and Keep modes.

**Clip mode**: this is the default behavior, the one used when you don’t specify any specific chomp character in your header. It is the Fold or Block style above.

**Strip mode**: indicated by a - in the block header. When used with the Fold character (>) it will behave like in the Fold style but remove the final new line.

    {% highlight yaml %}
text: 
  strip: >-
    this text will be considered 
    on a single line 
    with no new line
    {% endhighlight %}

The above YAML snippet is interpreted as below. Notice the new line is not present at the end of the string like  in the Fold style. Notice the removal of the trailing new line.

    {% highlight yaml %}
text: "this text will be considered on a single line with no new line"
    {% endhighlight %}

In the same way, if you want to have a string in Block mode without the trailing newlines you can use the chomp character "|-".

**Keep mode**: indicated by a + in the block header, this will keep both the final new line and any potential trailing empty lines too.

    {% highlight yaml %}
text: 
  keep: >+
    this text will be considered 
    on a single line 
    with a new line at the end.


    {% endhighlight %}

The text is interpreted in this way:

    {% highlight yaml %}
text: "this text will be considered on\nmultiple lines\nwith a new line and trailing newlines\n\n\n"
    {% endhighlight %}

A good way to check how the YAML parser interprets your string is to use this [online tool](https://www.json2yaml.com/). Insert your YAML file on the right and see its equivalent in JSON which will show you the strings with new lines.

## Implicit vs. Explicit Typing in YAML: Understanding How to Use Them

YAML supports both implicit and explicit typing of values, allowing you to specify the type of data you are working with. Implicit typing, also known as automatic typing, uses the structure of the data to determine the type, while explicit typing, also known as tagged typing, uses tags to specify the type of data.

In implicit typing, the type of a value is determined by the way it is represented in the YAML document. For example, a string that starts with a digit is interpreted as a number, and a string that is enclosed in quotes is interpreted as a string.

In explicit typing, you use tags to specify the type of data you are working with. Tags are added to the value by prefixing it with !, followed by the tag name. For example, the tag !str specifies that the value is a string, while the tag !int specifies that the value is an integer.

Here's an example of implicit typing in YAML:

    {% highlight yaml %}
implicit_typing:
  - 123                     # This is an integer
  - 456.78                  # This is a float
  - true                    # This is a boolean
  - This is a string        # This is a string
  - null                    # This is null
    {% endhighlight %}

And here's an example of explicit typing in YAML:

    {% highlight yaml %}
explicit_typing:
  - !int 123                # This is an integer
  - !float 456.78           # This is an integer
  - !bool true              # This is a boolean
  - !str This is a string   # This is a string
  - !null null              # This is null
    {% endhighlight %}

In general, it's a good idea to use explicit typing in YAML whenever possible, as it makes the data more self-describing and can help to prevent unintended type conversions.

In YAML there are two types of type tags: specific tags and non-specific tags. A specific tag, indicated by an exclamation mark (!), specifies the exact type of a value. For example, the tag !int indicates that the value is an integer, and the tag !float indicates that the value is a floating-point number.

On the other hand, non-specific tags, indicated by a double exclamation mark (!!), provide a more general indication of the type of a value, without specifying the exact type. For example, the tag !!int indicates that the value is some kind of integer, without specifying whether it's a 32-bit integer, a 64-bit integer, or any other type of integer. The exact type of integer is then determined by the parser based on the data itself.

The use of specific tags is generally recommended, as it allows you to explicitly specify the type of a value. This helps to prevent potential type mismatches and makes it easier to understand the structure of the data. 

## Representing Time and Dates in YAML: Understanding Timestamp Formats

Timestamps in YAML are used to represent dates and times. There are several ways to represent timestamps in YAML:

* canonical: 2022-02-05T10:30:00.1Z
* ISO 8601: 2022-02-05t10:30:00.10-05:00
* space sepaarated: 2022-02-05 10:30:00.10 -5
* no time zone (Z): 2022-02-05 10:30:00.10
* date (00:00:00Z): 2022-02-05
* human-friendly: February 5, 2023 12:00 PM

ISO 8601 timestamps are the most common and widely used format for representing timestamps in YAML. They are written in the format YYYY-MM-DDTHH:mm:ss.sssZ, where YYYY represents the year, MM represents the month, DD represents the day, HH represents the hour, mm represents the minute, ss represents the second, sss represents the fractional part of the second, and Z represents the time zone offset. For example, the ISO 8601 timestamp 2023-02-04T12:00:00.000Z represents the time 12:00:00 PM on February 4, 2023 in the UTC zone.

Human-readable timestamp are a more human-friendly representation of timestamps, and can be written in a variety of formats. For example, the human-readable timestamp February 4, 2023 12:00 PM is equivalent to the ISO 8601 timestamp 2023-02-04T12:00:00.000Z.

YAML supports explicit type declaration for date and timestamps, here are some examples:

    {% highlight yaml %}
birthday: !date 2020-10-11
timeoftheday: !timestamp '2023-02-07T08:30:00Z'
    {% endhighlight %}

## Anchors and Aliases in YAML: Reusing Complex Data Structures

YAML allows for the creation of reusable elements through the use of anchors and aliases. An anchor is a label attached to a specific piece of data, and an alias is a reference to that anchor. This allows for the creation of complex data structures with repetitive elements. Anchors and Aliases can be considered if we have repeated sections inside our YAML file. They can reduce effort and make updating in bulk easier. The Aliases essentially act as a "see above" command.

Here's an example of using Anchors and Aliases in YAML:

    {% highlight yaml %}
person: &person
  name: John Doe
  age: 30

other_person: *person
    {% endhighlight %}

In this example, an anchor &person is attached to a dictionary of key-value pairs representing a person. An alias *person is then created to reference this data. The result is two variables, person and other_person, that both refer to the same dictionary of data.

Anchors and aliases are a powerful feature in YAML, allowing for the reuse of complex data structures and reducing the need for duplication in YAML files. They can be especially useful for creating templates or for sharing common data between multiple parts of an application.

Anchors and Aliases cannot contain the "{, }, [. ], ," characters.

## Overriding YAML Values with Anchor and Aliases

YAML provides a way to reuse values through anchors and aliases and to override values using the "<<:" operator. This allows you to define common values in a single place, and then use or override them in different parts of your configuration.

Here's an example to show how you can use anchors and aliases to override values in YAML:

    {% highlight yaml %}
# common values
defaults: &defaults
  color: red
  size: medium

# first configuration
first:
  <<: *defaults
  color: blue

# second configuration
second:
  <<: *defaults
  size: large
    {% endhighlight %}

In this example, the defaults section defines common values for color and size. The first and second sections then use these values with the "<<:" operator and the *defaults alias. The first section overrides the value of the color key, while the second section overrides the value of the size key. The final result would be:

    {% highlight yaml %}
first:
  color: blue
  size: medium

second:
  color: red
  size: large
    {% endhighlight %}

Overriding is also called Merging.

## Multi-Document Support in YAML

YAML supports the concept of multi-document, which allows you to store multiple separate documents in a single YAML file. Each document is separated by "---" on a line by itself and is treated as a separate entity. Optionally, you can use three dots to indicate the end of a YAML document. 

Here's an example to show how you can use multi-document support in YAML:

    {% highlight yaml %}
---
# Document 1
name: John Doe
age: 30
...

---
# Document 2
name: Jane Doe
age: 25
...
    {% endhighlight %}

Some YAML processors require the document start operator. For example, Java's Jackson will not process a YAML document without the start operator, and Python's PyYAML will.

## Complex Keys in YAML

In YAML, you can also use multiline complex keys, which are keys that span multiple lines and are denoted by a ? followed by a space. This type of key is useful when you want to create long and descriptive keys, or when you need to represent nested data structures.

Here's an example of a multiline complex key in YAML:

    {% highlight yaml %}
# Multiline complex key example
?
  This is a complex
  key with multiple
  lines
: value
    {% endhighlight %}

YAML interprets the key as a single line string as follows:

    {% highlight yaml %}
# Multiline complex key example
This is a complex key with multiple lines: value
    {% endhighlight %}

This feature is useful when you want to use more descriptive keys.

## Conclusion

In conclusion, YAML is a highly flexible and readable data serialization format that supports a wide range of advanced features and functionality. From custom data types and complex keys to multi-document support and inheritance with anchors and aliases, YAML provides developers with a powerful tool for representing and exchanging data in a meaningful and concise way. Whether you are working with configuration files, data structures, or even cloud templates, YAML is a versatile and flexible solution that is well worth exploring. By taking the time to learn about its advanced features and functionality, you can leverage the full power of YAML to meet your unique data needs and requirements.

On the Internet there are a lot of tutorials you can use to get more details on YAML files, here few of my favorites:

* [YAML Tutorial: Everything You Need to Know in 5 Mins](https://levelup.gitconnected.com/yaml-tutorial-everything-you-need-to-know-in-5-mins-14f333a23ed1)
* [YAML Tutorial: A Complete Language Guide with Examples](https://spacelift.io/blog/yaml)
* [YAML Basic to Advance](https://medium.com/globant/yaml-basic-to-advance-36a3046e3bf6)



