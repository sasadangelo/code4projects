---
layout: post
title: "Getting Started with HTML: A Beginner's Guide"
slug: getting-started-with-html
thumbnail: assets/img/rds-logo.png
excerpt: In this article, I would like to give you a brief introduction to Kubernetes and how to deploy applications on it.
categories:
  - Web Programming
sitemap:
  exclude: 'yes'
---

![Getting Started with HTML: A Beginner's Guide](assets/img/rds-logo.png){:width="393" height="200" .responsive_img}

# Getting Started with HTML: A Beginner's Guide
_Posted on **{{ page.date | date_to_string }}**_

## What is HTML?

HTML, or Hypertext Markup Language, is a standard markup language used for creating and structuring web pages and applications. It allows developers to define the content and the structure of a web page, including headings, paragraphs, lists, links, and more. HTML is written using a series of tags, which are enclosed in angle brackets and typically come in pairs, with an opening and closing tag. The content of the page goes between the opening and closing tags. For example, the opening tag <p> represents a paragraph, and the closing tag </p> indicates the end of that paragraph. By using HTML, developers can create rich, interactive, and engaging web pages that can be accessed by users across the world.

## A bit of History

HTML was initially developed to provide a way to share scientific research and information over the internet. As the World Wide Web grew in popularity, the need for a more advanced and user-friendly language for creating web pages became evident. Over the years, HTML has undergone several revisions and updates to add new features and capabilities.

Today, HTML is the backbone of the World Wide Web, and almost all websites and web applications use HTML in some form or another. It is a powerful and versatile language that continues to evolve and improve, providing new and exciting ways for developers to create dynamic and interactive web content.

During the years different HTML versions ware released. Here is a brief overview of these versions and the key features and improvements they introduced:

* HTML 1.0: This was the first version of HTML, developed in 1990 by Tim Berners-Lee. It provided a basic set of tags for creating simple web pages, including tags for headings, paragraphs, lists, and links.

* HTML 2.0: This version of HTML was released in 1995 and added support for tables, text formatting, and additional multimedia elements like images and audio files.

* HTML 3.0: The third version of HTML, released in 1997, introduced support for forms, scripts, and other advanced features. It also added support for style sheets, which allowed developers to separate the presentation of a web page from its content.

* HTML 4.0: This version of HTML, released in 1999, added support for more multimedia elements and introduced new tags for creating interactive web applications. It also added support for internationalization and the ability to use XML-based languages like MathML and SVG.

* HTML 5: The latest version of HTML, released in 2014, added many new features and capabilities, including support for video and audio playback, local storage, and offline web applications. It also introduced a new approach to web development called "responsive design", which allows web pages to adapt to different screen sizes and devices.

![HTML History](assets/img/HTML_History.webp){:width="450" height="338" .responsive_img}

These are just a few of the key highlights in the history of HTML. Over the years, the language has continued to evolve and improve, providing new and exciting ways for developers to create dynamic and interactive web content.

The history of HTML, however, has not always been linear. At a certain point, the W3C competition decided to embark on a new path which, over time, has proved unsuccessful. This path involved the development of XHTML as a natural succession of HTML 4.0.

XHTML, which stands for Extensible Hypertext Markup Language, is a markup language that is based on HTML but uses stricter syntax rules. It was developed in the late 1990s as a way to make HTML more consistent and compatible with other XML-based languages.

The first version of XHTML, XHTML 1.0, was released in 2000 and was based on HTML 4.0. It introduced a number of changes to the HTML language, including the use of lowercase tags, the requirement for all tags to be closed, and the requirement to use quotation marks around attribute values.

* XHTML 1.1, released in 2001, added support for additional modules, such as ruby annotations and bidirectional text, and introduced additional rules for creating well-formed documents.

* XHTML 2.0, which was under development for several years but was never completed or released, would have introduced even more significant changes to the HTML language. However, this version of XHTML was eventually abandoned in favor of a new approach called HTML5.

Today, XHTML is not as widely used as it once was, but it continues to be supported by many web browsers and is still used by some developers for creating web pages.

## The HTML Basic structure

A basic HTML document has a very simple structure and consists of the following elements:

* A `DOCTYPE` declaration, which specifies the version of HTML that the document uses.
* An `html` element, which is the root element of the document and encloses all other elements.
* A `head` element, which contains metadata about the document, such as the title, character set, styles, and scripts.
* A `body` element, which contains the main content of the document, such as headings, paragraphs, images, and links.
Here is an example of a basic HTML document:

{% highlight html %}
    <!DOCTYPE html>
    <html>
    <head>
        <title>My web page</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is my first web page.</p>
    </body>
    </html>
{% endhighlight %}

As you can see, the DOCTYPE declaration, the HTML element, the head element, and the body element are all nested within each other, with the DOCTYPE declaration at the top, and the body element at the bottom. The head element contains metadata about the document, and the body element contains the main content.

## HTML Elements, Tags and Attributes

In HTML, elements are the basic building blocks used to create a web page. These elements are represented by tags, which are keywords surrounded by angle brackets. For example, the p tag is used to create a paragraph element, and the h1 tag is used to create a heading element.

Here is an example of a simple HTML tag:

{% highlight html %}
    <p>This is a paragraph.</p>
{% endhighlight %}

In this example, the `<p>` tag is used to mark up a paragraph of text. The `<p>` tag has an opening tag `<p>` and a closing tag `</p>`, with the content in between.

In addition to the basic structure provided by tags, HTML also supports the use of attributes. Attributes are used to provide additional information about an element. They are added to the opening tag of an element and consist of a name and a value, separated by an equals sign. For example, the src attribute is used to specify the source of an image, and the href attribute is used to specify a link.

Here is an example of an HTML tag with an attribute:

{% highlight html %}
    <a href="http://www.example.com">This is a link.</a>
{% endhighlight %}

In this example, the `<a>` tag is used to create a link to another web page. The href attribute is used to specify the URL of the page that the link should go to.

So, to sum up, Elements are used to structure and format the content of a web page. Each Element is enclosed in an open and close Tag. Attributes are used to provide additional information or to modify the behavior of a tag. Together, elements. tags and attributes form the basic building blocks of an HTML document.

## The head tag

The `<head>` element is a container for metadata (data about the document, such as its title, character set, styles, and scripts) in an HTML or XHTML document. The metadata is not displayed on the page, but is used by browsers and search engines to understand the content of the page.

The `<head>` element should be placed at the beginning of the `<html>` element, and must contain a `<title>` element, which specifies the title of the document. The `<head>` element can also include other elements, such as `<style>` for styling the page with CSS, `<link>` for linking to external resources, and `<meta>` for defining metadata, such as the character set, keywords, and description of the page.

Here is an example of a <head> element that includes a <title> element and a <meta> element:

{% highlight html %}
    <head>
        <title>My web page</title>
        <meta charset="utf-8">
    </head>
{% endhighlight %}

As you can see, the `<title>` element appears within the `<head>` element and specifies the title of the page, and the `<meta>` element appears within the `<head>` element and defines the character set of the page.

## The body tag

The `<body>` element is a container for the main content of an HTML or XHTML document. The content of the <body> element is displayed in the main window or viewport of the browser.

The `<body>` element should be placed after the `<head>` element, and can contain any type of content, such as headings, paragraphs, lists, images, links, and more. This content is rendered by the browser according to the styles and layout defined by the document or by external stylesheets.

Here is an example of a `<body>` element that contains a heading and a paragraph:

{% highlight html %}
    <body>
        <h1>Hello, World!</h1>
        <p>This is my first web page.</p>
    </body>
{% endhighlight %}

As you can see, the `<h1>` element and the `<p>` element are nested within the `<body>` element, and their content is displayed on the page. The `<h1>` element represents a heading, and the `<p>` element represents a paragraph.

## Headlines

In HTML, a headline is a piece of text that is used to indicate the importance or relevance of the content that follows. Headlines are typically larger and bolder than the surrounding text, and they may also be styled differently to make them stand out. There are several different levels of headlines in HTML, ranging from level 1 (the most important) to level 6 (the least important). The level of a headline is indicated by the use of a specific HTML tag, such as `<h1>` for a level 1 headline or `<h2>` for a level 2 headline. For example, the following code would create a level 2 headline that says "Introduction":

{% highlight html %}
    <h2>Introduction</h2>
{% endhighlight %}

Headlines are used to organize and structure the content of a webpage, making it easier for readers to navigate and understand the information being presented. They also help search engines understand the hierarchy and organization of a webpage, which can improve its visibility and ranking in search results.

## Paragraphs

In HTML, the <p> tag is used to define a paragraph of text. The <p> tag tells the web browser that the enclosed text should be treated as a paragraph, and it automatically adds some extra space before and after the paragraph to help separate it from other content on the page. The <p> tag is an example of an "inline" element, which means that it can be used within a block-level element such as a <div> or a <section> to add structure and organization to the content of a webpage. Here is an example of how the <p> tag might be used:

{% highlight html %}
    <p>This is the first paragraph of text on the page.</p>
    <p>This is the second paragraph of text on the page.</p>
{% endhighlight %}

In the example above, the first and second paragraphs of text are each enclosed within their own <p> tags. This tells the web browser to treat each paragraph as a distinct block of text, and to add the appropriate amount of space between them. The <p> tag is a very common and useful element in HTML, and it is used on almost every webpage to structure the content and make it easier to read.

## An example of HTML document

Here is an example of how you might use headlines and paragraphs together in an HTML document:

{% highlight html %}
    <h1>Introduction</h1>
    <p>This is the first paragraph of the introduction, which provides a brief overview of the topic.</p>
    <p>This is the second paragraph of the introduction, which expands on the ideas introduced in the first paragraph.</p>
    <h2>Background Information</h2>
    <p>This is the first paragraph of the background section, which provides additional context and detail about the topic.</p>
    <p>This is the second paragraph of the background section, which continues to build on the information from the first paragraph.</p>
    <h3>Key Points</h3>
    <p>This is the first paragraph of the key points section, which summarizes the most important information from the article.</p>
    <p>This is the second paragraph of the key points section, which provides a concise overview of the key ideas discussed in the article.</p>
{% endhighlight %}

In this example, the <h1> tag is used to create a level 1 headline for the introduction, the <h2> tag is used to create a level 2 headline for the background information, and the <h3> tag is used to create a level 3 headline for the key points. Each of these headlines is followed by one or more paragraphs of text, which provide more details and information about the topic. The use of headlines and paragraphs helps to organize the content of the webpage and make it easier for readers to understand and navigate.

## Lorem Ipsum

Lorem Ipsum is a placeholder text that is often used by designers and printers to fill in space in a document or website. It is a dummy text that is used to give an idea of what the final content will look like, without actually having to come up with real content. Lorem Ipsum is a Latin text that was popularized in the 1500s, and is commonly used as dummy text because it has a neutral, unassuming appearance that doesn't distract from the design of the page. Lorem Ipsum is often used as placeholder text in web design, graphic design, and publishing, and is a useful tool for designers and printers to preview what the final content will look like.

## Text Formatting with bold, italic, and underline

Yes, HTML supports several ways to format text, including bold, italic, and underline. Here's how to use each one. To make text bold, you can use the `<strong>` or `<b>` tag. For example:

{% highlight html %}
    <p>This text is <strong>bold</strong></p>
{% endhighlight %}

To make text italic, you can use the `<em>` or `<i>` tag. For example:

{% highlight html %}
    <p>This text is <em>italic</em></p>
{% endhighlight %}

To underline text, you can use the `<u>` tag. For example:

{% highlight html %}
    <p>This text is <u>underlined</u></p>
{% endhighlight %}

It's important to note that these tags are just a way to add formatting to your text. They don't change the meaning of the text itself, and they don't necessarily affect how the text is read by a screen reader or other assistive technology. If you want to convey the meaning or importance of your text, it's often better to use semantic HTML tags like `<strong>` or `<em>` rather than visual tags like `<b>` or `<u>`.

## Links in HTML

A link, or hyperlink, is a way to navigate between web pages on the internet. In HTML, a link is created using the <a> tag, which stands for "anchor". The `<a>` tag is used to define the start and end of a link, and the href attribute is used to specify the destination of the link.

Here's an example of a basic HTML link:

{% highlight html %}
    <a href="https://www.example.com">This is a link</a>
{% endhighlight %}

When this link is clicked, the user's web browser will navigate to the URL specified in the href attribute (in this case, "https://www.example.com"). The text between the <a> and </a> tags (in this case, "This is a link") is what the user will see and click on.

You can also use the target attribute to specify how the link should be opened. For example, you can use target="_blank" to open the link in a new tab or window.

{% highlight html %}
    <a href="https://www.example.com" target="_blank">This is a link that opens in a new tab</a>
{% endhighlight %}

In addition to linking to other web pages, you can also use the <a> tag to create links within the same page. This is known as an "anchor" link, and it's created by using the id attribute to give an element a unique name, and then using that name as the destination of the link.

Here's an example:

{% highlight html %}
    <h1 id="section1">This is a heading</h1>
    <p>Here's a link to <a href="#section1">the heading above</a></p>
{% endhighlight %}

When this link is clicked, the user's web browser will jump to the element with the id of "section1" (in this case, the <h1> heading). This can be useful for creating a table of contents or for allowing users to quickly navigate to different sections of a page.















