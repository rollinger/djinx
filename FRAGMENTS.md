## 🚀 Installation

### 1. Install via `pip`

If published on PyPI:

```bash
pip install djinx
```

### 2. Add to your Django settings
In settings.py:

```python
INSTALLED_APPS = [
    ...
    "djinx",
]
```

### 3. Override Defaults (optional)
In your project’s settings.py:

```python
DJINX_OPTION = "your_override"
```

# See Also: 
- [HTMX](https://htmx.org/)
- [Django HTMX](https://github.com/adamchainz/django-htmx)

## Ramblings
Django is a powerful web app framework build for reliable backend systems 
while giving you freedom of choice for the frontend. However django frontend 
defaults to server side rendered HTML.

### Why bother?
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

### Proposition
Imagine: 
- you use Django the usual way url->view->template => entire page swap;
- you define an Endpoint Battery bundling related actions, that is htmx endpoints
- the battery has everything in one file: template, route and view logic
- you can mix an endpoint battery into regular Django View upgrading the page with htmx.


### Features
- DjinxViewMixin allows you to 

### Reasons:
#### Make it easier for Django (web 1.0) to integrate with HTMX (web 2.5)
Django is the great, reliable grandpa. Does its thing very well and slow and unsexy.
HTMX is the new sexy, agile but fragmented Post-Grad who likes to hookup with Grandpa.
Djxi is the memorandum of understanding between grandpa and his new crush.
#### Reduce/manage the drag to dispersed partials.
Django 1.0 Templating system alone tends to become unwieldy due to dispersed partials for DRY reasons.
That is made worse by HTMX, since it adds the need to further fragment the html into smaller response snippets.
Djxi introduces inline section templates which bundle a render domain in a single unified document.
#### Unify the Main User Loop in one location (LoB-atomize)
Main User Loop = Request->Route->Logic->Render->Response
Lobatomize: Unify all aspects of the main sequence into ONE atomic hub/file maximizing LoB


Locality of Behaviour is the principle that:

    "The behaviour of a unit of code should be as obvious as possible 
    by looking only at that unit of code"

Base Generic Class Views
See: https://ccbv.co.uk/projects/Django/5.2/django.views.generic.base/View/