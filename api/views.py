import datetime
from random import randint

from rest_framework.views import APIView
from django.utils import timezone

from contag.response import JSONResponse
from models import OTPToken


class LoginView(APIView):
    def post(self, request):
        number = request.data['number']
        otp_value = randint(100000, 999999)
        otp = OTPToken(number=number, otp=otp_value)
        otp.save()
        return JSONResponse({"success": "true"}, status=200)


class OTPView(APIView):
    def post(self, request):
        number = request.data['number']
        otp = request.data['otp']
        if OTPToken.objects.filter(updated_on__gte = (timezone.now() - datetime.timedelta(hours=2)),number=number, otp=otp).exists():
            return JSONResponse({"success": "true"}, status=200)
        else:
            return JSONResponse({"success": "false"}, status=200)
