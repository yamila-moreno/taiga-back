
import pytest
from django.core.urlresolvers import reverse

from rest_framework.renderers import JSONRenderer

from taiga.projects.serializers import ProjectSerializer

from tests import factories as f

import json

pytestmark = pytest.mark.django_db


@pytest.fixture
def data():
    m = type("Models", (object,), {})
    m.registered_user = f.UserFactory.create()
    m.project_member = f.UserFactory.create()
    m.project_owner = f.UserFactory.create()
    m.other_user = f.UserFactory.create()

    m.public_project = f.ProjectFactory(is_private=False,
                                        anon_permissions=['view_project'],
                                        public_permissions=['view_project'])
    m.private_project1 = f.ProjectFactory(is_private=True,
                                          anon_permissions=['view_project'],
                                          public_permissions=['view_project'],
                                          owner=m.project_owner)
    m.private_project2 = f.ProjectFactory(is_private=True,
                                          anon_permissions=['view_project'],
                                          public_permissions=['view_project'],
                                          owner=m.other_user)

    m.membership = f.MembershipFactory(project=m.private_project1,
                                       user=m.project_member,
                                       role__project=m.private_project1)

    return m


def test_roles_retrieve(client, data):
    role_public = f.RoleFactory(project=data.public_project)
    role_private = f.RoleFactory(project=data.private_project1)

    public_url = reverse('roles-detail', kwargs={"pk": role_public.pk})
    private_url = reverse('roles-detail', kwargs={"pk": role_private.pk})

    response = client.get(public_url)
    assert response.status_code == 200
    response = client.get(private_url)
    assert response.status_code == 401

    client.login(data.registered_user)
    response = client.get(public_url)
    assert response.status_code == 200
    response = client.get(private_url)
    assert response.status_code == 403

    client.login(data.project_member)
    response = client.get(public_url)
    assert response.status_code == 200
    response = client.get(private_url)
    assert response.status_code == 200

    client.login(data.project_owner)
    response = client.get(public_url)
    assert response.status_code == 200
    response = client.get(private_url)
    assert response.status_code == 200

# def test_roles_update(client, data):
#     assert False
#
#
def test_roles_delete(client, data):
    role_public = f.RoleFactory(project=data.public_project)
    role_private = f.RoleFactory(project=data.private_project1)

    public_url = reverse('roles-detail', kwargs={"pk": role_public.pk})
    private_url = reverse('roles-detail', kwargs={"pk": role_private.pk})

    response = client.delete(public_url)
    assert response.status_code == 401
    response = client.delete(private_url)
    assert response.status_code == 401

    client.login(data.registered_user)
    response = client.delete(public_url)
    assert response.status_code == 403
    response = client.delete(private_url)
    assert response.status_code == 403

    client.login(data.project_member)
    response = client.delete(public_url)
    assert response.status_code == 403
    response = client.delete(private_url)
    assert response.status_code == 403

    client.login(data.project_owner)
    response = client.delete(public_url)
    assert response.status_code == 403
    response = client.delete(private_url)
    assert response.status_code == 204


def test_roles_list(client, data):
    url = reverse('roles-list')

    role_public = f.RoleFactory(project=data.public_project)
    role_private = f.RoleFactory(project=data.private_project1)

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 1
    assert response.status_code == 200

    client.login(data.registered_user)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 1
    assert response.status_code == 200

    client.login(data.project_member)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 3
    assert response.status_code == 200

    client.login(data.project_owner)
    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 3
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
