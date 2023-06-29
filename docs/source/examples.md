# Examples

## Issue
```htmldjango
{% load dalec %}

{% dalec "gitlab" "issue" channel="project" channel_objects='["55", "42"]' %}
```

would return with the default template something like:

---
```{include} examples/issue_default.html
```
---

This is rather simplistic, but with a bit of template overiding and css, you could easily go to this instead:

![](./examples/example_issue_fosm.png)

## Event

```htmldjango
{% load dalec %}

{% dalec "gitlab" "event" channel="project" channel_objects='["42"]' %}
```

would return with the default template something like:

---
```{include} examples/event_default.html
```
---

This is rather simplistic, but with a bit of template overriding and css, you could easily go to this instead:

![](./examples/example_event_fosm.png)
