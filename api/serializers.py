from rest_framework import serializers
from models import User, Contact, UserInterest


class SUser(serializers.ModelSerializer):
    class Meta:
        model = User


# class SContact(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         depth = 2
#
#
# class SUserInterest(serializers.ModelSeriazlier):
#     class Meta:
#         model = UserInterest
#         depth = 1
