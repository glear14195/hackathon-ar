# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.utils import timezone
from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View
from appStuff.models import AppUser

logger = logging.getLogger(__name__)


# Create your views here.
class UserAuthView(View):
    def post(self, request, *args, **kwargs):
        email = request.GET.get('email_id')
        name = request.GET.get('name')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        if email and name:
            (app_user, created) = AppUser.objects.update_or_create(name=name, email=email,
                                                                       latitude=latitude,
                                                 longitude=longitude, defaults={
                                                    'last_logged_in_at': timezone.now()
                                                })
            if created:

            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse('No email present in request', status=status.HTTP_400_BAD_REQUEST)

class UserAdView(View):
