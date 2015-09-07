import datetime
from random import randint

from rest_framework.views import APIView
from django.utils import timezone
from utilities.sms import SMS
from contag.response import JSONResponse
from models import OTPToken, User, AccessToken
from serializers import SUser


class LoginView(APIView):
    def post(self, request):
        number = request.data['number']
        otp_value = randint(100000, 999999)
        otp = OTPToken(number=number, otp=otp_value)
        print(otp_value)
        otp.save()
        otp_message = "Dear user you One Time Password(OTP) for login to Contag is " + str(otp_value) + "."
        print(otp_message)
        sms = SMS()
        sms.send(number, otp_message)
        return JSONResponse({"success": "true"}, status=200)


class OTPView(APIView):
    def post(self, request):
        number = request.data['number']
        otp = request.data['otp']
        if OTPToken.objects.filter(updated_on__gte=(timezone.now() - datetime.timedelta(hours=2)), number=number,
                                   otp=otp).exists():
            if User.objects.filter(mobile_number=number).exists():
                user = User.objects.filter(mobile_number=number)
                access_token = user.get_access_token(request.META)
                print(access_token.access_token)
                user_serializer = SUser(user)
                return JSONResponse(
                    {"is_new_user": False, "success": True, "auth_token": access_token, "user": user_serializer},
                    status=200)
            else:
                return JSONResponse({"is_new_user": True, "success": True, "auth_token" : None, "user": None}, status=200)

        else:
            return JSONResponse({"is_new_user": False, "success": False, "auth_token" : None, "user": None}, status=200)


class CreateUserView(APIView):
    def post(self, request):
        return
