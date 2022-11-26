from rest_framework import serializers
from .models import PlayCard, CardTrade
from accounts.serializer import UserSerializer
from department.models import Department


class PlayCardSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PlayCard
        fields = (
            "owner",
            "person",
        )


class PlayCardViewSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PlayCard
        fields = "owner", "person", "id"
        extra_kwargs = {"owner": {"read_only": True}, "person": {"read_only": True}}

    owner = UserSerializer()
    person = UserSerializer()


class UserDepartmentCollectionSerializer(serializers.ModelSerializer):

    top_deck = serializers.SerializerMethodField("resolver_top_deck")

    def resolver_top_deck(self, department):
        playcard_set = PlayCard.objects.filter(
            person__department_members=department, owner=self.context.get("user")
        ).order_by("pk")
        if playcard_set:
            return PlayCardViewSerializer(playcard_set.first()).data
        return {}

    class Meta(object):
        model = Department
        fields = "title", "top_deck", "id"
        extra_kwargs = {
            "title": {"read_only": True},
            "top_deck": {"read_only": True},
            "full_deck": {"read_only": True},
        }


class DepartmentCollectionSerializer(UserDepartmentCollectionSerializer):

    full_deck = serializers.SerializerMethodField("resolve_full_deck")

    def resolve_full_deck(self, department):
        playcard_set = set(
            PlayCard.objects.filter(
                person__department_members=department, owner=self.context.get("user")
            ).values_list("person_id", flat=True)
        )
        department_members = set(department.members.values_list("id", flat=True))
        if playcard_set == department_members:
            return True
        return False

    class Meta(object):
        model = Department
        fields = "title", "top_deck", "full_deck", "id"
        extra_kwargs = {
            "title": {"read_only": True},
            "top_deck": {"read_only": True},
            "full_deck": {"read_only": True},
        }


class CardTradeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CardTrade
        fields = "id", "user1", "user2", "user1_cards", "user2_cards"


class CardTradeViewSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CardTrade
        fields = "id", "user1", "user2", "user1_cards", "user2_cards"
        extra_kwargs = {
            "user1": {"read_only": True},
            "user2": {"read_only": True},
            "user1_cards": {"read_only": True},
            "user2_cards": {"read_only": True},
        }

    user1 = UserSerializer()
    user2 = UserSerializer()
    user1_cards = PlayCardViewSerializer(many=True)
    user2_cards = PlayCardViewSerializer(many=True)
