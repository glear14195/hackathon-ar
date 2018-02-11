# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from appStuff.models import Advertisement, Advertiser
# Register your models here.


class AdvertiserAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request):
        return False


class AdvertisementAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
