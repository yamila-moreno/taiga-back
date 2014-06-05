import pytest

from taiga.permissions import service

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
