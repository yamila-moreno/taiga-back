import pytest
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from taiga.projects.api import ProjectViewSet
from taiga.projects.models import Project
from taiga.users.models import User

from tests import factories as f

import json

pytestmark = pytest.mark.django_db


@pytest.fixture
def data():
    registered_user = f.UserFactory.create()
    project_member = f.UserFactory.create()
    project_owner = f.UserFactory.create()
    other_user = f.UserFactory.create()

    public_project = f.ProjectFactory.create(is_private=False,
                                             anon_permissions=['view_project'],
                                             public_permissions=['view_project'])
    private_project1 = f.ProjectFactory.create(is_private=True,
                                              anon_permissions=['view_project'],
                                              public_permissions=['view_project'],
                                              owner=project_owner)
    private_project2 = f.ProjectFactory.create(is_private=True,
                                              anon_permissions=['view_project'],
                                              public_permissions=['view_project'],
                                              owner=other_user)

    f.MembershipFactory.create(project=private_project1, user=project_member)

    return {
        "registered_user": registered_user,
        "project_member": project_member,
        "project_owner": project_owner,
        "public_project": public_project,
        "private_project1": private_project1,
        "private_project2": private_project2,
    }


def test_project_retrieve(client, data):
    public_url = reverse('projects-detail', kwargs={"pk": data['public_project'].pk})
    private_url = reverse('projects-detail', kwargs={"pk": data['private_project1'].pk})

    response = client.get(public_url)
    project_data = json.loads(response.content.decode('utf-8'))
    assert project_data['is_private'] == False
    assert response.status_code == 200

    response = client.get(private_url)
    assert response.status_code == 401

    client.login(data['registered_user'])

    response = client.get(public_url)
    project_data = json.loads(response.content.decode('utf-8'))
    assert project_data['is_private'] == False
    assert response.status_code == 200

    response = client.get(private_url)
    assert response.status_code == 403

    client.login(data['project_member'])

    response = client.get(public_url)
    project_data = json.loads(response.content.decode('utf-8'))
    assert project_data['is_private'] == False
    assert response.status_code == 200

    response = client.get(private_url)
    project_data = json.loads(response.content.decode('utf-8'))
    assert project_data['is_private'] == True
    assert response.status_code == 200

    client.login(data['project_owner'])

    response = client.get(public_url)
    project_data = json.loads(response.content.decode('utf-8'))
    assert project_data['is_private'] == False
    assert response.status_code == 200

    response = client.get(private_url)
    project_data = json.loads(response.content.decode('utf-8'))
    assert project_data['is_private'] == True
    assert response.status_code == 200

    client.logout()


# def test_project_update(client):
#     assert False
#
#
# def test_project_delete(client):
#     assert False
#
#
def test_project_list(client, data):
    url = reverse('projects-list')

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 1
    assert response.status_code == 200

    client.login(data['registered_user'])

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 1
    assert response.status_code == 200

    client.login(data['project_member'])

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 2
    assert response.status_code == 200

    client.login(data['project_owner'])

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 2
    assert response.status_code == 200

    client.logout()

# def test_project_patch(client):
#     assert False
#
#
# def test_project_action_stats(client):
#     assert False
#
#
# def test_project_action_star(client):
#     assert False
#
#
# def test_project_action_unstar(client):
#     assert False
#
#
# def test_project_action_issues_stats(client):
#     assert False
#
#
# def test_project_action_issues_filters_data(client):
#     assert False
#
#
# def test_project_action_issues_tags(client):
#     assert False
#
#
# def test_membership_retrieve(client):
#     assert False
#
#
# def test_membership_update(client):
#     assert False
#
#
# def test_membership_delete(client):
#     assert False
#
#
# def test_membership_list(client):
#     assert False
#
#
# def test_membership_patch(client):
#     assert False
#
#
# def test_invitation_retrieve(client):
#     assert False
#
#
# def test_invitation_update(client):
#     assert False
#
#
# def test_invitation_delete(client):
#     assert False
#
#
# def test_invitation_list(client):
#     assert False
#
#
# def test_invitation_patch(client):
#     assert False
#
#
# def test_roles_retrieve(client):
#     assert False
#
#
# def test_roles_update(client):
#     assert False
#
#
# def test_roles_delete(client):
#     assert False
#
#
# def test_roles_list(client):
#     assert False
#
#
# def test_roles_patch(client):
#     assert False
#
#
# def test_points_retrieve(client):
#     assert False
#
#
# def test_points_update(client):
#     assert False
#
#
# def test_points_delete(client):
#     assert False
#
#
# def test_points_list(client):
#     assert False
#
#
# def test_points_patch(client):
#     assert False
#
#
# def test_points_action_bulk_update_order(client):
#     assert False
#
#
# def test_user_story_status_retrieve(client):
#     assert False
#
#
# def test_user_story_status_update(client):
#     assert False
#
#
# def test_user_story_status_delete(client):
#     assert False
#
#
# def test_user_story_status_list(client):
#     assert False
#
#
# def test_user_story_status_patch(client):
#     assert False
#
#
# def test_user_story_status_action_bulk_update_order(client):
#     assert False
#
#
# def test_task_status_retrieve(client):
#     assert False
#
#
# def test_task_status_update(client):
#     assert False
#
#
# def test_task_status_delete(client):
#     assert False
#
#
# def test_task_status_list(client):
#     assert False
#
#
# def test_task_status_patch(client):
#     assert False
#
#
# def test_task_status_action_bulk_update_order(client):
#     assert False
#
#
# def test_severity_retrieve(client):
#     assert False
#
#
# def test_severity_update(client):
#     assert False
#
#
# def test_severity_delete(client):
#     assert False
#
#
# def test_severity_list(client):
#     assert False
#
#
# def test_severity_patch(client):
#     assert False
#
#
# def test_severity_action_bulk_update_order(client):
#     assert False
#
#
# def test_priority_retrieve(client):
#     assert False
#
#
# def test_priority_update(client):
#     assert False
#
#
# def test_priority_delete(client):
#     assert False
#
#
# def test_priority_list(client):
#     assert False
#
#
# def test_priority_patch(client):
#     assert False
#
#
# def test_priority_action_bulk_update_order(client):
#     assert False
#
#
# def test_issue_type_retrieve(client):
#     assert False
#
#
# def test_issue_type_update(client):
#     assert False
#
#
# def test_issue_type_delete(client):
#     assert False
#
#
# def test_issue_type_list(client):
#     assert False
#
#
# def test_issue_type_patch(client):
#     assert False
#
#
# def test_issue_type_action_bulk_update_order(client):
#     assert False
#
#
# def test_issue_status_retrieve(client):
#     assert False
#
#
# def test_issue_status_update(client):
#     assert False
#
#
# def test_issue_status_delete(client):
#     assert False
#
#
# def test_issue_status_list(client):
#     assert False
#
#
# def test_issue_status_patch(client):
#     assert False
#
#
# def test_issue_status_action_bulk_update_order(client):
#     assert False
#
#
# def test_project_template_retrieve(client):
#     assert False
#
#
# def test_project_template_update(client):
#     assert False
#
#
# def test_project_template_delete(client):
#     assert False
#
#
# def test_project_template_list(client):
#     assert False
#
#
# def test_project_template_patch(client):
#     assert False
#
#
# def test_project_template_action_create_from_project(client):
#     assert False
#
#
# def test_fans_retrieve(client):
#     assert False
#
#
# def test_fans_update(client):
#     assert False
#
#
# def test_fans_delete(client):
#     assert False
#
#
# def test_fans_list(client):
#     assert False
#
#
# def test_fans_patch(client):
#     assert False
#
#
# def test_starred_retrieve(client):
#     assert False
#
#
# def test_starred_update(client):
#     assert False
#
#
# def test_starred_delete(client):
#     assert False
#
#
# def test_starred_list(client):
#     assert False
#
#
# def test_starred_patch(client):
#     assert False
#
#
