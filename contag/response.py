from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, search=None, **kwargs):

        # In case of search we don't need to json render
        if search:
            content = data
        else:
            content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


VALIDATION_ERROR_MESSAGE = {"message": "Validation error occurred!"}

UNKOWN_ERROR_MESSAGE = {"message": "Unknown error occured!"}

OBJECT_DOES_NOT_EXIST = {"message": "Object does not exist!"}

REQUEST_ALREADY_EXISTS  = {"message": "Request already exists!"}

PROFILE_REQUEST_CREATED = {"message": "Profile request created!"}

SUCCESS_MESSAGE = {"result": True}

ERROR_MESSAGE = {"result": False}