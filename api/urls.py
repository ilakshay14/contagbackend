from django.conf.urls import url
from views import LoginView, OTPView, CreateUserView

urlpatterns = [
    url(r'login/', LoginView.as_view()),
    url(r'otp/', OTPView.as_view()),
    url(r'otp/', CreateUserView.as_view()),
]
