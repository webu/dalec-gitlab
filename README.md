# dalec-gitlab

Django Aggregate a Lot of External Content -- Gitlab

Aggregate last gitlab issue or event from a given gitlab instance.

Plugin of [dalec](https://dev.webu.coop/w/i/dalec).

## Installation

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


## Usage

General usage: in a template

```django
{% load dalec %}

{% dalec "gitlab" content_type [channel=None] [channel_object=None] [template=None] %}
```

## Real examples

### content_type "issue"

- Available `channel`: `group`, `project`.
- Available `channel_object`: group or project id or public_id


Retrieves recent gitlab issues for a project:

```django
{% dalec "gitlab" "issue" channel="project" channel_object="14" %}
```

### content_type "event"

- Available `channel`: `group`, `project`, `user`.
- Available `channel_object`: group or project id or public_id, or user username


Retrieves recent gitlab activity for a user:

```django
{% dalec "gitlab" "event" channel="user" channel_object="doctor-who" %}
```

Retrieves recent gitlab activity for a group:

```django
{% dalec "gitlab" "event" channel="group" channel_object="42" %}
```

Retrieves recent gitlab activity for a project:

```django
{% dalec "gitlab" "event" channel="project" channel_object="512" %}
```

## Settings

Django settings must define:

  - `GITLAB_BASE_URL` : gitlab instance url (ex: `https://gitlab.com/`)
  - `GITLAB_API_TOKEN` : gitlab api token (ex: `azeazeaezdfqsmlkrjzr`)


