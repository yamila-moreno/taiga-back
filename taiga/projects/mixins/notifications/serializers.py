# -*- coding: utf-8 -*-

from django.db.models.loading import get_model

from rest_framework import serializers


class WatcherValidationSerializerMixin(object):
    def validate_watchers(self, attrs, source):
        values =  set(attrs.get(source, []))
        if values:
            project = None
            if "project" in attrs and attrs["project"]:
                project = attrs["project"]
            elif self.object:
                project = self.object.project

            model_cls = get_model("projects", "Membership")
            if len(values) != model_cls.objects.filter(project=project, user__in=values).count():
                raise serializers.ValidationError("Error, some watcher user is not a member of the project")
        return attrs
