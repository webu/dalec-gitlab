from datetime import timedelta
from typing import Dict
import requests

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django.conf import settings

from dalec.proxy import Proxy

import gitlab

gl = gitlab.Gitlab(settings.DALEC_GITLAB_BASE_URL, private_token=settings.DALEC_GITLAB_API_TOKEN)
gl.auth()


class GitlabProxy(Proxy):
    """
    Gitlab dalec proxy to fetch the last :
    * issue:
    * event:
    """

    app = "gitlab"

    def _fetch(
        self, nb: int, content_type: str, channel: str, channel_object: str
    ) -> Dict[str, dict]:
        if content_type == "issue":
            return self._fetch_issue(nb, channel, channel_object)
        if content_type == "event":
            return self._fetch_event(nb, channel, channel_object)

        raise ValueError("Invalid content_type %s" % content_type)

    def _filter_channel(channel=None, channel_object=None):
        if channel is None:
            channel_retrieved = gl
        elif channel == "user":
            channel_retrieved = gl.users.get(channel_object)
        elif channel == "group":
            channel_retrieved = gl.groups.get(channel_object)
        elif channel == "project":
            channel_retrieved = gl.projects.get(channel_object)

        return channel_retrieved

    def _fetch_issue(self, nb, channel=None, channel_object=None):
        options = {"per_page": nb}

        if channel is not None:
            if channel not in ["group", "project"]:
                raise ValueError(
                    """Value `{}` is not a correct value for channel type and Issue. Issue has no meaning
                    for it. It must be either {group, project}
                    """.format(
                        channel
                    )
                )
        else:
            options["scope"] = "all"

        channel_retrieved = _filter_channel(channel, channel_object)
        issues = channel_retrieved.issues.list(**options)

        contents = {}
        for issue in issues:
            contents[id] = {
                **issue.attributes,
                # id is already in attributes
                "last_update_dt": now(),
                "creation_dt": issue.created_at,
            }
        return contents

    def _fetch_event(self, nb, channel=None, channel_object=None):
        options = {"per_page": nb}

        if channel is not None:
            if channel not in ["project", "user", "issue"]:
                raise ValueError(
                    """Value `{}` is not a correct value for channel type and Event. Event has no meaning
                    for it. It must be either {project, user, issue}
                    """.format(
                        channel
                    )
                )
        else:
            options["scope"] = "all"

        channel_retrieved = _filter_channel(channel, channel_object)
        events = channel_retrieved.events.list(**options)

        contents = {}
        for event in events:
            contents[id] = {
                **event.attributes,
                # id is already in attributes
                "last_update_dt": now(),
                "creation_dt": event.created_at,
            }
        return contents
