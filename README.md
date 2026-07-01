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

**Stop scrolling for scattered HTMX!**

Djxi lets you architect your HTMX widgets in one single **Endpoint Battery**. It bundles the urls, view logic, and the HTML into a central hub. The feature lives in one place — without scattering your code across `urls`, `views`, and `templates`.

- **No more archaeology.** No more digging through three files just to tweak a button label.  
- **Locality of Behaviour** Request → Logic → Render stays in one class.  
- **Scales cleanly.** Small partials stay manageable, without turning your project into spaghetti.
- **Django Integration.** Tags, Filters, Messages, HX-Headers, CBV and more are frictionless integrated. 

## 📦 What is this?
    Just a prenup between Grandpa Django and his sexy new HTMX fling — 
    preventing scatterbrain syndrome and reactive dysfunction.

Django's Request-Render-Response cycle was architected with full page reloads in mind. The separation into views, urls and templates is practical when the response affect the whole of the client's state.

HTMX introduces minute partial updates via server-side rendered html snippets which update the page selectively and asynchronly. Those small page updates have to be orchestrated and maintained, each with its own view, url and template.

Using Django with HTMX usually results in a scattering of a multitude of template snippest, view logics and url endpoints.

Consider a simple CRUD Todo List: that is 4 urls, 4 views and 5 templates, if you do it with HTMX and create a partial for a todo item. This count can easily go up, as soon as the urge to allow in-place smart actions is given in. The number is not the problem it is the scattering of those snippets (url, view, html) over the codebase under vanilla Django best practices.

Therefore the marriage of Django and HTMX can be bad news for [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/) and affect maintability of projects the more it make use of HTMX.

### Djxi's solution:
Bundle HTMX urls, views and template collection all into one or more `DXEndpointBattery`. Here the 'todo-list' feature with all it's actions is described in full in one place and obvious at a glace.
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
Djxi is an opinionated and frictionless HTMX drop-in. It can be run in parallel to vanilla Django views and even 
alongside the way you used to use HTMX.

`pip install djxi` and streamline new and old HTMX functionalities.

### Inline Templates?
    HTML in a multiline string? Bäh, I loose all the template syntax higllighting!

No problem at all! Just use the `template_name` with a path to your template instead of the `inline_template`. You can deal with two files per feature set!

### Spice up Django CBV
### Integrate with django.contrib.messages
### Expose HX-Headers per middleware


**Pre-Alpha Note**
The package is considered in pre-alpha state, use with as an experimental package.
- Happy to hear from you if you like to contribute to the project.
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

As there are significant syntax changes between v4 and v2 of htmx, keep DX_HTMX_VERSION in sync with what htmx version you are using.

### Configuration
In your settings file you can overide the following default values for Djxi:
- **DX_HTMX_VERSION**: "4" # allow ['2', '4']
- **DX_HTMX_COMPRESSION**: ".js"  # allow: ['.js','.min.js']
- **DX_SECTION_TAG**: "dx-section" # html tag to delineate html snippets

## FAQ
- **Why HTMX 4** Djxi defaults to HTMX 4 as it is the up and comming iteration on version 2, with many changes and improvement. While it works with HTMX 2 as well, in the future Djxi may drop support for HTMX 2.