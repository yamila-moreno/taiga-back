from taiga.base import api

from . import models, serializers


class ProjectInvitationViewSet(api.ModelCrudViewSet):
    queryset = models.ProjectInvitation.objects.all()
    serializer_class = serializers.MembershipSerializer
    lookup_field = "token"
    # permission_classes = (AllowAny,)
