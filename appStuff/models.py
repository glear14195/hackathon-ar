# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AppUser(models.Model):
    name = models.CharField(max_length=200)
    fb_id = models.CharField(max_length=250, unique=True)
    gender = models.CharField(null=True, max_length=20)
    last_logged_in_at = models.DateTimeField(auto_now=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    area = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True, max_length=100)
    country = models.CharField(null=True, max_length=100)


class Advertiser(models.Model):
    user = models.ForeignKey(User)


class Advertisement(models.Model):
    advertiser = models.ForeignKey(Advertiser)
    title = models.CharField(max_length=120)
    key = models.CharField(max_length=100)
    ad_site = models.URLField(null=False)


class UserAdvertisementViewed(models.Model):
    app_user = models.ForeignKey(AppUser)
    advertisement = models.ForeignKey(Advertisement)
    view_start_at = models.DateTimeField(auto_now_add=True)
    view_end_at = models.DateTimeField(null=True)
    is_closed = models.BooleanField(default=False)

