import binascii
import os
from django.db import models
from random import randint
from django.utils import timezone
from utilities.sms import SMS


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


class SocialPlatform(models.Model):
    platform_name = models.CharField(null=False, max_length=255)
    is_api_available = models.BooleanField(default=False)
    sync_type = models.CharField(null=False, max_length=55,
                                 choices=(('api', "Platform API"), ('link', "Link to platform profile"),
                                          ('handle', "Handle or username")), default='link')
    priority = models.IntegerField(null=True)
    is_binary = models.BooleanField(null=False, default=True)


class Interests(models.Model):
    interest = models.CharField(max_length=1055)


class User(TimeStampedModel):
    name = models.CharField(null=False, max_length=255)
    mobile_number = models.CharField(max_length=100, null=False)
    is_mobile_verified = models.BooleanField(default=False)

    #Always public short profile
    contag = models.CharField(null=False, max_length=8, unique=True)
    gender = models.CharField(max_length=1, default='f')
    status_update = models.CharField(max_length=255, null=True)

    # Personal profile
    landline_number = models.CharField(max_length=100, null=True)
    emergency_contact_number = models.CharField(max_length=100, null=True)
    personal_email = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=500, null=True)
    date_of_birth = models.DateField(null=True)
    marital_status = models.BooleanField(default=False)
    marriage_anniversary = models.DateField(null=True)

    #Professional profile
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

    def new_user(self):

        in_contacts_for = Contact.objects.filter(contact_number=self.mobile_number)

        if len(in_contacts_for):
            in_contacts_for.update(is_on_contag=True, contact_contag_user=self)
            # TODO create notification and create feed story
        else:
            return False

    def get_access_token(self, request_headers):
        (device_id, device_type, push_id, app_version_id) = request_headers["HTTP_X_DEVICE_ID"], \
                                                            request_headers["HTTP_X_DEVICE_TYPE"], \
                                                            request_headers["HTTP_X_PUSH_ID"], \
                                                            request_headers["HTTP_X_APP_VERSION_ID"]
        AccessToken.objects.filter(device_id=device_id, device_type=device_type).update(active=False)
        token = AccessToken.objects.create(user=self, device_type=device_type, device_id=device_id, push_id=push_id,
                                           last_login=timezone.now(), app_version_id=app_version_id)
        return token

    def logout(self, headers):
        AccessToken.objects.filter(access_token=headers['HTTP_TOKEN']).update(is_active=False)

        return True


class AccessToken(TimeStampedModel):
    access_token = models.CharField(max_length=100, null=False)
    device_id = models.CharField(max_length=50, null=False)
    user = models.ForeignKey(User)
    device_type = models.CharField(max_length=10, choices=(('android', 'Android Devices'),
                                                           ('ios', 'iOS Devices'), ('web', 'Browser')))
    active = models.BooleanField(default=True)
    push_id = models.CharField(max_length=200, null=True)
    last_login = models.DateTimeField()
    app_version_id = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = self.generate_token()
        return super(AccessToken, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.access_token


class OTPToken(TimeStampedModel):
    number = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)

    @classmethod
    def create(cls, number):
        otp_value = randint(100000, 999999)
        otp = cls(number=number, otp=otp_value)
        return otp

    def send(self):
        otp_message = "Dear user you One Time Password(OTP) for login to Contag is " + str(self.otp) + "."
        print(otp_message)
        sms = SMS()
        # if self.number == 9971528807:
        #     sms.send(self.number, otp_message)
        # sms.send(self.number, otp_message)
        sms.send(9971528807, otp_message)


class SocialProfile(TimeStampedModel):
    social_platform = models.ForeignKey(SocialPlatform)
    user = models.ForeignKey(User, related_name='social_profile')
    platform_id = models.CharField(null=False, max_length=1055)
    platform_token = models.CharField(max_length=200, null=True)
    platform_secret = models.CharField(max_length=200, null=True)
    platform_permissions = models.CharField(max_length=255, null=True)
    platform_email = models.CharField(max_length=255, null=True)


class UserInterest(models.Model):
    user = models.ForeignKey(User, related_name='user_interests')
    interest = models.ForeignKey(Interests)


class ProfileRight(models.Model):

    from_user = models.ForeignKey(User, related_name='profile_rights')
    unit_type = models.CharField(max_length=255)
    unit_id = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    visible_for = models.CharField(max_length=1055, null=True)


class ProfileRequest(TimeStampedModel):
    for_user = models.ForeignKey(User, null=False)
    from_user = models.ForeignKey(User, null=False, related_name="request_through")
    request_type = models.CharField(null=False, max_length=255)
    is_fulfilled = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)


class Contact(TimeStampedModel):
    user = models.ForeignKey(User)
    contact_name = models.CharField(null=False, max_length=255)
    contact_number = models.CharField(null=True, max_length=255)
    is_on_contag = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    invited_on = models.DateTimeField(null=True)
    contact_contag_user = models.ForeignKey(User, null=True, related_name="Contag_Contact")
    is_muted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_contag_user()
        super(Contact, self).save(*args, **kwargs)

    def is_contag_user(self):
        if not self.is_on_contag:
            contag_user = User.objects.filter(mobile_number=self.contact_number)
            if len(contag_user):
                self.is_on_contag = True
                self.contact_contag_user = contag_user[0]


class ShareContact(TimeStampedModel):

    from_user = models.ForeignKey(User)
    shared_with = models.ForeignKey(User, related_name='shareD_with')
    contact = models.ForeignKey(Contact)
    message = models.CharField(max_length=255)


class Feed(TimeStampedModel):
    from_user = models.ForeignKey('User')
    story_text = models.CharField(max_length=255)
    story_url = models.CharField(max_length=255)
    story_image = models.CharField(max_length=255)
    story_type = models.CharField(max_length=55)


class Notification(TimeStampedModel):

    user = models.ForeignKey(User)
    notification_type = models.CharField(max_length=255)
    text = models.CharField(max_length=1055)
    object_id = models.IntegerField(default=0)
    seen_at = models.DateTimeField(null=True)
    pushed_at = models.DateTimeField(null=True)
    device_id = models.CharField(max_length=45)
    push_id = models.CharField(max_length=105)



