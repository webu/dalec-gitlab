# Content returned by dalec_gitlab

Every dalec save in database object with the following attributes:

 - `last_update_dt` 
 - `creation_dt` 
 - `app` 
 - `content_type` 
 - `channel` 
 - `channel_object` 
 - `dj_channel_content_type_id`
 - `dj_channel_id`
 - `dj_content_content_type_id`
 - `dj_content_id`
 - `content_id`
 - `content_data`

See [the main dalec](https://github.com/webu/dalec) repository for more information.
Hereafter are detailed the `content_data`, specific to the `gitlab` content type.

## Issue

```json
{
  "id": "2",
  "iid": 1,
  "type": "ISSUE",
  "state": "opened",
  "title": "Ex-ter-minate",
  "_links": {
    "self": "https://gitlab.dalec.who/api/v4/projects/42/issues/1",
    "notes": "https://gitlab.dalec.who/api/v4/projects/42/issues/1/notes",
    "project": "https://gitlab.dalec.who/api/v4/projects/42",
    "award_emoji": "https://gitlab.dalec.who/api/v4/projects/42/issues/1/award_emoji",
    "closed_as_duplicate_of": null
  },
  "author": {
    "id": 666,
    "name": "Dalec",
    "state": "active",
    "web_url": "https://gitlab.dalec.who/dalec",
    "username": "dalec",
    "avatar_url": null
  },
  "labels": [],
  "project": {
    "name": "extermination",
    "path": "extermination",
    "web_url": "https://gitlab.dalec.who/p/ORDER55/extermination",
    "namespace": {
      "id": 55,
      "kind": "group",
      "name": "Extermination project name !",
      "path": "ORDER55",
      "web_url": "https://gitlab.dalec.who/groups/p/ORDER55",
      "full_path": "p/ORDER55",
      "parent_id": 221,
      "avatar_url": "/uploads/-/system/group/avatar/55/avatar.png"
    },
    "name_with_namespace": "Projects / Order 55 / extermination",
    "path_with_namespace": "p/ORDER55/extermination"
  },
  "upvotes": 0,
  "web_url": "https://gitlab.dalec.who/p/ORDER55/extermination/-/issues/1",
  "assignee": {
    "id": 555,
    "name": "Doc Who",
    "state": "active",
    "web_url": "https://gitlab.dalec.who/docwho",
    "username": "docwho",
    "avatar_url": "https://gitlab.dalec.who/uploads/-/system/user/avatar/555/avatar.png"
  },
  "due_date": null,
  "group_id": "55",
  "severity": "UNKNOWN",
  "assignees": [
    {
      "id": 555,
      "name": "Doc Who",
      "state": "active",
      "web_url": "https://gitlab.dalec.who/docwho",
      "username": "docwho",
      "avatar_url": "https://gitlab.dalec.who/uploads/-/system/user/avatar/555/avatar.png"
    }
  ],
  "closed_at": null,
  "closed_by": null,
  "downvotes": 0,
  "has_tasks": false,
  "milestone": null,
  "created_at": "2019-10-02T09:56:40.296Z",
  "issue_type": "issue",
  "project_id": 42,
  "references": {
    "full": "p/ORDER55/extermination#1",
    "short": "#1",
    "relative": "extermination#1"
  },
  "time_stats": {
    "time_estimate": 0,
    "total_time_spent": 0,
    "human_time_estimate": null,
    "human_total_time_spent": null
  },
  "updated_at": "2019-10-02T09:56:40.296Z",
  "creation_dt": "2019-10-02T09:56:40.296Z",
  "description": "",
  "moved_to_id": null,
  "confidential": false,
  "last_update_dt": "2023-06-23T11:12:13.375Z",
  "user_notes_count": 0,
  "discussion_locked": null,
  "merge_requests_count": 0,
  "service_desk_reply_to": null,
  "task_completion_status": {
    "count": 0,
    "completed_count": 0
  }
}
```

## Event

```json
{
  "id": "84",
  "author": {
    "id": 555,
    "name": "Doc Who",
    "state": "active",
    "web_url": "https://gitlab.dalec.who/docwho",
    "username": "docwho",
    "avatar_url": "https://gitlab.dalec.who/uploads/-/system/user/avatar/555/avatar.png"
  },
  "project": {
    "name": "extermination",
    "path": "extermination",
    "web_url": "https://gitlab.dalec.who/p/ORDER55/extermination",
    "name_with_namespace": "Projects / Order 55 / extermination",
    "path_with_namespace": "p/ORDER55/extermination"
  },
  "author_id": 555,
  "push_data": {
    "ref": "0.1.0",
    "action": "created",
    "ref_type": "tag",
    "commit_to": "659ca11c3841add96551716af69c9f866afdf527",
    "ref_count": null,
    "commit_from": null,
    "commit_count": 1,
    "commit_title": "howto: ext-er-minate jedi"
  },
  "target_id": null,
  "created_at": "2021-01-27T13:33:27.201Z",
  "project_id": 42,
  "target_iid": null,
  "action_name": "pushed new",
  "creation_dt": "2021-01-27T13:33:27.201Z",
  "target_type": null,
  "target_title": null,
  "last_update_dt": "2023-06-23T11:12:14.461Z",
  "author_username": "docwho"
}
```

## Milestone

TODO
