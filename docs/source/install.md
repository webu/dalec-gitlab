# Installation & Usage

See also [the main dalec](https://github.com/webu/dalec) repository for more information.

## Python & django setup

Install the package or set it in your requirement:

```
pip install dalec_gitlab
```

In django settings `INSTALLED_APPS`, add:

```
INSTALLED_APPS = [
    ...
    "dalec",
    "dalec_prime",
    "dalec_gitlab",
    ...
    ]
```

Run `django-admin makemigrations` and `django-admin migrate` if this is the first dalec plugin installed.

Add also in your settings the gitlab server URL and token:

```
DALEC_GITLAB_BASE_URL = "https://gitlab.com/"
DALEC_GITLAB_API_TOKEN = "azeazeaezdfqsmlkrjzr"
```

## Usage

General usage: in a template

```django
{% load dalec %}

{% dalec "gitlab" content_type [channel=None] [channel_object=None] [channel_objects=None] [template=None] [ordered_by=None] %}
```

where `content_type` can be: `issue`, `event` or `milestone`.

## Extending the default templates

Default templates are rather simplistic (see [examples](examples)). But you can easily create your own template, like every other dalec:

- list (don't forget to extend `dalec/default/list.html`):
    * `dalec/gitlab/issue-list.html`
    * `dalec/gitlab/event-list.html`
    * `dalec/gitlab/milestone-list.html`
- item (don't forget to extend `dalec/default/item.html`):
    * `dalec/gitlab/issue-item.html`
    * `dalec/gitlab/event-item.html`
    * `dalec/gitlab/milestone-item.html`


It should be straightforward to create your own (see [Content data](content_data) for available data). Here for instance the default one for issue:

**Issue list** : simply redifine the block `dalec_list_items`
```{literalinclude} ../../dalec_gitlab/templates/dalec/gitlab/issue-list.html
:language: htmldjango
```
**Issue item** : simply load `{% load dalec %}` (if needed, for instance for the `|to_datetime` filter) and redifine the block `item_content`
```{literalinclude} ../../dalec_gitlab/templates/dalec/gitlab/issue-item.html
:language: htmldjango
```

