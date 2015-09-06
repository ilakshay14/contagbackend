import datetime
import traceback
from random import randint



from rest_framework.views import APIView
from django.utils import timezone
from contag.APIPermissions import AuthToken

from contag.response import JSONResponse, UNKOWN_ERROR_MESSAGE, VALIDATION_ERROR_MESSAGE
from models import OTPModel, Contact
from serializers import ContactSyncSerializer, ContactViewSerializer


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


class ContactView(APIView):

    permission_classes = (AuthToken, )

    def post(self, request):

        try:
            # Create/Update whatever contacts come from the app
            print request.user.name
            print '------------------------------------------'
            contacts = ContactSyncSerializer(many=True, context={'current_user': request.user})
            synced_contacts = contacts.create(validated_data=request.data)
            print synced_contacts
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

    def put(self, request):

        pass
