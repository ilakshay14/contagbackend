import datetime
from random import randint

from rest_framework.views import APIView
from django.utils import timezone

from contag.response import JSONResponse
from models import OTPModel


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
