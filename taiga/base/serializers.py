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

from django.forms import widgets

from rest_framework import serializers

from .neighbors import get_neighbors


class PickleField(serializers.WritableField):
    """
    Pickle objects serializer.
    """
    def to_native(self, obj):
        return obj

    def from_native(self, data):
        return data


class JsonField(serializers.WritableField):
    """
    Json objects serializer.
    """
    widget = widgets.Textarea

    def to_native(self, obj):
        return obj

    def from_native(self, data):
        return data


class PgArrayField(serializers.WritableField):
    """
    PgArray objects serializer.
    """
    widget = widgets.Textarea

    def to_native(self, obj):
        return obj

    def from_native(self, data):
        return data


class NeighborsSerializerMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["neighbors"] = serializers.SerializerMethodField("get_neighbors")

    def serialize_neighbor(self, neighbor):
        raise NotImplementedError

    def get_neighbors(self, obj):
        view, request = self.context.get("view", None), self.context.get("request", None)
        if view and request:
            queryset = view.filter_queryset(view.get_queryset())
            left, right = get_neighbors(obj, results_set=queryset)
        else:
            left = right = None

        return {
            "previous": self.serialize_neighbor(left),
            "next": self.serialize_neighbor(right)
        }
