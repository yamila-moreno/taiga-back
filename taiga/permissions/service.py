from taiga.projects.models import Membership, Project
from .permissions import OWNERS_PERMISSIONS, MEMBERS_PERMISSIONS


def _get_user_project_membership(user, project):
    if user.is_anonymous():
        return None

    try:
        return Membership.objects.get(user=user, project=project)
    except Membership.DoesNotExist:
        return None

def _get_object_project(obj):
    project = None

    if isinstance(obj, Project):
        project = obj
    elif obj and hasattr(obj, 'project'):
        project = obj.project
    return project


def is_project_owner(user, obj):
    project = _get_object_project(obj)
    if project:
        return project.owner == user
    return False


def user_has_perm(user, perm, obj=None):
    project = _get_object_project(obj)

    if not project:
        return False

    return perm in get_user_project_permissions(user, project)


def role_has_perm(role, perm):
    return perm in role.permissions


def get_user_project_permissions(user, project):
    membership = _get_user_project_membership(user, project)
    if project.owner == user:
        owner_permissions = list(map(lambda perm: perm[0], OWNERS_PERMISSIONS))
        if membership:
            members_permissions = membership.role.permissions
        else:
            members_permissions = list(map(lambda perm: perm[0], MEMBERS_PERMISSIONS))

        return set(project.anon_permissions + project.public_permissions + members_permissions + owner_permissions)
    elif membership:
        if membership.is_owner:
            owner_permissions = list(map(lambda perm: perm[0], OWNERS_PERMISSIONS))
            return set(project.anon_permissions + project.public_permissions + membership.role.permissions + owner_permissions)
        else:
            return set(project.anon_permissions + project.public_permissions + membership.role.permissions)
    elif project.is_private:
        return set()
    elif user.is_authenticated():
        return set(project.anon_permissions + project.public_permissions)
    else:
        return set(project.anon_permissions)
