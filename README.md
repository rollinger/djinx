# Djxi | **HTMX Integration for Django** 
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)

---

## 📦 What is this?

**Stop hunting for HTMX endpoints.**  
Djxi bundles the route, the view logic, and the HTML partial into a single **Endpoint Battery**. 
Drop the `DxActionRouter` into your existing Django views or use it standalone. Keep every tiny `hx-*` swap exactly where it lives—without scattering your code across `urls.py`, `views/`, and `templates/`.

- **No more archaeology.** No more digging through three files just to tweak a button label.  
- **LoB, restored.** Request → Logic → Render stays in one atomic, inline hub.  
- **Scales cleanly.** Small partials stay manageable, without turning your project into spaghetti.

Just a prenup between Grandpa Django and his sexy new HTMX fling—keeping your repo clean, one battery at a time.

## Pre-Alpha Note
The package is not yet published and considered in experimental pre-alpha state.
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

3) Optional: Adjust your base template or setup HTMX manually
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
You can choose to include the htmx script yourself and set the hx-headers to your liking.

### Configuration
In your settings file you can overide the following default values for Djxi:
- DX_HTMX_VERSION": "4" # Choose between 4 and 2
- DX_HTMX_MINIFIED": False # Load a minified source, recommended for production

### Quick start
Create and manage your HTMX Endpoint in a convenient Battery:

```python
from djxi.actions import DxActionRouter, dx_route

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

class SimpleInlineActionRouter(DxActionRouter):
    inline_template = INLINE_TEMPLATE
    
    @dx_route("get-confirm-button", methods=["GET"])
    def get_confirm_button(self, request):
        context = {"name": "Phil"}
        return self.render_section(
            request, section_name="confirm-button", context=context
        )
```