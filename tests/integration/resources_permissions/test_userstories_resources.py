import pytest
from django.core.urlresolvers import reverse

from rest_framework.renderers import JSONRenderer

from taiga.projects.userstories.serializers import UserStorySerializer
from taiga.permissions.permissions import MEMBERS_PERMISSIONS, ANON_PERMISSIONS, USER_PERMISSIONS

from tests import factories as f
from tests.utils import helper_test_http_method, disconnect_signals, reconnect_signals

import json

pytestmark = pytest.mark.django_db


def setup_module(module):
    disconnect_signals()


def teardown_module(module):
    reconnect_signals()


@pytest.fixture
def data():
    m = type("Models", (object,), {})

    m.registered_user = f.UserFactory.create()
    m.project_member_with_perms = f.UserFactory.create()
    m.project_member_without_perms = f.UserFactory.create()
    m.project_owner = f.UserFactory.create()
    m.other_user = f.UserFactory.create()

    m.public_project = f.ProjectFactory(is_private=False,
                                        anon_permissions=list(map(lambda x: x[0], ANON_PERMISSIONS)),
                                        public_permissions=list(map(lambda x: x[0], USER_PERMISSIONS)),
                                        owner=m.project_owner)
    m.private_project1 = f.ProjectFactory(is_private=True,
                                          anon_permissions=list(map(lambda x: x[0], ANON_PERMISSIONS)),
                                          public_permissions=list(map(lambda x: x[0], USER_PERMISSIONS)),
                                          owner=m.project_owner)
    m.private_project2 = f.ProjectFactory(is_private=True,
                                          anon_permissions=[],
                                          public_permissions=[],
                                          owner=m.project_owner)

    m.public_membership = f.MembershipFactory(project=m.public_project,
                                          user=m.project_member_with_perms,
                                          role__project=m.public_project,
                                          role__permissions=list(map(lambda x: x[0], MEMBERS_PERMISSIONS)))
    m.private_membership1 = f.MembershipFactory(project=m.private_project1,
                                                user=m.project_member_with_perms,
                                                role__project=m.private_project1,
                                                role__permissions=list(map(lambda x: x[0], MEMBERS_PERMISSIONS)))
    f.MembershipFactory(project=m.private_project1,
                        user=m.project_member_without_perms,
                        role__project=m.private_project1,
                        role__permissions=[])
    m.private_membership2 = f.MembershipFactory(project=m.private_project2,
                                                user=m.project_member_with_perms,
                                                role__project=m.private_project2,
                                                role__permissions=list(map(lambda x: x[0], MEMBERS_PERMISSIONS)))
    f.MembershipFactory(project=m.private_project2,
                        user=m.project_member_without_perms,
                        role__project=m.private_project2,
                        role__permissions=[])

    m.public_points = f.PointsFactory(project=m.public_project)
    m.private_points1 = f.PointsFactory(project=m.private_project1)
    m.private_points2 = f.PointsFactory(project=m.private_project2)

    m.public_role_points = f.RolePointsFactory(role=m.public_project.roles.all()[0],
                                               points=m.public_points,
                                               user_story__project=m.public_project)
    m.private_role_points1 = f.RolePointsFactory(role=m.private_project1.roles.all()[0],
                                                 points=m.private_points1,
                                                 user_story__project=m.private_project1)
    m.private_role_points2 = f.RolePointsFactory(role=m.private_project2.roles.all()[0],
                                                 points=m.private_points2,
                                                 user_story__project=m.private_project2)

    m.public_user_story = m.public_role_points.user_story
    m.private_user_story1 = m.private_role_points1.user_story
    m.private_user_story2 = m.private_role_points2.user_story

    return m


def test_user_story_retrieve(client, data):
    public_url = reverse('userstories-detail', kwargs={"pk": data.public_user_story.pk})
    private_url1 = reverse('userstories-detail', kwargs={"pk": data.private_user_story1.pk})
    private_url2 = reverse('userstories-detail', kwargs={"pk": data.private_user_story2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_without_perms,
        data.project_member_with_perms,
        data.project_owner
    ]

    results = helper_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200, 200]
    results = helper_test_http_method(client, 'get', private_url1, None, users)
    assert results == [200, 200, 200, 200, 200]
    results = helper_test_http_method(client, 'get', private_url2, None, users)
    assert results == [401, 403, 403, 200, 200]


def test_user_story_update(client, data):
    public_url = reverse('userstories-detail', kwargs={"pk": data.public_user_story.pk})
    private_url1 = reverse('userstories-detail', kwargs={"pk": data.private_user_story1.pk})
    private_url2 = reverse('userstories-detail', kwargs={"pk": data.private_user_story2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_without_perms,
        data.project_member_with_perms,
        data.project_owner
    ]

    user_story_data = UserStorySerializer(data.public_user_story).data
    user_story_data["subject"] = "test"
    user_story_data = JSONRenderer().render(user_story_data)
    results = helper_test_http_method(client, 'put', public_url, user_story_data, users)
    assert results == [401, 403, 403, 200, 200]

    user_story_data = UserStorySerializer(data.private_user_story1).data
    user_story_data["subject"] = "test"
    user_story_data = JSONRenderer().render(user_story_data)
    results = helper_test_http_method(client, 'put', private_url1, user_story_data, users)
    assert results == [401, 403, 403, 200, 200]

    user_story_data = UserStorySerializer(data.private_user_story2).data
    user_story_data["subject"] = "test"
    user_story_data = JSONRenderer().render(user_story_data)
    results = helper_test_http_method(client, 'put', private_url2, user_story_data, users)
    assert results == [401, 403, 403, 200, 200]


def test_user_story_delete(client, data):
    public_url = reverse('userstories-detail', kwargs={"pk": data.public_user_story.pk})
    private_url1 = reverse('userstories-detail', kwargs={"pk": data.private_user_story1.pk})
    private_url2 = reverse('userstories-detail', kwargs={"pk": data.private_user_story2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_without_perms,
        data.project_member_with_perms,
    ]
    results = helper_test_http_method(client, 'delete', public_url, None, users)
    assert results == [401, 403, 403, 204]
    results = helper_test_http_method(client, 'delete', private_url1, None, users)
    assert results == [401, 403, 403, 204]
    results = helper_test_http_method(client, 'delete', private_url2, None, users)
    assert results == [401, 403, 403, 204]


def test_user_story_list(client, data):
    url = reverse('userstories-list')

    response = client.get(url)
    userstories_data = json.loads(response.content.decode('utf-8'))
    assert len(userstories_data) == 2
    assert response.status_code == 200

    client.login(data.registered_user)

    response = client.get(url)
    userstories_data = json.loads(response.content.decode('utf-8'))
    assert len(userstories_data) == 2
    assert response.status_code == 200

    client.login(data.project_member_with_perms)

    response = client.get(url)
    userstories_data = json.loads(response.content.decode('utf-8'))
    assert len(userstories_data) == 3
    assert response.status_code == 200

    client.login(data.project_owner)

    response = client.get(url)
    userstories_data = json.loads(response.content.decode('utf-8'))
    assert len(userstories_data) == 3
    assert response.status_code == 200


def test_user_story_patch(client, data):
    public_url = reverse('userstories-detail', kwargs={"pk": data.public_user_story.pk})
    private_url1 = reverse('userstories-detail', kwargs={"pk": data.private_user_story1.pk})
    private_url2 = reverse('userstories-detail', kwargs={"pk": data.private_user_story2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_without_perms,
        data.project_member_with_perms,
        data.project_owner
    ]

    patch_data = json.dumps({"subject": "test"})

    results = helper_test_http_method(client, 'patch', public_url, patch_data, users)
    assert results == [401, 403, 403, 200, 200]
    results = helper_test_http_method(client, 'patch', private_url1, patch_data, users)
    assert results == [401, 403, 403, 200, 200]
    results = helper_test_http_method(client, 'patch', private_url2, patch_data, users)
    assert results == [401, 403, 403, 200, 200]
