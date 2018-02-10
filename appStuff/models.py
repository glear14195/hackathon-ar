# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AppUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    last_logged_in_at = models.DateTimeField(auto_now=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Advertiser(models.Model):
    user = models.ForeignKey(User)


class Advertisement(models.Model):
    advertiser = models.ForeignKey(Advertiser)
    title = models.CharField(max_length=120)


class UserAdvertisementViewed(models.Model):
    app_user = models.ForeignKey(AppUser)
    advertisement = models.ForeignKey(Advertisement)
    viewed_at = models.DateTimeField(auto_now_add=True)
