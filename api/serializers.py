from django.contrib.auth.models import Group
from rest_framework import serializers

from media.models import Author, Media, Game
from users.models import User, Clef, Adhesion


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ('url', 'title', 'author', 'side_title')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('url', 'name', 'owner', 'length', 'min_players',
                  'max_players', 'comment')


class KeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clef
        fields = ('name', 'owner', 'comment')


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Adhesion
        fields = ('start_at', 'end_at', 'members')
