from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from faino.AuthSystem.models import TempLink
from faino.WebServer.utils import get_client_ip


def Update_device(request, link):

    temp = get_object_or_404(TempLink, link=link)
    # ip_client = get_client_ip(request)
    # print(ip_client)
    # if temp.check_expired == True or temp.is_valid_ip(ip_client) == False:
    #     return Http404()

    file = temp.file
    filename = file.name

    response = HttpResponse(file)
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response
