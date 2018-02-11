# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import requests
from django.utils import timezone
from rest_framework import status

from django.http import HttpResponse
from django.views.generic import View, TemplateView
from appStuff.models import AppUser, Advertisement

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from appStuff.models import AppUser, UserAdvertisementViewed, Advertisement
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

logger = logging.getLogger(__name__)


def parse_google_data(data):
    keys_to_check = ['administrative_area_level_1', 'locality', 'country']
    key_map = {
        'administrative_area_level_1': 'city',
        'locality': 'area',
        'country': 'country'
    }
    response = {}
    if len(data['results']):
        json_objects = data['results'][0]['address_components']
        for json_obj in json_objects:
            for google_type in json_obj['types']:
                if google_type in keys_to_check:
                    response[key_map[google_type]] = json_obj['long_name']
    return response


# Create your views here.
class UserAuthView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserAuthView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_dict = json.loads(request.body)
        fb_id = request_dict.get('fb_id')
        name = request_dict.get('name')
        gender = request_dict.get('gender')
        latitude = request_dict.get('lat')
        longitude = request_dict.get('lon')
        if fb_id and name:
            (app_user, created) = AppUser.objects.update_or_create(fb_id=fb_id,
                                                                   defaults={
                                                                        'name': name,
                                                                        'gender': gender,
                                                                        'latitude': latitude,
                                                                        'longitude': longitude,
                                                                        'last_logged_in_at': timezone.now()
                                                                    })
            if created:
                params = {
                    'latlng': '{},{}'.format(latitude, longitude),
                    'key': settings.API_KEY
                }
                response = requests.get(settings.GOOGLE_API, params=params)
                data = response.json()
                parsed_google_data = parse_google_data(data)
                if parsed_google_data:
                    AppUser.objects.filter(fb_id=fb_id).update(**parsed_google_data)
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse('No email present in request', status=status.HTTP_400_BAD_REQUEST)


class UserAdView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserAdView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        fb_id = request.GET.get('fb_id')
        if fb_id:
            response = {'results': [key['advertisement__key'] for key in
                                    UserAdvertisementViewed.objects.filter(
                                       app_user__fb_id=fb_id).values(
                                       'advertisement__key').distinct(
                                       'advertisement').order_by('advertisement',
                                                                 '-view_start_at')
                                    ]
                        }
            return JsonResponse(response)
        else:
            return HttpResponse('Missing fb_id', status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode')
        fb_id = request.POST.get('user_id')
        adv_id = request.POST.get('adv_id')

        if mode and fb_id and adv_id:
            if mode == 'Close':
                UserAdvertisementViewed.objects.filter(app_user__fb_id=fb_id,
                                                       advertisement__key=adv_id,
                                                       is_closed=False).update(
                    view_end_at=timezone.now(), is_closed=True
                )
                return HttpResponse('Done!', status.HTTP_200_OK)
            elif mode == 'Open':
                try:
                    user = AppUser.objects.get(fb_id=fb_id)
                except AppUser.DoesNotExist:
                    return HttpResponse('No such user', status=status.HTTP_400_BAD_REQUEST)
                try:
                    advertisement = Advertisement.objects.get(key=adv_id)
                except Advertisement.DoesNotExist:
                    return HttpResponse('Invalid advertisement', status=status.HTTP_400_BAD_REQUEST)
                UserAdvertisementViewed.objects.create(app_user=user, advertisement=advertisement)
                return HttpResponse('Done!', status.HTTP_200_OK)
        else:
            return HttpResponse('Invalid parameters', status.HTTP_400_BAD_REQUEST)


class AdvertisementAnalyticsView(TemplateView):

    template_name = "analytics.html"

    def get_context_data(self, **kwargs):
        advertisement_id = kwargs["ad_id"]
        advertisement = Advertisement.objects.get(id=advertisement_id)
        return advertisement.calculate_advertisement_analytics()
