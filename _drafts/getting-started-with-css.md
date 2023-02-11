---
layout: post
title: "Mastering the Basics of CSS: A Beginner's Guide"
slug: mastering-basics-css
image: /assets/img/css-logo.webp
excerpt: bla bla bla
categories:
  - Programming
sitemap:
  exclude: 'yes'
---

![CSS Logo]({{ site.baseurl }}/assets/img/css-logo.webp){:width="200" height="200" .responsive_img}

# Mastering the Basics of CSS: A Beginner's Guide

_Posted on **{{ page.date | date_to_string }}**_

## Introduction

CSS (Cascading Style Sheets) is a styling language used to control the presentation of web pages. It is used to define the layout, colors, typography, and other visual elements of a web page. CSS allows you to separate the presentation of a web page from its structure, which is defined using HTML.

CSS has become an essential part of web development, as it allows you to create visually appealing and responsive designs that adapt to different screen sizes and devices. With CSS, you can control the position and layout of elements, create animations and transitions, and define the typography and colors of a web page.

In this article, we will explore the basics of CSS and how it can be used to enhance the visual design of a web page. We will cover topics such as selectors, cascading, the box model, layout, typography, color and background, transitions and animations, and responsive design. By the end of this article, you will have a solid understanding of how to use CSS to create visually stunning and responsive web pages.

## CSS Selectors and Cascading: The Building Blocks of Web Design

In CSS, selectors are used to select elements on a web page that you want to apply styles to. There are several types of selectors, including:

* **Element selectors**: Select elements based on their tag name, such as "p" for paragraphs or "a" for links.
* **Class selectors**: Select elements based on their class attribute, using a period (.) before the class name. For example, ".my-class" would select all elements with the class "my-class".
* **ID selectors**: Select elements based on their id attribute, using a hash (#) before the id name. For example, "#my-id" would select the element with the id "my-id".
* **Attribute selectors**: Select elements based on their attributes and attribute values. For example, "[href='https://example.com']" would select all elements with an href attribute equal to "https://example.com".

Cascading refers to how styles are applied to elements when multiple stylesheets and/or styles are conflicting. When multiple styles apply to the same element, the browser uses the following rules to determine which style to use:

* **Specificity**: Styles with a higher specificity are given priority. For example, an ID selector has a higher specificity than a class selector.
* **Origin**: Styles that are defined in the user's browser have lower priority than those defined in the author's stylesheet.
* **Importance**: Styles that are marked as "!important" have higher priority than those that are not. Finally, cascading also works with the order of styles in the CSS file, styles defined later on the file will overwrite previous styles.

It's important to keep in mind that specificity and cascading rules when working with CSS to avoid unexpected results.

Element Selector:

    {% highlight css %}
/* This will select all <p> elements and make their text color red */
p {
    color: red;
}
    {% endhighlight %}

Class selector

    {% highlight css %}
/* This will select all elements with the class "my-class" and make their background color yellow */
.my-class {
    background-color: yellow;
}
    {% endhighlight %}

ID Selector

    {% highlight css %}
/* This will select the element with the ID "my-id" and make it's font-size 20px */
#my-id {
    font-size: 20px;
}
    {% endhighlight %}

Attribute Selector:

    {% highlight css %}
/* This will select all <a> elements with an href attribute equal to "https://example.com" and make their text color blue */
a[href='https://example.com'] {
    color: blue;
}
    {% endhighlight %}

It's also possible to use attribute selectors to match elements with a specific attribute value prefix, suffix, or a substring by using "^", "$", "*" respectively.

    {% highlight css %}
/* This will select all <input> elements with a name attribute that starts with "user" and make their border red */
input[name^='user'] {
    border: 1px solid red;
}
    {% endhighlight %}

It's important to note that attribute selectors are more performance-intensive than the other types of selectors, so it's best to use them sparingly and with caution.

Also, it's good practice to use class and ID selectors to select elements, instead of element selectors because it makes the CSS more reusable and less specific, avoiding the risk of changing the visual of unintended elements.

## The Box model

The box model is a concept in CSS that describes the layout of an HTML element as a rectangular box. Each box has four main parts: the content, padding, border, and margin.

* **Content**: This is the area where the element's content is displayed, such as text or images.

* **Padding**: This is the space between the content and the border. You can control the padding using the padding property and its related properties such as padding-top, padding-right, padding-bottom, padding-left. 

* **Border**: This is the line that surrounds the padding and content. You can control the border using the border property and its related properties such as border-width, border-color, border-style.

* **Margin**: This is the space outside of the border. You can control the margin using the margin property and its related properties such as margin-top, margin-right, margin-bottom, margin-left.

When you set the width and height of an element, by default, it's the width and height of the content area. However, you can include the padding, border and margin by using the box-sizing property with value "border-box".

    {% highlight css %}
/* This will make the width and height properties include the padding and border */
.my-class {
    box-sizing: border-box;
    width: 200px;
    height: 100px;
    padding: 10px;           # padding-top=padding-bottom=padding-left=padding-right=10px
    border: 1px solid #000;
    margin: 20px 10px;       # margin-top=margin-bottom=20px, margin-left=margin-right=10px
}
    {% endhighlight %}

It's important to understand the box model and how the different parts interact with each other because it affects the layout and spacing of elements on a web page. Additionally, the box-sizing property can be very useful to control the dimensions of an element in a more intuitive way.

The properties width and height express the size of the box.

The box-sizing property in CSS determines how the dimensions of an element are calculated. It specifies whether the width and height of an element should include the border and padding or not.

There are two possible values for box-sizing:

content-box (the default value): the dimensions of an element are determined only by its content, excluding the border and padding.

border-box: the dimensions of an element include both the content and the border and padding.

For example, if you specify a width of 200 pixels for an element with a 10-pixel border and 20-pixel padding, the element will have a total width of 250 pixels with box-sizing: content-box and 200 pixels with box-sizing: border-box.

The box-sizing property can be useful for managing layout issues when working with fixed dimensions, as it allows for a more precise prediction of how spaces will be distributed.

## Layout in CSS

There are several layout techniques that you can use to control the position of elements, such as:

* **display property**: This property is used to specify the type of box an element should generate. The most common values are block, inline, and inline-block. Block elements take up the full width of their parent container, and create a new line after them. Inline elements only take up as much width as their content, and do not create a new line after them. Inline-block elements are similar to inline elements, but they can have dimensions set with width and height properties, and they also create a new line after them.

* **position property**: This property is used to specify the positioning of an element. The possible values are static, relative, absolute, and fixed. Static is the default value, and means that the element will be positioned according to the normal flow of the document. Relative means that the element will be positioned relative to its normal position, using the left, right, top, and bottom properties. Absolute means that the element will be positioned relative to its nearest positioned ancestor, using the same properties. Fixed means that the element will be positioned relative to the viewport, and it will remain in the same position even when the page is scrolled.

* **float property**: This property is used to make an element float to the left or right of its parent container. The possible values are left and right. When an element is floated, it will move to the left or right of its parent container, and other elements will flow around it.

* **flexbox and grid layout**: These are advanced layout techniques that are used to create flexible and responsive layouts. Flexbox is used to create a layout in one dimension, either a row or a column, and grid is used to create a layout in two dimensions, rows and columns. Both flexbox and grid provide powerful layout capabilities that allow you to control the size, alignment, and positioning of elements on a web page in a more flexible and efficient way.

It's important to keep in mind that the layout techniques should be used in a combination to make the layout of a webpage more optimal and adaptable to different viewports. Additionally, it's good practice to use semantic HTML and to style according to the meaning of the elements, as this will make the layout more robust and maintainable.

## Typography in CSS

Typography in CSS refers to the control of the font, size, and spacing of text on a web page. Here are some key concepts in typography:

* **font-family**: This property is used to specify the font for an element. The value can be a specific font name, such as "Arial" or "Times New Roman", or a generic font family, such as "serif" or "sans-serif". It's also possible to specify a list of fonts, in case the first one is not available in the client device, the next one will be used.

* **font-size**: This property is used to specify the size of the text. The value can be specified in different units, such as pixels (px), points (pt), or ems (em).

* **font-weight**: This property is used to specify the boldness of the text. The possible values are normal and bold. It's also possible to use numeric values from 100 to 900, where 400 is the same as normal and 700 is the same as bold.

* **line-height**: This property is used to specify the spacing between lines of text. The value can be specified in different units, such as pixels or ems.

* **letter-spacing** and **word-spacing**: These properties are used to specify the spacing between letters and words, respectively. The value can be specified in different units, such as pixels or ems.

* **text-align**: This property is used to specify the alignment of text within an element. The possible values are left, right, center, and justify.

* **text-transform**: This property is used to specify the capitalization of text. The possible values are none, uppercase, lowercase, and capitalize.

* **text-decoration**: This property is used to specify the decoration of text. The possible values are none, underline, overline, line-through, and blink (this one is not widely supported, use it with caution)

It's important to keep in mind that typography is an important aspect of web design, and it can greatly impact the readability and aesthetics of a web page. Additionally, it's good practice to use web-safe fonts and consider the accessibility guidelines when choosing the font family and size to ensure that the text is legible for users with visual impairments.

##  Color and background in CSS

Color and background in CSS refer to the control of the color and background of elements on a web page. Here are some key concepts in color and background:

color: This property is used to specify the text color of an element. The value can be specified in several ways, such as using color names (e.g. "red"), RGB values (e.g. "rgb(255, 0, 0)"), or hexadecimal values (e.g. "#ff0000").

background-color: This property is used to specify the background color of an element. The value can be specified in the same ways as the color property.

background-image: This property is used to specify an image as the background of an element. The value is the URL of the image file.

background-repeat: This property is used to specify how the background image should be repeated. The possible values are repeat, repeat-x, repeat-y, and no-repeat.

background-position: This property is used to specify the position of the background image. The value can be specified in several ways, such as using keywords (e.g. "center"), length units (e.g. "10px 20px"), or percentages (e.g. "50% 50%").

background-size: This property is used to specify the size of the background image. The value can be specified in several ways, such as using keywords (e.g. "cover"), length units (e.g. "200px 100px"), or percentages (e.g. "50% 50%").

background-clip and background-origin : These properties are used to specify the area where the background image and color should be applied. The possible values of background-clip are border-box, padding-box and content-box, and the possible values of background-origin are padding-box and content-box.

It's important to keep in mind that color and background can greatly impact the aesthetics of a web page, and they should be used in a harmonious way to create a visually pleasing design. Also, it's good practice to consider the accessibility guidelines when choosing the color combinations and contrasts to ensure that the text is legible for users with visual impairments.

## Transitions and animations in CSS

Transitions and animations in CSS are used to create smooth and fluid visual effects when elements change their state.

transition: This property is used to specify the transition effect that should be applied to an element when its state changes. The property takes several values, such as the property that will be transitioned (e.g. "color"), the duration of the transition (e.g. "1s"), the timing function (e.g. "ease-in-out"), and the delay before the transition starts (e.g. "0.5s").

    {% highlight css %}
/* This will make the transition of the color property to last 1 second, with an ease-in-out timing function and a delay of 0.5s */
.my-class {
    transition: color 1s ease-in-out 0.5s;
}
    {% endhighlight %}

animation: This property is used to specify a series of keyframes that define the animation effect. The property takes several values, such as the name of the animation (e.g. "my-animation"), the duration of the animation (e.g. "1s"), the timing function (e.g. "ease-in-out"), the number of times the animation should be played (e.g. "infinite"), and the delay before the animation starts (e.g. "0.5s").

    {% highlight css %}
/* This will make the animation to be named 'my-animation', last 1 second, with an ease-in-out timing function, to be played infinite times and a delay of 0.5s */
.my-class {
    animation: my-animation 1s ease-in-out infinite 0.5s;
}
    {% endhighlight %}

The keyframes need to be defined separately, usually in a different css file or in a <style> tag. The keyframes rule is used to define the styles that the animation should have at different points in time.

    {% highlight css %}
@keyframes my-animation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
    {% endhighlight %}

This animation will rotate the element from 0degrees to 360degrees in 1 second, with an ease-in-out timing function, and will repeat infinitely with a delay of 0.5s.

It's important to keep in mind that transitions and animations can greatly enhance the user experience and make a web page more interactive. However, it's good practice to use them in a subtle and appropriate way, to avoid overwhelming the user and to make sure that the animation does not interfere with the functionality of the page.

## Responsive design in CSS

Responsive design in CSS is used to create web pages that adapt to different screen sizes and resolutions. The main idea behind responsive design is to use flexible grids, flexible images, and media queries to create a layout that adjusts to the size of the viewport.

media queries: This is a CSS technique that allows you to apply different styles based on the characteristics of the device and the viewport. Media queries use a set of CSS rules that are only applied when certain conditions are met, such as the width or height of the viewport, the resolution of the screen, or the type of device.

    {% highlight css %}
/* This media query will apply the styles inside of it when the width of the viewport is less than 600px */
@media only screen and (max-width: 600px) {
    /* styles go here */
}
    {% endhighlight %}

flexbox and grid layout: These layout techniques are very useful for responsive design because they allow you to create flexible and adaptive layouts that adjust to the size of the viewport. Flexbox is used to create a layout in one dimension, either a row or a column, and grid is used to create a layout in two dimensions, rows and columns.

viewport: This is the area of the browser window where the web page is displayed. The viewport can be controlled using the viewport meta tag, this will allows you to set the width and initial scale of the viewport, and it will affect the layout of the page and the sizes of elements on the page.

    {% highlight css %}
<meta name="viewport" content="width=device-width, initial-scale=1">
    {% endhighlight %}

It's important to keep in mind that responsive design is crucial for creating a good user experience in today's web, where people access the internet from a wide range of devices and screen sizes. Additionally, it's good practice to test the layout on different devices and screen sizes during the development process to ensure that the layout is consistent and adaptable across different platforms.