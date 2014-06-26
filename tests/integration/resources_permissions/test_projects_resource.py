import pytest
from django.core.urlresolvers import reverse

from rest_framework.renderers import JSONRenderer

from taiga.projects.serializers import ProjectDetailSerializer
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
                                        public_permissions=['view_project'])
    m.private_project1 = f.ProjectFactory(is_private=True,
                                          anon_permissions=['view_project'],
                                          public_permissions=['view_project'],
                                          owner=m.project_owner)
    m.private_project2 = f.ProjectFactory(is_private=True,
                                          anon_permissions=[],
                                          public_permissions=[],
                                          owner=m.project_owner)

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


def test_project_retrieve(client, data):
    public_url = reverse('projects-detail', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-detail', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-detail', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]

    results = util_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private1_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private2_url, None, users)
    assert results == [401, 403, 200, 200]


def test_project_update(client, data):
    url = reverse('projects-detail', kwargs={"pk": data.private_project2.pk})

    project_data = ProjectDetailSerializer(data.private_project1).data
    project_data["is_private"] = False
    project_data = JSONRenderer().render(project_data)

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]

    results = util_test_http_method(client, 'put', url, project_data, users)
    assert results == [401, 403, 403, 200]


def test_project_delete(client, data):
    url = reverse('projects-detail', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'delete', url, None, users)
    assert results == [401, 403, 403, 204]


def test_project_list(client, data):
    url = reverse('projects-list')

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 2
    assert response.status_code == 200

    client.login(data.registered_user)

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 2
    assert response.status_code == 200

    client.login(data.project_member_with_perms)

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 3
    assert response.status_code == 200

    client.login(data.project_owner)

    response = client.get(url)
    projects_data = json.loads(response.content.decode('utf-8'))
    assert len(projects_data) == 3
    assert response.status_code == 200


def test_project_patch(client, data):
    url = reverse('projects-detail', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    data = json.dumps({"is_private": False})
    results = util_test_http_method(client, 'patch', url, data, users)
    assert results == [401, 403, 403, 200]


def test_project_action_stats(client, data):
    public_url = reverse('projects-stats', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-stats', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-stats', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private1_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private2_url, None, users)
    assert results == [404, 404, 200, 200]


def test_project_action_star(client, data):
    public_url = reverse('projects-star', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-star', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-star', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'post', public_url, None, users)
    assert results == [401, 200, 200, 200]
    results = util_test_http_method(client, 'post', private1_url, None, users)
    assert results == [401, 200, 200, 200]
    results = util_test_http_method(client, 'post', private2_url, None, users)
    assert results == [404, 404, 200, 200]


def test_project_action_unstar(client, data):
    public_url = reverse('projects-unstar', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-unstar', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-unstar', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'post', public_url, None, users)
    assert results == [401, 200, 200, 200]
    results = util_test_http_method(client, 'post', private1_url, None, users)
    assert results == [401, 200, 200, 200]
    results = util_test_http_method(client, 'post', private2_url, None, users)
    assert results == [404, 404, 200, 200]


def test_project_action_issues_stats(client, data):
    public_url = reverse('projects-issues-stats', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-issues-stats', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-issues-stats', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private1_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private2_url, None, users)
    assert results == [404, 404, 200, 200]


def test_project_action_issues_filters_data(client, data):
    public_url = reverse('projects-issue-filters-data', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-issue-filters-data', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-issue-filters-data', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private1_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private2_url, None, users)
    assert results == [404, 404, 200, 200]


def test_project_action_tags(client, data):
    public_url = reverse('projects-tags', kwargs={"pk": data.public_project.pk})
    private1_url = reverse('projects-tags', kwargs={"pk": data.private_project1.pk})
    private2_url = reverse('projects-tags', kwargs={"pk": data.private_project2.pk})

    users = [
        None,
        data.registered_user,
        data.project_member_with_perms,
        data.project_owner
    ]
    results = util_test_http_method(client, 'get', public_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private1_url, None, users)
    assert results == [200, 200, 200, 200]
    results = util_test_http_method(client, 'get', private2_url, None, users)
    assert results == [404, 404, 200, 200]


# def test_membership_retrieve(client, data):
#     assert False
#
#
# def test_membership_update(client, data):
#     assert False
#
#
# def test_membership_delete(client, data):
#     assert False
#
#
# def test_membership_list(client, data):
#     assert False
#
#
# def test_membership_patch(client, data):
#     assert False
#
#
# def test_invitation_retrieve(client, data):
#     assert False
#
#
# def test_invitation_update(client, data):
#     assert False
#
#
# def test_invitation_delete(client, data):
#     assert False
#
#
# def test_invitation_list(client, data):
#     assert False
#
#
# def test_invitation_patch(client, data):
#     assert False
#
#
# def test_project_template_retrieve(client, data):
#     assert False
#
#
# def test_project_template_update(client, data):
#     assert False
#
#
# def test_project_template_delete(client, data):
#     assert False
#
#
# def test_project_template_list(client, data):
#     assert False
#
#
# def test_project_template_patch(client, data):
#     assert False
#
#
# def test_project_template_action_create_from_project(client, data):
#     assert False
#
#
# def test_fans_retrieve(client, data):
#     assert False
#
#
# def test_fans_update(client, data):
#     assert False
#
#
# def test_fans_delete(client, data):
#     assert False
#
#
# def test_fans_list(client, data):
#     assert False
#
#
# def test_fans_patch(client, data):
#     assert False
#
#
# def test_starred_retrieve(client, data):
#     assert False
#
#
# def test_starred_update(client, data):
#     assert False
#
#
# def test_starred_delete(client, data):
#     assert False
#
#
# def test_starred_list(client, data):
#     assert False
#
#
# def test_starred_patch(client, data):
#     assert False
#
#
