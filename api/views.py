import datetime
import traceback
from random import randint



from rest_framework.views import APIView
from django.utils import timezone
from contag.APIPermissions import AuthToken

from contag.response import JSONResponse, UNKOWN_ERROR_MESSAGE, VALIDATION_ERROR_MESSAGE, OBJECT_DOES_NOT_EXIST
from models import OTPModel, Contact, Feed, User
from serializers import ContactSyncSerializer, ContactViewSerializer, FeedSerializer, ProfileEditSerializer, \
    ProfileViewSerializer


class LoginView(APIView):

    def post(self, request):
        number = request.data['number']
        otp = randint(100000, 999999)
        new_entry = OTPModel(number=number, otp=otp)
        new_entry.save()
        return JSONResponse({"success": "true"}, status=200)


class OTPView(APIView):

    def post(self, request):
        number = request.data['number']
        otp = request.data['otp']
        if OTPModel.objects.filter(updated_on__gte = (timezone.now() - datetime.timedelta(hours=2)),number=number, otp=otp).exists():
            return JSONResponse({"success": "true"}, status=200)
        else:
            return JSONResponse({"success": "false"}, status=200)


class UserView(APIView):

    permission_classes = (AuthToken, )

    def put(self, request):

        profile = ProfileEditSerializer(instance=request.user, partial=True, data=request.data)

        if profile.is_valid():
            profile.save()
            return JSONResponse(profile.data, status=200)

    def get(self, request):

        try:
            user = User.objects.get(pk= request.query_params["user_id"])
            profile = ProfileViewSerializer(instance=user)

            return JSONResponse(profile.data, status=200)
        except Exception as e:
            return JSONResponse(OBJECT_DOES_NOT_EXIST, status=400)


class ContactView(APIView):

    permission_classes = (AuthToken, )

    def post(self, request):

        try:
            # Create/Update whatever contacts come from the app
            contacts = ContactSyncSerializer(many=True, context={'current_user': request.user})
            synced_contacts = contacts.create(validated_data=request.data)

            # Delete records which are not in synced ids
            synced_ids = [contact.id for contact in synced_contacts]
            Contact.objects.filter(user=request.user).exclude(id__in=synced_ids).delete()

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

    permission_classes = (AuthToken, )

    def get(self, request):

        stories = Feed.objects.filter(from_user=request.user)

        feeds = FeedSerializer(instance=stories, many=True).data

        return JSONResponse(feeds, status=200)

