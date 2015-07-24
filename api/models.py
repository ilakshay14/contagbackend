from django.db import models


class AdminGroup(models.Model):
    #TODO Add choices here
    group_name = models.CharField(null=False, max_length=255, unique=True)


class AdminPlatform(models.Model):

    platform_name = models.CharField(null=False, max_length=255)
    is_api_available = models.BooleanField(default=False)
    sync_type = models.CharField(null=False, max_length=55,
                                 choices=(('api', "Platform API"), ('link', "Link to platform profile"), ('handle', "Handle or username")), default='link')
    priority = models.IntegerField(null=True)
    is_binary = models.BooleanField(null=False, default=True)


class User(models.Model):

    name = models.CharField(null=False, max_length=255)
    contag = models.CharField(null=False, max_length=8)
    mobile_number = models.CharField(max_length=100, null=False)
    landline_number = models.CharField(max_length=100, null=True)
    emergency_contact_number = models.CharField(max_length=100, null=True)
    is_mobile_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, default='f')
    personal_email = models.CharField(max_length=255, null=True)
    registered_with = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=500)
    work_email = models.CharField(max_length=255, null=True)
    work_mobile_number = models.CharField(max_length=100, null=True)
    work_landline_number = models.CharField(max_length=100, null=True)
    work_address = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    work_facebook_page = models.CharField(max_length=100, null=True)
    android_app_link = models.CharField(max_length=100, null=True)
    ios_app_link = models.CharField(max_length=100, null=True)
    avatar_url = models.CharField(max_length=500)
    blood_group = models.CharField(max_length=55)
    date_of_birth = models.DateField()
    marital_status = models.BooleanField(default=False)
    marriage_anniversary = models.DateField()
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class AccessToken(models.Model):

    access_token = models.CharField(max_length=100, null=False)
    device_id = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User)
    device_type = models.CharField(max_length=10, choices=(('android', 'Android Devices'),
                                                           ('ios', 'iOS Devices'), ('web', 'Browser')))
    active = models.BooleanField(default=True)
    push_id = models.CharField(max_length=200, null=True)
    last_login = models.DateTimeField()
    app_version_id = models.IntegerField()
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class Contact(models.Model):

    user = models.ForeignKey(User)
    contact_name = models.CharField(null=False, max_length=255)
    contact_number = models.CharField(null=True, max_length=255)
    is_on_contag = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    invited_on = models.DateTimeField()
    contact_contag_user = models.ForeignKey(User, null=True, related_name="Contag_Contact")
    group_type = models.ForeignKey(AdminGroup, default=1)
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_muted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

class UserInterest(models.Model):

    user = models.ForeignKey(User)
    interest = models.CharField(max_length=255, null=False)
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class UserPlatform(models.Model):

    platform = models.ForeignKey(AdminPlatform)
    platform_id = models.IntegerField(null=False)
    platform_token = models.CharField(max_length=200)
    platform_secret = models.CharField(max_length=200)
    platform_permissions = models.CharField(max_length=255)
    platform_email = models.CharField(max_length=255, null=True)
    user_id = models.IntegerField(null=False)
    is_public = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class BlockedList(models.Model):

    by_user = models.ForeignKey(User, null=False)
    for_user = models.ForeignKey(User, null=False, related_name="blocked_user")
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class OTPToken(models.Model):

    user = models.ForeignKey(User, null=False)
    contact_number = models.CharField(null=False, max_length=255)
    token = models.CharField(null=False, max_length=55)
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class ProfileRequest(models.Model):

    for_user = models.ForeignKey(User, null=False)
    to_user = models.ForeignKey(User, null=False, related_name="requested_user")
    request_type = models.CharField(null=False, max_length=255)
    created_on = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)


class Feed(models.Model):

    pass


class Notification(models.Model):

    pass


class PushNotification(models.Model):

    pass





