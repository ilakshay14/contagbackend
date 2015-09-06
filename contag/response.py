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


VALIDATION_ERROR_MESSAGE = {"Message": "Validation error occurred!"}

UNKOWN_ERROR_MESSAGE = {"Message": "Unknown error occured!"}

OBJECT_DOES_NOT_EXIST = {"Message": "Object does not exist!"}