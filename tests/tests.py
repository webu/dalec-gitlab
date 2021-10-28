import time

from copy import copy
from django.apps import apps
from django.conf import settings
from django.template.loader import get_template
from django.test import Client
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.timezone import now
from django.urls import reverse

from dalec_gitlab import settings as app_settings
from dalec.proxy import ProxyPool


class DalecGitlabTests(TestCase):
    @property
    def content_model(self):
        return apps.get_model(app_settings.CONTENT_MODEL)

    @property
    def fetch_history_model(self):
        return apps.get_model(app_settings.FETCH_HISTORY_MODEL)
