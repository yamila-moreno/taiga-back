import pytest
from django.core.urlresolvers import reverse

from rest_framework.renderers import JSONRenderer

from taiga.projects.serializers import ProjectSerializer
from taiga.permissions.permissions import MEMBERS_PERMISSIONS

from tests import factories as f

import json

pytestmark = pytest.mark.django_db


def util_test_http_method(client, method, url, data, users):
    results = []
    for user in users:
        if user is None:
            client.logout()
        else:
            client.login(user)
        if data:
            response = getattr(client, method)(url, data, content_type="application/json")
        else:
            response = getattr(client, method)(url)
        results.append(response.status_code)
    return results


@pytest.fixture
def data():
    m = type("Models", (object,), {})
    m.registered_user = f.UserFactory.create()
    m.project_member_with_perms = f.UserFactory.create()
    m.project_member_without_perms = f.UserFactory.create()
    m.project_owner = f.UserFactory.create()
    m.other_user = f.UserFactory.create()

    m.public_project = f.ProjectFactory(is_private=False,
                                        anon_permissions=['view_project'],
                                        public_permissions=['view_project'],
                                        owner=m.project_owner)
    m.private_project1 = f.ProjectFactory(is_private=True,
                                          anon_permissions=['view_project'],
                                          public_permissions=['view_project'],
                                          owner=m.project_owner)
    m.private_project2 = f.ProjectFactory(is_private=True,
                                          anon_permissions=[],
                                          public_permissions=[],
                                          owner=m.project_owner)

    f.RoleFactory(project=m.public_project)

    m.membership = f.MembershipFactory(project=m.private_project1,
                                       user=m.project_member_with_perms,
                                       role__project=m.private_project1,
                                       role__permissions=list(map(lambda x: x[0], MEMBERS_PERMISSIONS)))
    m.membership = f.MembershipFactory(project=m.private_project1,
                                       user=m.project_member_without_perms,
                                       role__project=m.private_project1,
                                       role__permissions=[])
    m.membership = f.MembershipFactory(project=m.private_project2,
                                       user=m.project_member_with_perms,
                                       role__project=m.private_project2,
                                       role__permissions=list(map(lambda x: x[0], MEMBERS_PERMISSIONS)))
    m.membership = f.MembershipFactory(project=m.private_project2,
                                       user=m.project_member_without_perms,
                                       role__project=m.private_project2,
                                       role__permissions=[])

    return m


def test_roles_retrieve(client, data):
    public_url = reverse('roles-detail', kwargs={"pk": data.public_project.roles.all()[0].pk})
    private1_url = reverse('roles-detail', kwargs={"pk": data.private_project1.roles.all()[0].pk})
    private2_url = reverse('roles-detail', kwargs={"pk": data.private_project2.roles.all()[0].pk})

    users = [
        None,
        data.registered_user,
        data.project_member_without_perms,
        data.project_member_with_perms,
        data.project_owner
    ]

    results = util_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private1_url, None, users)
    assert results == [200, 200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private2_url, None, users)
    assert results == [401, 403, 403, 200, 200]

# def test_roles_update(client, data):
#     assert False
#
#
def test_roles_delete(client, data):
    public_url = reverse('roles-detail', kwargs={"pk": data.public_project.roles.all()[0].pk})
    private1_url = reverse('roles-detail', kwargs={"pk": data.private_project1.roles.all()[0].pk})
    private2_url = reverse('roles-detail', kwargs={"pk": data.private_project2.roles.all()[0].pk})

    users = [
        None,
        data.registered_user,
        data.project_member_without_perms,
        data.project_member_with_perms,
        data.project_owner
    ]

    results = util_test_http_method(client, 'delete', public_url, None, users)
    assert results == [401, 403, 403, 403, 204]
    results = util_test_http_method(client, 'delete', private1_url, None, users)
    assert results == [401, 403, 403, 403, 204]
    results = util_test_http_method(client, 'delete', private2_url, None, users)
    assert results == [401, 403, 403, 403, 204]


def test_roles_list(client, data):
    url = reverse('roles-list')

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 3
    assert response.status_code == 200

    client.login(data.registered_user)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 3
    assert response.status_code == 200

    client.login(data.project_member_without_perms)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 5
    assert response.status_code == 200

    client.login(data.project_member_with_perms)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 5
    assert response.status_code == 200

    client.login(data.project_owner)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 5
    assert response.status_code == 200

#
#
# def test_roles_patch(client, data):
#     assert False
#
#
# def test_points_retrieve(client, data):
#     assert False
#
#
# def test_points_update(client, data):
#     assert False
#
#
# def test_points_delete(client, data):
#     assert False
#
#
# def test_points_list(client, data):
#     assert False
#
#
# def test_points_patch(client, data):
#     assert False
#
#
# def test_points_action_bulk_update_order(client, data):
#     assert False
#
#
# def test_user_story_status_retrieve(client, data):
#     assert False
#
#
# def test_user_story_status_update(client, data):
#     assert False
#
#
# def test_user_story_status_delete(client, data):
#     assert False
#
#
# def test_user_story_status_list(client, data):
#     assert False
#
#
# def test_user_story_status_patch(client, data):
#     assert False
#
#
# def test_user_story_status_action_bulk_update_order(client, data):
#     assert False
#
#
# def test_task_status_retrieve(client, data):
#     assert False
#
#
# def test_task_status_update(client, data):
#     assert False
#
#
# def test_task_status_delete(client, data):
#     assert False
#
#
# def test_task_status_list(client, data):
#     assert False
#
#
# def test_task_status_patch(client, data):
#     assert False
#
#
# def test_task_status_action_bulk_update_order(client, data):
#     assert False
#
#
# def test_severity_retrieve(client, data):
#     assert False
#
#
# def test_severity_update(client, data):
#     assert False
#
#
# def test_severity_delete(client, data):
#     assert False
#
#
# def test_severity_list(client, data):
#     assert False
#
#
# def test_severity_patch(client, data):
#     assert False
#
#
# def test_severity_action_bulk_update_order(client, data):
#     assert False
#
#
# def test_priority_retrieve(client, data):
#     assert False
#
#
# def test_priority_update(client, data):
#     assert False
#
#
# def test_priority_delete(client, data):
#     assert False
#
#
# def test_priority_list(client, data):
#     assert False
#
#
# def test_priority_patch(client, data):
#     assert False
#
#
# def test_priority_action_bulk_update_order(client, data):
#     assert False
#
#
# def test_issue_type_retrieve(client, data):
#     assert False
#
#
# def test_issue_type_update(client, data):
#     assert False
#
#
# def test_issue_type_delete(client, data):
#     assert False
#
#
# def test_issue_type_list(client, data):
#     assert False
#
#
# def test_issue_type_patch(client, data):
#     assert False
#
#
# def test_issue_type_action_bulk_update_order(client, data):
#     assert False
#
#
# def test_issue_status_retrieve(client, data):
#     assert False
#
#
# def test_issue_status_update(client, data):
#     assert False
#
#
# def test_issue_status_delete(client, data):
#     assert False
#
#
# def test_issue_status_list(client, data):
#     assert False
#
#
# def test_issue_status_patch(client, data):
#     assert False
#
#
# def test_issue_status_action_bulk_update_order(client, data):
#     assert False
#
#
