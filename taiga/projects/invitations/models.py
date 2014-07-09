from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProjectInvitation(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               help_text=_("User sending the invitation"))
    recipient_email = models.EmailField(max_length=255, help_text=_("Invited person email"))
    token = models.CharField(max_length=255, db_index=True, help_text=_("Invitation token"))
    project = models.ForeignKey("projects.Project",
                                help_text=_("Project to which the user is being invited"))
    role = models.ForeignKey("users.Role",
                             help_text=_("Project role to perform by the invited user"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("recipient_email", "project")
        ordering = ["-created_at"]
