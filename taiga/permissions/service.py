from taiga.projects.models import Membership, Project
from .permissions import OWNERS_PERMISSIONS


def _get_user_project_membership(user, project):
    if user.is_anonymous():
        return None

    try:
        return Membership.objects.get(user=user, project=project)
    except Membership.DoesNotExist:
        return None


def user_has_perm(user, perm, obj=None):
    project = None

    if isinstance(obj, Project):
        project = obj
    elif obj and obj.project:
        project = obj.project

    if not project:
        return False

    return perm in get_user_project_permissions(user, project)


def role_has_perm(role, perm):
    return perm in role.permissions


def get_user_project_permissions(user, project):
    membership = _get_user_project_membership(user, project)
    if membership:
        if membership.is_owner:
            owner_permissions = map(lambda perm: perm[0], OWNERS_PERMISSIONS)
            return project.anon_permissions + project.public_permissions + membership.role.permissions + owner_permissions
        else:
            return project.anon_permissions + project.public_permissions + membership.role.permissions
    elif project.is_private:
        return []
    elif user.is_authenticated():
        return project.anon_permissions + project.public_permissions
    else:
        return project.anon_permissions
