# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db.models.loading import get_model
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from taiga.base import exceptions as exc
from .serializers import ResolverSerializer


class ResolverViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        serializer = ResolverSerializer(data=request.QUERY_PARAMS)
        if not serializer.is_valid():
            raise exc.BadRequest(serializer.errors)

        data = serializer.data

        project_model = get_model("projects", "Project")
        project = get_object_or_404(project_model, slug=data["project"])

        result = {
            "project": project.pk
        }

        if data["us"]:
            result["us"] = get_object_or_404(project.user_stories.all(), ref=data["us"]).pk
        if data["task"]:
            result["task"] = get_object_or_404(project.tasks.all(), ref=data["task"]).pk
        if data["issue"]:
            result["issue"] = get_object_or_404(project.issues.all(), ref=data["issue"]).pk
        if data["milestone"]:
            result["milestone"] = get_object_or_404(project.milestones.all(), slug=data["milestone"]).pk

        return Response(result)
