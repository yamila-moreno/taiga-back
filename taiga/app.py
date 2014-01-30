# -*- coding: utf-8 -*-

import sys

from django.apps import AppConfig

class TaigaMainConfig(AppConfig):
    name = "taiga"
    verbose_name = "Taiga"

    def ready(self):
        print("Initialize Taiga", file=sys.stderr)
