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

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.core import validators
from django.utils import timezone

from djorm_pgarray.fields import TextArrayField

from taiga.base.utils.slug import slugify_uniquely
from taiga.permissions.permissions import MEMBERS_PERMISSIONS

import random
import re


def generate_random_hex_color():
    return "#{:06x}".format(random.randint(0,0xFFFFFF))


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django's Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '/./-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    email = models.EmailField(_('email address'), blank=True)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    full_name = models.CharField(_('full name'), max_length=256, blank=True)
    color = models.CharField(max_length=9, null=False, blank=True, default=generate_random_hex_color,
                             verbose_name=_("color"))
    bio = models.TextField(null=False, blank=True, default="", verbose_name=_("biography"))
    photo = models.FileField(upload_to="users/photo", max_length=500, null=True, blank=True,
                             verbose_name=_("photo"))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    default_language = models.CharField(max_length=20, null=False, blank=True, default="",
                                        verbose_name=_("default language"))
    default_timezone = models.CharField(max_length=20, null=False, blank=True, default="",
                                        verbose_name=_("default timezone"))
    colorize_tags = models.BooleanField(null=False, blank=True, default=False,
                                        verbose_name=_("colorize tags"))
    token = models.CharField(max_length=200, null=True, blank=True, default=None,
                             verbose_name=_("token"))
    github_id = models.IntegerField(null=True, blank=True, verbose_name=_("github ID"))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]
        permissions = (
            ("view_user", "Can view user"),
        )

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username

    def get_full_name(self):
        return self.full_name or self.username or self.email


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False,
                            verbose_name=_("name"))
    slug = models.SlugField(max_length=250, null=False, blank=True,
                            verbose_name=_("slug"))
    permissions = TextArrayField(blank=True, null=True,
                                 default=[],
                                 verbose_name=_("permissions"),
                                 choices=MEMBERS_PERMISSIONS)
    order = models.IntegerField(default=10, null=False, blank=False,
                                verbose_name=_("order"))
    project = models.ForeignKey("projects.Project", null=False, blank=False,
                                related_name="roles", verbose_name=_("project"))
    computable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.name, self.__class__)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"
        ordering = ["order", "slug"]
        unique_together = (("slug", "project"),)
        permissions = (
            ("view_role", "Can view role"),
        )

    def __str__(self):
        return self.name


# On Role object is changed, update all membership
# related to current role.
@receiver(models.signals.post_save, sender=Role,
          dispatch_uid="role_post_save")
def role_post_save(sender, instance, created, **kwargs):
    # ignore if object is just created
    if created:
        return

    unique_projects = set(map(lambda x: x.project, instance.memberships.all()))
    for project in unique_projects:
        project.update_role_points()
