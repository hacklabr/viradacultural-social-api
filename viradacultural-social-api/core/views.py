from rest_framework import viewsets
from .models import FbUser
from .serializer import UserSerializer
import facebook


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = FbUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        fb_user_id = request.query_params('uid')
        oauth_access_token = request.query_params('fbtoken')
        graph = facebook.GraphAPI(oauth_access_token)
        profile = graph.get_object("me")
        friends = graph.get_connections("me", "friends")

