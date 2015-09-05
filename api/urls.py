from django.conf.urls import url
from views import LoginView, OTPView

urlpatterns = [
    url(r'login/', LoginView.as_view()),
    url(r'otp/', OTPView.as_view()),
]
