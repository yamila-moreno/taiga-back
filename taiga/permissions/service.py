from taiga.projects.models import Membership, Project


def _get_user_project_role(user, project):
    if user.is_anonymous():
        return None

    try:
        membership = Membership.objects.get(user=user, project=project)
        return membership.role
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

    role = _get_user_project_role(user, project)
    if role:
        return role_has_perm(role, perm)
    elif project.is_private:
        return False
    elif user.is_authenticated():
        return perm in project.anon_permissions + project.public_permissions
    else:
        return perm in project.anon_permissions


def role_has_perm(role, perm):
    return perm in role.permissions
