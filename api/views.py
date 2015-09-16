import datetime
import traceback

from rest_framework.views import APIView
from django.utils import timezone

from django.db.models import Q
from models import OTPToken, User, ProfileRequest, Contact, SocialPlatform, \
    Interests, ShareContact, Feed, Notification, UserInterest, SocialProfile
from contag.APIPermissions import AuthToken
from contag.response import JSONResponse, VALIDATION_ERROR_MESSAGE, OBJECT_DOES_NOT_EXIST, REQUEST_ALREADY_EXISTS, \
    PROFILE_REQUEST_CREATED, SUCCESS_MESSAGE, ERROR_MESSAGE
from serializers import ContactSyncSerializer, ContactViewSerializer, FeedSerializer,\
    ProfileEditSerializer, ProfileViewSerializer, SocialProfileEditSerializer,\
    BlockedMutedSerializer, NotificationSerializer, SocialPlatformSerializer, InterestSerializer


class LoginView(APIView):

    def post(self, request):
        number = request.data['number']
        otp = OTPToken.create(number=number)
        otp.save()
        otp.send()
        return JSONResponse(SUCCESS_MESSAGE, status=200)


class OTPView(APIView):

    def post(self, request):
        number = request.data['number']
        otp = request.data['otp']
        status = 200
        if OTPToken.objects.filter(updated_on__gte=(timezone.now() - datetime.timedelta(hours=2)), number=number,
                                   otp=otp).exists():
            if User.objects.filter(mobile_number=number).exists():
                user = User.objects.filter(mobile_number=number)[0]
                token = user.get_access_token(request.META)
                result = {
                        "is_new_user": False,
                        "success":     True,
                        "auth_token":  token.access_token
                        }
            else:
                result = {
                        "is_new_user": True,
                        "success": True,
                        "auth_token": None
                         }
        else:
            result = {
                    "is_new_user": False,
                    "success": False,
                    "auth_token": None
                    }
            
        return JSONResponse(result, status=status)


class LogoutView(APIView):

    permission_classes = (AuthToken, )

    def delete(self, request):

        user = request.user

        user.logout(headers=request.META)

        return JSONResponse(SUCCESS_MESSAGE, status=200)


class UserView(APIView):

    permission_classes = (AuthToken,)

    def put(self, request):

        profile = ProfileEditSerializer()
        profile = profile.update(instance=request.user, validated_data=request.data)

        profile = ProfileViewSerializer(instance=profile)

        return JSONResponse(profile.data, status=200)

        #return JSONResponse(profile.errors, status=403)

    def get(self, request):

        try:
            user = User.objects.get(pk=request.query_params["user_id"]) if "user_id" in request.query_params else request.user
            profile = ProfileViewSerializer(instance=user)
            return JSONResponse(profile.data, status=200)
        except Exception as e:
            print traceback.format_exc(e)
            return JSONResponse(OBJECT_DOES_NOT_EXIST, status=200)

    def post(self, request):

        users = User.objects.filter(contag=request.data['contag_id'])
        # Check if an existing user exists with the given contag id
        if len(users):
            return JSONResponse({"success": False, "auth_token": None}, status=200)
        else:
            user = User(mobile_number=request.data['number'], contag=request.data['contag_id'])
            user.save()
            user.new_user()
            token = user.get_access_token(request.META)
            return JSONResponse({"success": True, "auth_token": token.access_token}, status=200)


class SocialProfileView(APIView):

    permission_classes = (AuthToken, )

    def get(self, request):

        platforms = SocialPlatform.objects.all()
        platforms = SocialPlatformSerializer(instance=platforms, many=True).data

        return JSONResponse(platforms, status=200)

    def post(self, request):

        user = request.user
        social_profile = SocialProfile.objects.filter(user=user, social_platform_id=request.data["social_platform_id"])

        if len(social_profile):
            profile = SocialProfileEditSerializer()
            profile.update(instance=social_profile[0], validated_data=request.data)
        else:
            social_profile = SocialProfileEditSerializer(context={'current_user': request.user})
            social_profile.create(validated_data=request.data)

        return JSONResponse(SUCCESS_MESSAGE, status=200)


class InterestView(APIView):

    permission_classes = (AuthToken, )

    def get(self, request):

        slug = request.query_params['slug']

        interests = Interests.objects.filter(interest__icontains=slug)

        interests = InterestSerializer(instance=interests, many=True).data

        return JSONResponse(interests, status=200)

    def post(self, request):

        try:
            user = request.user

            UserInterest.objects.filter(user=user).delete()

            for interest_id in request.data["interest_ids"].split(","):
                UserInterest.objects.create(user=user, interest_id=interest_id)

            return JSONResponse(SUCCESS_MESSAGE, status=200)
        except Exception as e:
            print traceback.format_exc(e)
            return JSONResponse(ERROR_MESSAGE, status=200)


class ProfileRequestView(APIView):

    permission_classes = (AuthToken, )

    def post(self, request):

        from_user = request.user
        for_user = request.data["for_user"]
        request_type = request.data["request_type"]

        profile_request = ProfileRequest.objects.filter(for_user_id=for_user, from_user=from_user,
                                                        request_type=request_type)

        if len(profile_request):
            return JSONResponse(REQUEST_ALREADY_EXISTS, status=200)
        else:
            profile_request = ProfileRequest(for_user_id=for_user, from_user=from_user, request_type=request_type)
            profile_request.save()
            return JSONResponse(PROFILE_REQUEST_CREATED, status=200)

    def put(self, request):

        profile_request = ProfileRequest.objects.get(pk=request.data["profile_request_id"])

        try:
            profile_request.is_fulfilled = request.data["is_fulfilled"]
        except Exception as e:
            profile_request.is_denied = request.data["is_denied"]

        profile_request.save()

        return JSONResponse(SUCCESS_MESSAGE, status=200)


class ContactView(APIView):
    permission_classes = (AuthToken,)

    def post(self, request):

        try:
            # Create/Update whatever contacts come from the app
            contacts = ContactSyncSerializer(many=True, context={'current_user': request.user})
            synced_contacts = contacts.create(validated_data=request.data)

            # Delete records which are not in synced ids
            # synced_ids = [contact.id for contact in synced_contacts]
            # Contact.objects.filter(user=request.user).exclude(id__in=synced_ids).delete()

            response_data = ContactViewSerializer(instance=synced_contacts, many=True).data

            response_data = ContactViewSerializer.set_visibility(response_data, user_id = request.user.id)

            print(response_data)
            return JSONResponse(response_data, status=200)
        except Exception as e:
            print traceback.format_exc(e)
            return JSONResponse(VALIDATION_ERROR_MESSAGE, status=200)

    def get(self, request):

        contacts = Contact.objects.filter(user=request.user, is_blocked=False)

        response_data = ContactViewSerializer(instance=contacts, many=True).data

        response_data = ContactViewSerializer.set_visibility(response_data, user_id = request.user.id)

        return JSONResponse(response_data, status=200)


class InviteView(APIView):

    permission_classes = (AuthToken, )

    def put(self, request):

        try:
            contact_id = request.data["contact_id"]
            # TODO send the invite through sms/whatsapp?
            Contact.objects.filter(id=contact_id).update(is_invited=True, invited_on=datetime.datetime.now())

            return JSONResponse(SUCCESS_MESSAGE, status=200)
        except Exception as e:
            return JSONResponse(OBJECT_DOES_NOT_EXIST, status=200)


class ShareContactView(APIView):

    permission_classes = (AuthToken, )

    def post(self, request):

        try:
            contact_id = request.data["contact_id"]
            message = request.data["message"]
            shared_with = request.data["shared_with"]
            share = ShareContact(from_user= request.user, shared_with_id = shared_with,
                                 contact_id=contact_id, message=message)
            share.save()
            return JSONResponse(SUCCESS_MESSAGE, status=200)
        except Exception as e:
            print traceback.format_exc(e)
            return JSONResponse(ERROR_MESSAGE, status=200)


class BlockMuteView(APIView):

    permission_classes = (AuthToken, )

    def put(self, request):

        try:
            is_blocked = request.data["is_blocked"]
            is_muted = request.data["is_muted"]
            contact_id = request.data["contact_id"]

            Contact.objects.filter(id=contact_id).update(is_blocked=is_blocked, is_muted=is_muted)
            return JSONResponse(SUCCESS_MESSAGE, status=200)

        except Exception as e:
            return JSONResponse(OBJECT_DOES_NOT_EXIST, status=200)

    def get(self, request):

        blocked_muted_contacts = Contact.objects.filter(Q(user=request.user) & (Q(is_blocked=True) | Q(is_muted=True)))

        return JSONResponse(BlockedMutedSerializer(instance=blocked_muted_contacts, many=True).data, status=200)


class FeedView(APIView):
    permission_classes = (AuthToken,)

    def get(self, request):
        stories = Feed.objects.filter(from_user=request.user)

        feeds = FeedSerializer(instance=stories, many=True).data

        return JSONResponse(feeds, status=200)


class NotificationView(APIView):

    permission_classes = (AuthToken, )

    def get(self, request):

        start_index = request.data["start_index"]
        end_index = request.data["end_index"]

        notifications = Notification.obejcts.filter(user=request.user)[start_index:end_index]

        return JSONResponse(NotificationSerializer(instance=notifications, many=True).data, status=200)












# Profile Right mess
# Feed/notification generation and contact update
# End points: Block/Mute, Feed, Notification, logout, Change contact number