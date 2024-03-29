from rest_framework import serializers
from api.models import User, Contact, Feed, SocialProfile, ProfileRight, Notification,\
    Interests, SocialPlatform


class SocialPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialPlatform


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interests


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


class SocialProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialProfile

    def create(self, validated_data):

        user = self.context["current_user"]
        visibility = validated_data.pop("visibility", -1)

        profile = SocialProfile.objects.create(user=user, **validated_data)


        social_platform_id = validated_data.get("social_platform_id")
        platform_name = SocialPlatform.objects.get(pk=social_platform_id).platform_name

        if isinstance(visibility, int):
                is_public = True if visibility else False

        ProfileRight.objects.create(from_user=user, unit_type=platform_name,
                                         unit_id=social_platform_id, is_public= is_public,
                                    visible_for=visibility)

        return profile

    def update(self, instance, validated_data):

        instance.platform_id = validated_data.get("platform_id")
        instance.platform_token = validated_data.get("platform_token", None)
        instance.platform_secret = validated_data.get("platform_secret", None)
        instance.platform_permissions = validated_data.get("platform_permissions", None)
        instance.platform_email = validated_data.get("platform_email", None)

        instance.save()

        right = ProfileRight.objects.filter(from_user=instance.user, unit_type=instance.social_platform.platform_name)[0]
        visibility = validated_data.get("visibility", -1)
        is_public = False
        if isinstance(visibility, int):
                is_public = True if visibility else False
        right.is_public = is_public
        right.visible_for = visibility
        right.save()

        return instance




class SocialProfileSerializer(serializers.ModelSerializer):
    social_platform = serializers.SerializerMethodField(source = 'get_social_platform')

    class Meta:
        model = SocialProfile
        fields = ('social_platform', 'platform_id')

    def get_social_platform(self, obj):
        return obj.social_platform.platform_name


class ProfileRightSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileRight
        exclude = ('from_user', 'id')


class ProfileViewSerializer(serializers.ModelSerializer):
    profile_rights = ProfileRightSerializer(many=True)
    social_profile = SocialProfileSerializer(many=True)
    user_interests = serializers.SerializerMethodField(source='get_user_interests')

    class Meta:
        model = User
        include = ('social_profile', 'profile_rights', 'user_interests' )

    def get_user_interests(self, obj):
        user_interests = []
        for row in obj.user_interests.all():
            user_interests.append({
                "interest_id": row.interest.id,
                "interest_name": row.interest.interest
            })
        return user_interests


class ContactViewSerializer(serializers.ModelSerializer):
    contact_contag_user = ProfileViewSerializer()

    class Meta:
        model = Contact
        exclude = ('user',)
        depth = 1

    @staticmethod
    def set_visibility(contacts, user_id):
        i = 0

        for contact in contacts:

            if contact["is_on_contag"]:
                j = 0
                for visibility in contact["contact_contag_user"]["profile_rights"]:

                    if not visibility['is_public']:
                        if not visibility['visible_for'] or not user_id in [int(x) for x in visibility['visible_for'].split(",")]:
                            if visibility['unit_type'] in contacts[i]['contact_contag_user']:
                                contacts[i]['contact_contag_user'][visibility['unit_type']] = None
                            else:
                                social_index = next(index for (index, d) in enumerate(contacts[i]['contact_contag_user']['social_profile']) if d["social_platform"] == visibility['unit_type'])
                                if social_index > -1:
                                    del contacts[i]['contact_contag_user']['social_profile'][social_index]
                    j += 1


                contacts[i]['contact_contag_user'].pop("profile_rights", None)
            i += 1

        return contacts


class FeedSerializer(serializers.ModelSerializer):
    from_user = ProfileViewSerializer()

    class Meta:
        model = Feed
        depth = 1


class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id', 'registered_with', 'is_mobile_verified')

    def update(self, instance, validated_data):

        for field in validated_data:

            visibility = field.pop("visibility",-1)
            column_name = field.keys()[0]
            column_value = field[column_name]
            setattr(instance, column_name, column_value)

            is_public = False
            if isinstance(visibility, int):
                is_public = True if visibility else False

            right = ProfileRight.objects.filter(from_user=instance, unit_type=column_name)

            if not len(right):
                ProfileRight.objects.create(from_user=instance, unit_type=column_name,
                                 unit_id=instance.id, is_public= is_public,
                                visible_for=visibility)
            else:
                right = right[0]
                right.is_public = is_public
                right.visible_for = visibility
                right.save()

        instance.save()

        return instance


class BlockedMutedSerializer(serializers.ModelSerializer):
    contact_name = serializers.SerializerMethodField(source='get_contact_name')

    class Meta:
        model = Contact
        fields = ('contact_name', 'contact_number', 'contact_contag_user')


    def get_contact_name(self, obj):
        return obj.contact_contag_user.name if obj.contact_contag_user else obj.contact_name


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification






