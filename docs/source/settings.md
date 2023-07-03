# Settings

## Mandatory settings

Django settings must define:

  - `DALEC_GITLAB_BASE_URL` : gitlab instance url (ex: `https://gitlab.com/`)
  - `DALEC_GITLAB_API_TOKEN` : gitlab api token (ex: `azeazeaezdfqsmlkrjzr`)


## Extra settings

But extra settings can also be defined as well, following the DALEC settings method, that overide generic value if specified:

- `DALEC_GITLAB_ISSUE_NB_CONTENT` : number of content per issue
- `DALEC_GITLAB_EVENT_NB_CONTENT` : number of content per event
- `DALEC_GITLAB_MILESTONE_NB_CONTENT` : number of content per milestone

