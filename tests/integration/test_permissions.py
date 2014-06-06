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

    assert service._get_user_project_role(user1, project) == role
    assert service._get_user_project_role(user2, project) is None

def test_anon_user_has_perm():
    project = factories.ProjectFactory()
    project.anon_permissions = ["test"]
    assert service.user_has_perm(AnonymousUser(), "test", project) == True
    assert service.user_has_perm(AnonymousUser(), "fail", project) == False

def test_authenticated_user_has_perm():
    user1 = factories.UserFactory()
    project = factories.ProjectFactory()
    project.public_permissions = ["test"]
    assert service.user_has_perm(user1, "test", project) == True
    assert service.user_has_perm(user1, "fail", project) == False
