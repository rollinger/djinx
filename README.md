# Djxi | **HTMX 4 Integration for Django** 

[![CI](https://github.com/rollinger/djxi/actions/workflows/main.yml/badge.svg)](https://github.com/rollinger/djxi/actions/workflows/main.yml)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)
![Lint](https://img.shields.io/badge/linting-black%2Fruff-blue)
[![codecov](https://codecov.io/gh/rollinger/djxi/branch/master/graph/badge.svg)](https://codecov.io/gh/rollinger/djxi)

[![PyPI](https://img.shields.io/pypi/v/Djxi)](https://pypi.org/project/djxi)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/Djxi)](https://pypi.org/project/djxi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Djxi)](https://pypi.org/project/djxi)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/Djxi)](https://pypi.org/project/djxi)

---

## 📦 What is this?
    Just a prenup between Grandpa Django and his sexy new HTMX fling — preventing scatterbrain syndrome and reactive dysfunction.

Django's API was written with full page reloads in mind. The separation into view, urls and template made sense. 
HTMX introduces partial updates via server-side html snippets that updates the page selectively.
Using Django with HTMX usually results in a scattering of a multitudes of small templates, views and endpoints.
This is bad news for "Locality of Behaviour" and affect maintability of projects the more they make use of HTMX.

### Djxi's solution:
Bundle HTMX urls, views and template collection all into one or more `DXEndpointBattery`. 
```python
from djxi import DXEndpointBattery, dx_action 

INLINE_TEMPLATE = """
<dx-section name="todo-list">
    <div hx-get={% url "load-todo-list" %} hx-trigger="load delay:100ms">
        <h3>TODO</h3>
        <div id="todo-list"></div>
    </div>
</dx-section>

<dx-section name="todo-item">
    <button disabled>Confirmed!</button>
</dx-section>
"""


class SimpleInlineActionRouter(DXEndpointBattery):
    inline_template = INLINE_TEMPLATE

    @dx_action("get-confirm-button", methods=["GET"])
    def get_confirm_button(self, request):
        context = {"name": "Phil"}
        return self.render_section(
            request, section_name="confirm-button", context=context
        )
```
Djxi is a opinionated yet frictionless HTMX drop-in. It can be run in parallel to vanilla Django views or even 
alongside the way you used to use HTMX.

### Inline Templates?

**Stop hunting for HTMX endpoints.**  
Djxi bundles the route, the view logic, and the HTML partial into a single **Endpoint Battery**. 
Drop the `DXEndpointBattery` into your existing Django views or use it standalone. Keep every tiny `hx-*` swap exactly where it lives—without scattering your code across `urls.py`, `views/`, and `templates/`.

- **No more archaeology.** No more digging through three files just to tweak a button label.  
- **LoB, restored.** Request → Logic → Render stays in one atomic, inline hub.  
- **Scales cleanly.** Small partials stay manageable, without turning your project into spaghetti.

Just a prenup between Grandpa Django and his sexy new HTMX fling—keeping your repo clean, one battery at a time.

## Pre-Alpha Note
The package is considered in experimental pre-alpha state, use with caution.
- Watch out for updates and consider giving it a star.
- Checkout the djxi showcases in the example django app.

---

## Getting Started
### Instalation
1) Install with pip:

`python -m pip install djxi`

2) Add django-htmx to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...,
    "djxi",
    ...,
]
```

3) Optional: Adjust your base template to get you up and running instantly
```html
 {% load djxi %}
 <!doctype html>
 <html>
   <head>
     ...
     {% htmx_script_inclusion %}
   </head>
   <body {% htmx_headers %}>
     ...
   </body>
 </html>
```
The htmx_script_inclusion tag will pull the unminified v4 from CDN. Set DX_HTMX_VERSION="2" to pull in v2.
For prodution you likely want to serve your own minified htmx.js.

As there are significant syntax changes between v4 and v2 of htmx, keep DX_HTMX_VERSION in sync with 
what htmx version you are serving.

### Configuration
In your settings file you can overide the following default values for Djxi:
- DX_HTMX_VERSION": "4" # Choose between 4 and 2
- DX_HTMX_MINIFIED": False # Load a minified source, recommended for production

### Quick start
Create and manage your HTMX Endpoint in a convenient Battery:

```python
from djxi.actions import DXEndpointBattery, dx_action 

INLINE_TEMPLATE = """
<dx-section name="confirm-button">
    <button hx-post="/showcase/simple/confirm">
        Confirm, {{ name }}
    </button>
</dx-section>

<dx-section name="check-confirmed">
    <button disabled>Confirmed!</button>
</dx-section>
"""


class SimpleInlineActionRouter(DXEndpointBattery):
    inline_template = INLINE_TEMPLATE

    @dx_action("get-confirm-button", methods=["GET"])
    def get_confirm_button(self, request):
        context = {"name": "Phil"}
        return self.render_section(
            request, section_name="confirm-button", context=context
        )
```