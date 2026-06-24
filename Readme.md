# Djinx

![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)

**Django - HTMX Integration**

---

## 📦 What is this?

**Djinx** is a Django package that provides seamless integration between Django form widgets and [HTMX](https://htmx.org/). It aims to reduce boilerplate and promote clean, component-like behavior in your views and templates.

Use it to:
- Add HTMX behavior to Django view declaratively.
- Simplify progressive enhancement in your app.
- Avoid repetitive HTML/JS when building dynamic, interactive UIs.

---

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
