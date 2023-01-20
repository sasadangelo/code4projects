---
layout: page
title: Contacts
slug: contacts
excerpt: If you wish to contact Code4Projects author use the following page and fill the contact form included your message for him.
jsscripts_urls:
- https://www.google.com/recaptcha/api.js?hl=it
---
# Contacts

If you wish to contact me, write your message using the following contact form. Remember to enter the required fields: **Your Name**, **Your Email**; and the **Subject** that will help me understand the topic of the message immediately.

Consider that I generally read all the messages that come from this form. If possible, I try to answer within 24 hours. It could happen, however, that for personal problems, for commitments or for other reasons, my answer may arrive a little late. In such cases, I only ask for a little patience because, within the limits of my possibilities, I always try to respond to everyone.

If you wish you can also contact me on the [Linkedin social network](https://www.linkedin.com/in/salvatore-d-angelo-0321851/).

<form class="contact-form" action="https://formspree.io/f/mvongqkp" method="POST">
  <div class="contact-form-item">
  <input type="text" name="name" size="38" placeholder="Your Name" required=""/>
  </div>
  <div class="contact-form-item">
  <input type="email" name="email" size="38" placeholder="Your email (email@domain.tld)" required="">
  </div>
  <div class="contact-form-item">
  <input type="text" name="subject" size="38" placeholder="Subject" required="">
  </div>
  <div class="contact-form-item">
  <textarea name="message" rows="10" cols="30" placeholder="Your Message"></textarea>
  </div>
  <input type="hidden" name="_next" value="{{ site.url }}{{ site.baseurl }}/contacts/">
  <input type="hidden" name="_subject" value="Code4Projects Contact Form Submission">
    <!-- your other form fields go here -->
  <div class="g-recaptcha" data-callback='onSubmit' data-sitekey="6LcTvIAUAAAAAMt-fH4wPnR7T3Sqtn9Ih8tXHNQz"></div>
  <br/>
  <div class="contact-form-item">
  <button type="submit">Send</button>
  </div>
  <br/>
</form>