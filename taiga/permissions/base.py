

# class Permission(object):
#     global_perms = Or(ShouldAnonymous(),
#                       ShouldAuthenticated())

#     list_perms = HasPermission("view_milestones")

#     detail_perms = Or(And(SafeMethod(),
#                           CanViewMilestones()),
#                       And(CanEditMilestones()))


# class Permission(object):
#     global_perms = (should_anonymous() | should_authenticated())

#     list_perms = has_permission("view_milestones")

#     detail_perms = ((safe_method() & has_permission("view_milestones")) |
#                     has_permission("edit_milestones"))


# class Permission(object):
#     enought_perms =
#     global_perms = Or(ShouldAnonymous(),
#                       ShouldAuthenticated())
#     list_perms = None
#     update_perms = None
#     delete_perms = None

import abc

from taiga.base.utils.sequence as sq


class ResourcePermission(object):
    """
    Base class for define resource permissions.
    """

    enought_perms = None
    list_perms = None
    create_perms = None
    detail_perms = None
    update_perms = None
    delete_perms = None

    def __init__(self, request, view):
        self.request = request
        self.view = view

    def _evalute_permissions_set(self, permset, obj=None):
        if isinstance(permset, (list, tuple)):
            permset = reduce(lambda acc, v: acc & v, permset)

        if self.enought_perms:
            perms = (self.enought_perms | perms)

        return permset.check_permission(perm=self,
                                        request=self.request,
                                        view=self.view,
                                        obj=obj)

    def check_list_permissions(self):
        pass

    def check_detail_permissions(self):
        pass

    def check_update_permissions(self):
        pass

    def check_delete_permissions(self):
        pass


class PermissionComponent(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check_permission(self, perm, req, view, obj=None):
        pass

    def __invert__(self):
        return Not(self)

    def __and__(self, component):
        return And(self, component)

    def __or__(self, component):
        return Or(self, component)


class PermissionOperator(PermissionComponent):
    """
    Base class for all logical operators for compose
    components.
    """

    def __init__(self, *components):
        self.components = tuple(components)


class Not(PermissionOperator):
    """
    Negation operator as permission composable component.
    """

    # Overwrites the default constructor for fix
    # to one parameter instead of variable list of them.
    def __init__(self, component):
        super().__init__(component)

    def check_permission(self, *args, **kwargs):
        component = sq.first(self.components)
        return (not component.check_permission(*args, **kwargs))


class Or(PermissionOperator):
    """
    Or logical operator as permission component.
    """

    def check_permission(self, *args, **kwargs):
        valid = False

        for component in self.components:
            if component.check_permission(*args, **kwargs):
                valid = True
                break

        return valid


class And(PermissionOperator):
    """
    And logical operator as permission component.
    """

    def check_permission(self, *args, **kwargs):
        valid = True

        for component in self.components:
            if not component.check_permission(*args, **kwargs):
                valid = False
                break

        return valid

