import datetime
import traceback

from rest_framework.views import APIView
from django.utils import timezone

from models import OTPToken, Contact, Feed, User, ProfileRequest
from contag.APIPermissions import AuthToken
from contag.response import JSONResponse, VALIDATION_ERROR_MESSAGE, OBJECT_DOES_NOT_EXIST, REQUEST_ALREADY_EXISTS, \
    PROFILE_REQUEST_CREATED, SUCCESS_STATUS
from serializers import ContactSyncSerializer, ContactViewSerializer, FeedSerializer, ProfileEditSerializer, \
    ProfileViewSerializer, SocialProfileEditSerializer


class LoginView(APIView):

    def post(self, request):
        number = request.data['number']
        otp = OTPToken.create(number=number)
        otp.save()
        otp.send()
        return JSONResponse(SUCCESS_STATUS, status=200)


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
            status = 400

        return JSONResponse(result, status=status)


class UserView(APIView):

    permission_classes = (AuthToken,)

    def put(self, request):

        profile = ProfileEditSerializer(instance=request.user, partial=True, data=request.data["profile"])

        if profile.is_valid():
            user_profile = profile.save()
            user_profile.set_visibility(request.data)
            return JSONResponse(profile.data, status=200)
        else:
            return JSONResponse(profile.errors, status=403)

    def get(self, request):

        try:
            user = User.objects.get(pk=request.query_params["user_id"]) if "user_id" in request.query_params else request.user
            profile = ProfileViewSerializer(instance=user)
            # TODO visibility object
            return JSONResponse(profile.data, status=200)
        except Exception as e:
            return JSONResponse(OBJECT_DOES_NOT_EXIST, status=400)

    def post(self, request):

        users = User.objects.filter(contag=request.data['contag_id'])
        # Check if an existing user exists with the given contag id
        if len(users):
            return JSONResponse({"success": False, "auth_token": None}, status=200)
        else:
            user = User(mobile_number=request.data['number'], contag=request.data['contag_id'])
            user.save()
            token = user.get_access_token(request.META)
            return JSONResponse({"success": True, "auth_token": token.access_token}, status=200)


class SocialProfileView(APIView):

    permission_classes = (AuthToken, )

    def put(self, request):

        social_profile = SocialProfileEditSerializer(partial=True, data=request.data["social_profile"],
                                                     context={'current_user': request.user})

        if social_profile.is_valid():
            social_profile.save()
            social_profile.set_visibility(request.data)
            return JSONResponse(social_profile.save(), status=200)
        else:
            return JSONResponse(social_profile.error_messages, status=403)


class ProfileRequestView(APIView):
    def post(self, request):

        from_user = request.user
        for_user = request.data["for_user"]
        request_type = request.data["request_type"]

        profile_request = ProfileRequest.objects.filter(for_user=for_user, from_user=from_user,
                                                        request_type=request_type)

        if len(profile_request):
            return JSONResponse(REQUEST_ALREADY_EXISTS, status=200)
        else:
            profile_request = ProfileRequest(for_user=for_user, from_user=from_user, request_type=request_type)
            profile_request.save()
            return JSONResponse(PROFILE_REQUEST_CREATED, status=200)

    def put(self, request):

        profile_request = ProfileRequest.objects.get(pk=request.data["profile_request_id"])

        try:
            profile_request.is_fulfilled = request.data["is_fulfilled"]
        except Exception as e:
            profile_request.is_denied = request.data["is_denied"]

        profile_request.save()

        return JSONResponse(SUCCESS_STATUS, status=200)


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

            return JSONResponse(response_data, status=200)
        except Exception as e:
            print traceback.format_exc(e)
            return JSONResponse(VALIDATION_ERROR_MESSAGE, status=400)

    def get(self, request):

        contacts = Contact.objects.filter(user=request.user)

        response_data = ContactViewSerializer(instance=contacts, many=True).data

        return JSONResponse(response_data, status=200)


class FeedView(APIView):
    permission_classes = (AuthToken,)

    def get(self, request):
        stories = Feed.objects.filter(from_user=request.user)

        feeds = FeedSerializer(instance=stories, many=True).data

        return JSONResponse(feeds, status=200)
