# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import abc

from taiga.base.utils import sequence as sq


######################################################################
# Base permissiones definition
######################################################################

class ResourcePermission(object):
    """
    Base class for define resource permissions.
    """

    enought_perms = None
    retrieve_perms = None
    create_perms = None
    detail_perms = None
    update_perms = None
    delete_perms = None

    def __init__(self, request, view):
        self.request = request
        self.view = view

    def check_permissions(self, action:str, obj:object=None):
        permset = getattr(self, "{}_perms".format(action))

        if isinstance(permset, (list, tuple)):
            permset = reduce(lambda acc, v: acc & v, permset)
        elif permset is None:
            # Use empty operator that always return true with
            # empty components.
            permset = And()
        elif isinstance(permset, PermissionComponent):
            # Do nothing
            pass
        elif inspect.isclass(permset) and issubclass(permset, PermissionComponent):
            permset = permset()
        else:
            raise RuntimeError("Invalid permission definition.")

        if self.enought_perms:
            perms = (self.enought_perms | perms)

        return permset.check_permissions(request=self.request,
                                         view=self.view,
                                         obj=obj)


class PermissionComponent(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check_permissions(self, request, view, obj=None):
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

    def check_permissions(self, *args, **kwargs):
        component = sq.first(self.components)
        return (not component.check_permissions(*args, **kwargs))


class Or(PermissionOperator):
    """
    Or logical operator as permission component.
    """

    def check_permissions(self, *args, **kwargs):
        valid = False

        for component in self.components:
            if component.check_permissions(*args, **kwargs):
                valid = True
                break

        return valid


class And(PermissionOperator):
    """
    And logical operator as permission component.
    """

    def check_permissions(self, *args, **kwargs):
        valid = True

        for component in self.components:
            if not component.check_permissions(*args, **kwargs):
                valid = False
                break

        return valid


######################################################################
# Generic components.
######################################################################

class AllowAny(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return True


class IsAuthenticated(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return request.user and request.user.is_authenticated()


######################################################################
# Generic permissions.
######################################################################

class AllowAnyPermission(ResourcePermission):
    enought_perms = AllowAny()
