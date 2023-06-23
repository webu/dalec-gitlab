# Standard libs
import logging
from typing import Dict
import urllib.parse

# Django imports
from django.conf import settings
from django.utils.timezone import now

# DALEC imports
from dalec.proxy import Proxy
import gitlab

logger = logging.getLogger("dalec")

gl = gitlab.Gitlab(settings.DALEC_GITLAB_BASE_URL, private_token=settings.DALEC_GITLAB_API_TOKEN)
gl.auth()


class GitlabProxy(Proxy):
    """
    Gitlab dalec proxy to fetch the last :

    content_type = {"issue", "event", "milestone"}

    For `issue`:
        - channel = {"group", "project"}
        - channel_object = group id or public_id, project id or public_id
    For `event`:
        - channel = {"group", "project", "user"}
        - channel_object = group id or public_id, project id or public_id, or user username
    For `milestone`:
        - channel = {"group", "project"}
        - channel_object = group id or public_id, project id or public_id

    """

    app = "gitlab"

    def _fetch(
        self, nb: int, content_type: str, channel: str, channel_object: str
    ) -> Dict[str, dict]:
        supported_channels = ["issue", "event", "milestone"]

        if content_type not in supported_channels:
            raise ValueError(
                "Invalid content_type `{}`, only {} are supported.".format(
                    content_type,
                    ", ".join(supported_channels),
                )
            )

        return getattr(self, "_fetch_{}".format(content_type))(nb, channel, channel_object)

    def _filter_channel(self, channel=None, channel_object=None):
        if channel_object:
            channel_object = urllib.parse.unquote(channel_object)

        if channel is None:
            channel_retrieved = gl
        elif channel == "user":
            # Users are get via their username
            channel_retrieved = gl.users.list(username=channel_object)[0]
        elif channel == "group":
            # Group are get via their id
            try:
                channel_retrieved = gl.groups.get(channel_object)
            except gitlab.exceptions.GitlabGetError:
                raise ValueError(f"Group {channel_object} is not found.")
        elif channel == "project":
            # Project are get via their id
            try:
                channel_retrieved = gl.projects.get(channel_object)
            except gitlab.exceptions.GitlabGetError:
                raise ValueError(f"Project {channel_object} is not found.")
        else:
            raise ValueError("Value `{}` is not a correct value for channel type.".format(channel))

        return channel_retrieved

    def _fetch_issue(self, nb, channel=None, channel_object=None):
        options = {"per_page": nb}

        if channel is not None:
            if channel not in ["group", "project"]:
                raise ValueError(
                    "Value `{}` is not a correct value for channel type and Issue. Issue has no meaning for it. It must be either `group` or `project` ".format(
                        channel
                    )
                )
        else:
            options["scope"] = "all"

        channel_retrieved = self._filter_channel(channel, channel_object)
        issues = channel_retrieved.issues.list(**options)

        contents = {}
        for issue in issues:
            project = gl.projects.get(issue.project_id).attributes
            id = str(issue.id)
            contents[id] = {
                **issue.attributes,
                "project": {
                    "name": project["name"],
                    "name_with_namespace": project["name_with_namespace"],
                    "path": project["path"],
                    "path_with_namespace": project["path_with_namespace"],
                    "web_url": project["web_url"],
                    "namespace": project["namespace"],
                },
            }
            contents[id].update(
                {
                    "id": id,  # needed otherwise id is an int
                    "last_update_dt": now(),
                    "creation_dt": issue.created_at,
                }
            )
        return contents

    def _fetch_event(self, nb, channel=None, channel_object=None):
        """
        Get the latest event from gitlab.

        If channel is "group", "project" or "user" we retrieve the event belonging to the channel.

        FUTUR:
        If channel is "dashboard", we retrieve event similar to the "/dashboard/activity" of a user (i.e. all activities related to the user, not *from* the user (see https://gitlab.com/gitlab-org/gitlab/-/merge_requests/19816).)
        """
        options = {"per_page": nb}

        if channel is not None:
            if channel not in [
                "group",
                "project",
                "user",
            ]:  # futur: add "dashboard":
                raise ValueError(
                    "Value `{}` is not a correct value for channel type and Event. Event has no meaning for it. It must be either `project`, `user` or `issue`.".format(
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
        # TODO:For futur
        # elif channel == "dashboard":
        #     # specific. We want individual ressources' activity feeds, instead of returning the activity generated by the current user.
        #     # Users are get via their username
        #     user = gl.users.list(username=channel_object)[0]
        #     token_name = "dalec_token_{date}".format(date=now().strftime("%Y%m%d-%H%M.%s"))
        #     i_t = user.impersonationtokens.create({"name": token_name, 'scopes': ["api"]})
        #     user_gl = gitlab.Gitlab(settings.DALEC_GITLAB_BASE_URL, private_token=i_t.token)
        #     events = user_gl.events.list(scope="all")
        #     i_t.delete()
        else:
            events = channel_retrieved.events.list(**options)

        projects = {}
        contents = {}
        for event in events:
            if event.project_id not in projects:
                project = gl.projects.get(event.project_id).attributes
                projects[event.project_id] = project
            else:
                project = projects[event.project_id]

            id = str(event.id)
            contents[id] = {
                **event.attributes,
                "project": {
                    "name": project["name"],
                    "name_with_namespace": project["name_with_namespace"],
                    "path": project["path"],
                    "path_with_namespace": project["path_with_namespace"],
                    "web_url": project["web_url"],
                },
            }
            # Dalec related info
            contents[id].update(
                {
                    "id": id,  # needed otherwise id is a int
                    "last_update_dt": now(),
                    "creation_dt": event.created_at,
                }
            )
        return contents

    def _fetch_milestone(self, nb, channel=None, channel_object=None):
        """Retrieve milestone and associated issues.

        ordering by last updated_at
        """
        # TODO: wait for https://github.com/webu/dalec/issues/4 for custom ordering
        options = {"per_page": nb, "order_by": "updated_at", "sort": "desc"}

        if channel not in ["group", "project"]:
            raise ValueError(
                "Value `{}` is not a correct value for channel type and Milestone. Milestone has no meaning for it. It must be either `project` or `group`.".format(
                    channel
                )
            )

        channel_retrieved = self._filter_channel(channel, channel_object)
        milestones = channel_retrieved.milestones.list(**options)
        contents = {}
        project = channel_retrieved.attributes
        for milestone in milestones:
            milestones_issues = milestone.issues()
            issues = []
            closed_issues = []
            for issue in milestones_issues:
                issues.append(issue.iid)
                if issue.state == "closed":
                    closed_issues.append(issue.iid)
            id = str(milestone.id)

            contents[id] = {
                **milestone.attributes,
                "issues": {
                    "all": issues,
                    "closed": closed_issues,
                    "total_count": len(issues),
                    "closed_count": len(closed_issues),
                },
                "project": {
                    "name": project["name"],
                    "name_with_namespace": project["name_with_namespace"],
                    "path": project["path"],
                    "path_with_namespace": project["path_with_namespace"],
                    "web_url": project["web_url"],
                    "namespace": project["namespace"],
                },
            }
            contents[id].update(
                {
                    "id": id,  # needed otherwise id is a int
                    "last_update_dt": now(),
                    "creation_dt": milestone.created_at,
                }
            )
        return contents
