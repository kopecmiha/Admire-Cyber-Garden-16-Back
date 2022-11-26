from rest_framework import serializers
from .models import PlayCard
from accounts.serializer import UserSerializer
from department.models import Department


class PlayCardSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PlayCard
        fields = "owner", "person"


class PlayCardViewSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PlayCard
        fields = "owner", "person"
        extra_kwargs = {'owner': {'read_only': True}, "person": {'read_only': True}}

    owner = UserSerializer()
    person = UserSerializer()


class DepartmentCollectionSerializer(serializers.ModelSerializer):

    top_deck = serializers.SerializerMethodField("resolver_top_deck")

    def resolver_top_deck(self, department):
        playcard_set = PlayCard.objects.filter(person__department_members=department).order_by("pk")
        if playcard_set:
            return PlayCardViewSerializer(playcard_set.first())
        return {}

    class Meta(object):
        model = Department
        fields = "title", "top_deck"
        extra_kwargs = {'title': {'read_only': True}, "top_deck": {'read_only': True}}

