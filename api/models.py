import binascii
import os
from django.db import models


class TimeStampedModel(models.Model):
    """ TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'updated_on'
        ordering = ('-updated_on', '-created_on',)
        abstract = True


class AdminPlatform(models.Model):

    platform_name = models.CharField(null=False, max_length=255)
    is_api_available = models.BooleanField(default=False)
    sync_type = models.CharField(null=False, max_length=55,
                                 choices=(('api', "Platform API"), ('link', "Link to platform profile"),
                                          ('handle', "Handle or username")), default='link')
    priority = models.IntegerField(null=True)
    is_binary = models.BooleanField(null=False, default=True)


class User(TimeStampedModel):

    name = models.CharField(null=False, max_length=255)
    contag = models.CharField(null=False, max_length=8)
    mobile_number = models.CharField(max_length=100, null=False)
    landline_number = models.CharField(max_length=100, null=True)
    emergency_contact_number = models.CharField(max_length=100, null=True)
    is_mobile_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, default='f')
    personal_email = models.CharField(max_length=255, null=True)
    registered_with = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=500, null=True)
    work_email = models.CharField(max_length=255, null=True)
    work_mobile_number = models.CharField(max_length=100, null=True)
    work_landline_number = models.CharField(max_length=100, null=True)
    work_address = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    work_facebook_page = models.CharField(max_length=100, null=True)
    android_app_link = models.CharField(max_length=100, null=True)
    ios_app_link = models.CharField(max_length=100, null=True)
    avatar_url = models.CharField(max_length=500, null=True)
    blood_group = models.CharField(max_length=55, null=True)
    date_of_birth = models.DateField()
    marital_status = models.BooleanField(default=False)
    marriage_anniversary = models.DateField()


    def get_access_token(self, request_headers):

        return

class AccessToken(TimeStampedModel):

    access_token = models.CharField(max_length=100, null=False)
    device_id = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User)
    device_type = models.CharField(max_length=10, choices=(('android', 'Android Devices'),
                                                           ('ios', 'iOS Devices'), ('web', 'Browser')))
    active = models.BooleanField(default=True)
    push_id = models.CharField(max_length=200, null=True)
    last_login = models.DateTimeField()
    app_version_id = models.IntegerField()



class Contact(TimeStampedModel):

    user = models.ForeignKey(User)
    contact_name = models.CharField(null=False, max_length=255)
    contact_number = models.CharField(null=True, max_length=255)
    is_on_contag = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    invited_on = models.DateTimeField()
    contact_contag_user = models.ForeignKey(User, null=True, related_name="Contag_Contact")
    is_muted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)


class UserInterest(TimeStampedModel):

    user = models.ForeignKey(User)
    interest = models.CharField(max_length=255, null=False)


class UserPlatform(TimeStampedModel):

    admin_platform = models.ForeignKey(AdminPlatform)
    user = models.ForeignKey('User')
    platform_id = models.IntegerField(null=False)
    platform_token = models.CharField(max_length=200, null=True)
    platform_secret = models.CharField(max_length=200, null=True)
    platform_permissions = models.CharField(max_length=255, null=True)
    platform_email = models.CharField(max_length=255, null=True)
    is_public = models.BooleanField(default=True)


class PlatformShare(TimeStampedModel):

    platform= models.ForeignKey('UserPlatform')
    shared_for = models.ForeignKey('User')


class BlockedList(TimeStampedModel):

    through_user = models.ForeignKey(User, null=False)
    blocked_user = models.ForeignKey(User, null=False, related_name="blocked_user")


class ProfileRequest(TimeStampedModel):

    for_user = models.ForeignKey(User, null=False)
    from_user = models.ForeignKey(User, null=False, related_name="request_through")
    request_type = models.CharField(null=False, max_length=255)


class Feed(TimeStampedModel):

    from_user = models.ForeignKey('User')
    story_text = models.CharField(max_length=255)
    story_url = models.CharField(max_length=255)
    story_image = models.CharField(max_length=255)


class Notification(models.Model):

    pass


class PushNotification(models.Model):

    pass


class OTPToken(TimeStampedModel):
    number = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)


