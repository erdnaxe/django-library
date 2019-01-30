from django.contrib.auth.models import Group
from rest_framework import serializers

from media.models import Author, Media, GameType, Game
from users.models import User, Key, Membership


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


class GameTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameType
        fields = ('name',)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('url', 'name', 'type', 'owner', 'length', 'min_players',
                  'max_players', 'box_length', 'box_width', 'box_depth',
                  'last_time_week_game', 'comment')


class KeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Key
        fields = ('name', 'owner', 'comment')


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Membership
        fields = ('start_at', 'end_at', 'members')
