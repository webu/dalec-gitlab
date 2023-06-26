# 🦝 dalec-gitlab

[![Stable Version](https://img.shields.io/pypi/v/dalec-gitlab?color=blue)](https://pypi.org/project/dalec-gitlab/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![semver](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)


Django Aggregate a Lot of External Content -- Gitlab

Aggregate last gitlab issue or event from a given gitlab instance.

Plugin of [🤖 dalec](https://github.com/webu/dalec).

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

{% dalec "gitlab" content_type [channel=None] [channel_object=None] [channel_objects=None] [template=None] [ordered_by=None] %}
```

## Real examples

### content_type "issue"

- Available `channel`: `group`, `project`.
- Available `channel_object`: group or project id or public_id
- Available `channel_objects`: list of group or project id or public_id


Retrieves recent gitlab issues for a project:

```django
{% dalec "gitlab" "issue" channel="project" channel_object="14" %}
```

Or for multiple projects at once:

```django
{% dalec "gitlab" "issue" channel="project" channel_objects=["14", "42"] %}
```

### content_type "event"

- Available `channel`: `group`, `project`, `user`.
- Available `channel_object`: group or project id or public_id, or user username
- Available `channel_objects`: list of group or project id or public_id, or user username


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

### content_type "milestone"

- Available `channel`: `group`, `project`.
- Available `channel_object`: group or project id or public_id
- Available `channel_objects`: list of group or project id or public_id

Milestone are retrieve by descending updated date.

Retrieves gitlab milestone for a project or group:
```django
{% dalec "gitlab" "milestone" channel="project" channel_object="14" %}

{% dalec "gitlab" "milestone" channel="group" channel_object="42" %}
```

## Settings

Django settings must define:

  - `DALEC_GITLAB_BASE_URL` : gitlab instance url (ex: `https://gitlab.com/`)
  - `DALEC_GITLAB_API_TOKEN` : gitlab api token (ex: `azeazeaezdfqsmlkrjzr`)


