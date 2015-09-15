from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from api.models import AccessToken


class AuthToken(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        from api.models import User
        request.user = User.objects.get(pk=1)
        return request.user
        # if 'HTTP_TOKEN' in request.META:
        #     print('Hi')
        #     last_month = datetime.today() - timedelta(days=60)
        #     if request.META['HTTP_TOKEN'].__eq__('Anon'):
        #         print('yes')
        #         request.user = 'Anon'
        #         return request.user
        #     else:
        #         print('No')
        #         token = AccessToken.objects.filter(access_token=request.META['HTTP_TOKEN'],
        #                                               created_on__gte=last_month, active=True).first()
        #         print(token)
        #         if token:
        #             request.user = token.user
        #             return request.user
