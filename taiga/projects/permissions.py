# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be> # Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
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


from taiga.base.permissions import BasePermission

from taiga.base.api.permissions import (ResourcePermission, HasProjectPerm,
                                        IsAuthenticated, IsProjectOwner, AllowAny)


class ProjectPermission(ResourcePermission):
    retrieve_perms = HasProjectPerm('view_project')
    create_perms = IsAuthenticated()
    update_perms = IsProjectOwner()
    destroy_perms = IsProjectOwner()
    list_perms = AllowAny()
    stats_perms = AllowAny()
    star_perms = IsAuthenticated()
    unstar_perms = IsAuthenticated()
    issues_stats_perms = AllowAny()
    issues_filters_data_perms = AllowAny()
    tags_perms = AllowAny()


class MembershipPermission(BasePermission):
    get_permission = "view_membership"
    post_permission = "add_membership"
    put_permission = "change_membership"
    patch_permission = "change_membership"
    delete_permission = "delete_membership"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


# User Stories

class PointsPermission(ResourcePermission):
    retrieve_perms = HasProjectPerm('view_project')
    create_perms = IsProjectOwner()
    update_perms = IsProjectOwner()
    destroy_perms = IsProjectOwner()
    list_perms = AllowAny()


class UserStoryStatusPermission(BasePermission):
    get_permission = "view_userstorystatus"
    post_permission = "add_userstorystatus"
    put_permission = "change_userstorystatus"
    patch_permission = "change_userstorystatus"
    delete_permission = "delete_userstorystatus"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


# Tasks

class TaskStatusPermission(BasePermission):
    get_permission = "view_taskstatus"
    post_permission = "ade_taskstatus"
    put_permission = "change_taskstatus"
    patch_permission = "change_taskstatus"
    delete_permission = "delete_taskstatus"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


# Issues

class SeverityPermission(BasePermission):
    get_permission = "view_severity"
    post_permission = "add_severity"
    put_permission = "change_severity"
    patch_permission = "change_severity"
    delete_permission = "delete_severity"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


class PriorityPermission(BasePermission):
    get_permission = "view_priority"
    post_permission = "add_priority"
    put_permission = "change_priority"
    patch_permission = "change_priority"
    delete_permission = "delete_priority"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


class IssueStatusPermission(BasePermission):
    get_permission = "view_issuestatus"
    post_permission = "add_issuestatus"
    put_permission = "change_issuestatus"
    patch_permission = "change_issuestatus"
    delete_permission = "delete_issuestatus"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


class IssueTypePermission(BasePermission):
    get_permission = "view_issuetype"
    post_permission = "add_issuetype"
    put_permission = "change_issuetype"
    patch_permission = "change_issuetype"
    delete_permission = "delete_issuetype"
    safe_methods = ["HEAD", "OPTIONS"]
    path_to_project =  ["project"]


class RolesPermission(ResourcePermission):
    retrieve_perms = HasProjectPerm('view_project')
    create_perms = IsProjectOwner()
    update_perms = IsProjectOwner()
    destroy_perms = IsProjectOwner()
    list_perms = AllowAny()


# Project Templates

class ProjectTemplatePermission(BasePermission):
    # TODO: should be improved in permissions refactor
    pass
