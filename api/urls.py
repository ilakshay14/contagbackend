from django.conf.urls import url
from views import LoginView, OTPView, ContactView, FeedView, UserView, ProfileRequestView, \
BlockMuteView, NotificationView

urlpatterns = [
    url(r'login/', LoginView.as_view()),
    url(r'otp/', OTPView.as_view()),
    url(r'contact/', ContactView.as_view()),
    url(r'feed/', FeedView.as_view()),
    url(r'user/', UserView.as_view()),
    url(r'profile_request/', ProfileRequestView.as_view()),
    url(r'block_mute/', BlockMuteView.as_view()),
    url(r'notification/', NotificationView.as_view())
]
