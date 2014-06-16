import pytest
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from taiga.projects.api import ProjectViewSet
from taiga.projects.models import Project
from taiga.users.models import User

from tests import factories as f

pytestmark = pytest.mark.django_db

rf = APIRequestFactory()


def setup_module(module):
    Project.objects.all().delete()
    User.objects.all().delete()

    module.registered_user = f.UserFactory()
    module.project_member = f.UserFactory()
    module.project_owner = f.UserFactory()

    module.public_project = f.ProjectFactory(is_private=False)
    module.private_project = f.ProjectFactory(is_private=True, owner=project_owner)

    f.MembershipFactory(project=private_project, user=project_member)


def test_project_retrieve():
    request = rf.get(reverse('projects-detail', args=[1]))
    request.user = registered_user
    response = ProjectViewSet().retrieve(request, 1)
    assert len(response) == 1


# def test_project_update(client):
#     assert False
#
#
# def test_project_delete(client):
#     assert False
#
#
# def test_project_list(client):
#     assert False
#
#
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
