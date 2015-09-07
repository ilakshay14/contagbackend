from rest_framework import serializers
from models import User, Contact, UserInterest, Feed


class ContactSyncSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact

    def create(self, validated_data):

        user = self.context['current_user']

        contact_name = validated_data.pop("contact_name", '')
        contact_number = validated_data.pop("contact_number", None)

        if not contact_number:
            return

        existing_contact = Contact.objects.filter(user=user, contact_number=contact_number)

        if len(existing_contact):
            existing_contact = existing_contact[0]
            existing_contact.contact_name = contact_name
            existing_contact.contact_number = contact_number
            existing_contact.save()
            result = existing_contact
        else:
            new_contact = Contact(user=user, contact_name=contact_name, contact_number=contact_number)
            new_contact.save()
            result = new_contact

        return result

    def update(self, instance, vaidated_data):
        pass


class UserInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInterest
        #fields = ('interest', )


class ProfileViewSerializer(serializers.ModelSerializer):
    user_interest = serializers.SerializerMethodField(source='get_user_interest')

    class Meta:
        model = User

    def get_user_interest(self, obj):
        return [interest.interest for interest in UserInterest.objects.filter(user=obj)]


class ContactViewSerializer(serializers.ModelSerializer):
    contact_contag_user = ProfileViewSerializer()

    class Meta:
        model = Contact
        exclude = ('user',)
        depth = 1


class FeedSerializer(serializers.ModelSerializer):
    from_user = ProfileViewSerializer()

    class Meta:
        model = Feed
        depth = 1


class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id', 'registered_with', 'is_mobile_verified')

