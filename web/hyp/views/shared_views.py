from django.shortcuts import render
from django.template import RequestContext
from .api_views import apiResponse

def handler404(request, *args, **argv):
    if request.content_type == "application/json":
        return apiResponse(
            status=404,
            message="Not found."
        )
    else:
        response = render(
            '404.html',
            {},
            context_instance=RequestContext(request)
        )
        response.status_code = 404
        return response

def handler500(request, *args, **argv):
    if request.content_type == "application/json":
        return apiResponse(
            status=500,
            message="Unexpected Hyp server error! Our developers have been notified."
        )
    else:
        response = render(
            '500.html',
            {},
            context_instance=RequestContext(request)
        )
        response.status_code = 500
        return response
