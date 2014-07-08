import pytest

from taiga.permissions import service
from django.contrib.auth.models import AnonymousUser

from .. import factories

pytestmark = pytest.mark.django_db


def test_get_user_project_role():
    user1 = factories.UserFactory()
    user2 = factories.UserFactory()
    project = factories.ProjectFactory()
    role = factories.RoleFactory()
    membership = factories.MembershipFactory(user=user1, project=project, role=role)

    assert service._get_user_project_membership(user1, project) == membership
    assert service._get_user_project_membership(user2, project) is None


def test_anon_get_user_project_permissions():
    project = factories.ProjectFactory()
    project.anon_permissions = ["test1"]
    project.public_permissions = ["test2"]
    assert service.get_user_project_permissions(AnonymousUser(), project) == set(["test1"])


def test_user_get_user_project_permissions_on_public_project():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.anon_permissions = ["test1"]
    project.public_permissions = ["test2"]
    assert service.get_user_project_permissions(user1, project) == set(["test1", "test2"])


def test_user_get_user_project_permissions_on_private_project():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.anon_permissions = ["test1"]
    project.public_permissions = ["test2"]
    project.is_private = True
    assert service.get_user_project_permissions(user1, project) == set([])


def test_owner_get_user_project_permissions():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.anon_permissions = ["test1"]
    project.public_permissions = ["test2"]
    project.owner = user1
    role = factories.RoleFactory(permissions=["test3"])
    factories.MembershipFactory(user=user1, project=project, role=role)

    expected_perms = set(["test1", "test2", "test3", "modify_project",
                          "add_member", "remove_member", "delete_project",
                          "admin_project_values", "admin_roles"])
    assert service.get_user_project_permissions(user1, project) == expected_perms


def test_owner_member_get_user_project_permissions():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.anon_permissions = ["test1"]
    project.public_permissions = ["test2"]
    role = factories.RoleFactory(permissions=["test3"])
    factories.MembershipFactory(user=user1, project=project, role=role, is_owner=True)

    expected_perms = set(["test1", "test2", "test3", "modify_project",
                          "add_member", "remove_member", "delete_project",
                          "admin_project_values", "admin_roles"])
    assert service.get_user_project_permissions(user1, project) == expected_perms


def test_member_get_user_project_permissions():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.anon_permissions = ["test1"]
    project.public_permissions = ["test2"]
    role = factories.RoleFactory(permissions=["test3"])
    factories.MembershipFactory(user=user1, project=project, role=role)

    assert service.get_user_project_permissions(user1, project) == set(["test1", "test2", "test3"])


def test_anon_user_has_perm():
    project = factories.ProjectFactory()
    project.anon_permissions = ["test"]
    assert service.user_has_perm(AnonymousUser(), "test", project) == True
    assert service.user_has_perm(AnonymousUser(), "fail", project) == False


def test_authenticated_user_has_perm_on_project():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.public_permissions = ["test"]
    assert service.user_has_perm(user1, "test", project) == True
    assert service.user_has_perm(user1, "fail", project) == False


def test_authenticated_user_has_perm_on_project_related_object():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.public_permissions = ["test"]
    us = factories.UserStoryFactory(project=project)

    assert service.user_has_perm(user1, "test", us) == True
    assert service.user_has_perm(user1, "fail", us) == False


def test_authenticated_user_has_perm_on_invalid_object():
    user1 = factories.UserFactory()
    assert service.user_has_perm(user1, "test", user1) == False
