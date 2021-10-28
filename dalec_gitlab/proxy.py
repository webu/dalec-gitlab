from datetime import timedelta
from typing import Dict
import requests
import urllib.parse

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django.utils.http import urlencode
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

    def _filter_channel(self, channel=None, channel_object=None):
        channel_object = urllib.parse.unquote(channel_object)
        if channel is None:
            channel_retrieved = gl
        elif channel == "user":
            # Users are get via their username
            channel_retrieved = gl.users.list(username=channel_object)[0]
        elif channel == "group":
            # Group are get via their full_path
            try:
                channel_retrieved = gl.groups.get(channel_object)
            except gitlab.exceptions.GitlabGetError:
                raise ValueError(f"Group {channel_object} is not found.")
        elif channel == "project":
            # Project are get via their project_name_with_namespace
            try:
                channel_retrieved = gl.projects.get(channel_object)
            except gitlab.exceptions.GitlabGetError:
                raise ValueError(f"Project {channel_object} is not found.")

        return channel_retrieved

    def _fetch_issue(self, nb, channel=None, channel_object=None):
        options = {"per_page": nb}

        if channel is not None:
            if channel not in ["group", "project"]:
                raise ValueError(
                    """Value `{}` is not a correct value for channel type and Issue. Issue has no meaning
                    for it. It must be either "group" or "project"}
                    """.format(
                        channel
                    )
                )
        else:
            options["scope"] = "all"

        channel_retrieved = self._filter_channel(channel, channel_object)
        issues = channel_retrieved.issues.list(**options)

        contents = {}
        for issue in issues:
            contents[issue.id] = {
                **issue.attributes,
                # id is already in attributes
                "last_update_dt": now(),
                "creation_dt": issue.created_at,
            }
        return contents

    def _fetch_event(self, nb, channel=None, channel_object=None):
        options = {"per_page": nb}

        if channel is not None:
            if channel not in ["group", "project", "user", "issue"]:
                raise ValueError(
                    """Value `{}` is not a correct value for channel type and Event. Event has no meaning
                    for it. It must be either "project", "user" or "issue".
                    """.format(
                        channel
                    )
                )
        else:
            options["scope"] = "all"

        channel_retrieved = self._filter_channel(channel, channel_object)

        if channel == "group":
            events = []
            for project in channel_retrieved.projects.list(all=True):
                p = gl.projects.get(project.id)
                events += p.events.list(**options)
        else:
            events = channel_retrieved.events.list(**options)

        contents = {}
        for event in events:
            contents[event.id] = {
                **event.attributes,
                # id is already in attributes
                "last_update_dt": now(),
                "creation_dt": event.created_at,
            }
        return contents
