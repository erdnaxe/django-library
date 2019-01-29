from django.contrib.auth.models import Group
from rest_framework import viewsets

from media.models import Author, Media, Game
from users.models import User, Clef, Adhesion
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = serializers.GameSerializer


class KeyViewSet(viewsets.ModelViewSet):
    queryset = Clef.objects.all()
    serializer_class = serializers.KeySerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Adhesion.objects.all()
    serializer_class = serializers.MembershipSerializer
