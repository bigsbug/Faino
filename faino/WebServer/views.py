from django import views
from django.http import HttpResponse, Http404, JsonResponse

from django.shortcuts import get_object_or_404

from rest_framework import status as Status

from faino.AuthSystem.models import Temp_link

from faino.WebServer.utils import get_client_ip

from django.core.mail import send_mail, EmailMessage


def Update_device(request, link):

    temp = get_object_or_404(Temp_link, link=link)
    # ip_client = get_client_ip(request)
    # print(ip_client)
    # if temp.check_expired == True or temp.check_ip(ip_client) == False:
    #     return Http404()

    file = temp.file
    filename = file.name

    response = HttpResponse(file)
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response
