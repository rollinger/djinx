# Djinx - HTMX Integration for Django
Django is a powerful web app framework build for reliable backend systems 
while giving you freedom of choice for the frontend. However django frontend 
defaults to server side rendered HTML.

## Why bother?
Introducing HTMX into a Django app, is easy and straightforward and works 
well for small injection of `hx-*` into the templates with corresponding views
that handle the request/response cycle.

Once a project grows in size, so do the small endpoints swapping out content buried 
deep in the template hierarchy. The code get messy and hard to maintain because the 
Locality of Behaviour Principle gets very squishy, very fast.

Reading a template.html a developer finds an hx-get pointing to a htmx_route somewhere
in app/urls.py pointing to a htmx_view in app/views/hx_endpoints.py:htmx_view.

This "endpoint hunting" may be justified for a GET the whole page, but for many small 
htmx endpoints this gets chaotic and difficult to maintain.

## Proposition
Imagine: 
- you use Django the usual way url->view->template => entire page swap;
- you define an Endpoint Battery bundling related actions, that is htmx endpoints
- the battery has everything in one file: template, route and view logic
- you can mix an endpoint battery into regular Django View upgrading the page with htmx.


## Features
- DjinxViewMixin allows you to 


Locality of Behaviour is the principle that:

    "The behaviour of a unit of code should be as obvious as possible 
    by looking only at that unit of code"
