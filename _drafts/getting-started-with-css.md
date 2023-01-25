---
layout: post
title: "Mastering the Basics of CSS: A Beginner's Guide"
slug: mastering-basics-css
thumbnail: assets/img/rds-logo.png
excerpt: bla bla bla
categories:
  - Web Programming
sitemap:
  exclude: 'yes'
---

![Docker]({{ site.baseurl }}/wp-content/uploads/2018/06/Docker-logo.png){:width="258" height="200" .responsive_img}

# Mastering the Basics of CSS: A Beginner's Guide

_Posted on **{{ page.date | date_to_string }}**_

## Introduction

CSS (Cascading Style Sheets) is a styling language used to control the presentation of web pages. It is used to define the layout, colors, typography, and other visual elements of a web page. CSS allows you to separate the presentation of a web page from its structure, which is defined using HTML.

CSS has become an essential part of web development, as it allows you to create visually appealing and responsive designs that adapt to different screen sizes and devices. With CSS, you can control the position and layout of elements, create animations and transitions, and define the typography and colors of a web page.

In this article, we will explore the basics of CSS and how it can be used to enhance the visual design of a web page. We will cover topics such as selectors, cascading, the box model, layout, typography, color and background, transitions and animations, and responsive design. By the end of this article, you will have a solid understanding of how to use CSS to create visually stunning and responsive web pages.

## CSS Selectors and Cascading: The Building Blocks of Web Design

In CSS, selectors are used to select elements on a web page that you want to apply styles to. There are several types of selectors, including:

Element selectors: Select elements based on their tag name, such as "p" for paragraphs or "a" for links.
Class selectors: Select elements based on their class attribute, using a period (.) before the class name. For example, ".my-class" would select all elements with the class "my-class".
ID selectors: Select elements based on their id attribute, using a hash (#) before the id name. For example, "#my-id" would select the element with the id "my-id".
Attribute selectors: Select elements based on their attributes and attribute values. For example, "[href='https://example.com']" would select all elements with an href attribute equal to "https://example.com".
Cascading refers to how styles are applied to elements when multiple stylesheets and/or styles are conflicting. When multiple styles apply to the same element, the browser uses the following rules to determine which style to use:

Specificity: Styles with a higher specificity are given priority. For example, an ID selector has a higher specificity than a class selector.
Origin: Styles that are defined in the user's browser have lower priority than those defined in the author's stylesheet.
Importance: Styles that are marked as "!important" have higher priority than those that are not.
Finally, cascading also works with the order of styles in the CSS file, styles defined later on the file will overwrite previous styles.

It's important to keep in mind that specificity and cascading rules when working with CSS to avoid unexpected results.

Element Selector:

/* This will select all <p> elements and make their text color red */
p {
    color: red;
}

Class selector

/* This will select all elements with the class "my-class" and make their background color yellow */
.my-class {
    background-color: yellow;
}

ID Selector

/* This will select the element with the ID "my-id" and make it's font-size 20px */
#my-id {
    font-size: 20px;
}

Attribute Selector:

/* This will select all <a> elements with an href attribute equal to "https://example.com" and make their text color blue */
a[href='https://example.com'] {
    color: blue;
}

It's also possible to use attribute selectors to match elements with a specific attribute value prefix, suffix, or a substring by using "^", "$", "*" respectively.

/* This will select all <input> elements with a name attribute that starts with "user" and make their border red */
input[name^='user'] {
    border: 1px solid red;
}

It's important to note that attribute selectors are more performance-intensive than the other types of selectors, so it's best to use them sparingly and with caution.

Also, it's good practice to use class and ID selectors to select elements, instead of element selectors because it makes the CSS more reusable and less specific, avoiding the risk of changing the visual of unintended elements.
