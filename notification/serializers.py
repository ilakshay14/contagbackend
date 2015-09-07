from rest_framework import serializers

from .models import User, Contact, UserInterest, UserPlatform, Feed, Notification


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact

    def create(self, validated_data):

        user = validated_data.pop("user", 0)

        contacts = validated_data.pop("contacts", [])

        result = []
        for contact in contacts:
            contact_contag_user = Contact.is_contag_user(contact_number=contact["contact_number"])
            is_on_contag  = True if contact_contag_user else False
            contag = Contact.objects.create(user=user, contact_name=contact["contact_name"],
                                   contact_number=contact["contact_number"], is_on_contag=is_on_contag,
                                   contact_contag_user=contact_contag_user)
            result.append(contag)

        return result


class InterestsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserInterest
        depth = 1


class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPlatform


class ProfileSerializer(serializers.ModelSerializer):
    user_interests = InterestsSerializer()
    user_platforms = PlatformSerializer()

    class Meta:
        model = User
        depth = 1
        fields = ('user_interests', 'user_platforms')


class FeedSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()

    class Meta:
        model = Feed
        depth = 1


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification


