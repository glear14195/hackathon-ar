# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import timedelta, datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models import F, Sum, Count, Avg
from django.db.models.functions import TruncDay


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

    def __unicode__(self):
        return self.user.username


class Advertisement(models.Model):
    advertiser = models.ForeignKey(Advertiser)
    title = models.CharField(max_length=120)
    key = models.CharField(unique=True, max_length=100)
    ad_site = models.URLField(null=False)

    def __unicode__(self):
        return self.title

    def calculate_advertisement_analytics(self):

        view_data = UserAdvertisementViewed.objects.filter(advertisement_id=self.id, is_closed=True).annotate(
            time_spent=F("view_end_at")-F("view_start_at"),
        ).aggregate(time_spent_sum=Sum("time_spent"), total_views=Count("id"), total_distinct=Count(
            "app_user", distinct=True))
        if view_data:
            total_views = view_data["total_views"]
            total_distinct = view_data["total_distinct"]
            if view_data["time_spent_sum"]:
                time_spent_per_view_seconds = view_data["time_spent_sum"].total_seconds()/total_views
            else:
                time_spent_per_view_seconds = 0
        returning_users_count = UserAdvertisementViewed.objects.filter(advertisement_id=self.id).values(
            "app_user"
        ).annotate(c=Count("id")).filter(c__gte=2).count()

        location_wise_data = UserAdvertisementViewed.objects.filter(
            advertisement_id=self.id
        ).values("app_user__city").annotate(c=Count("id")).values_list(
            "app_user__city",
            "c"
        )

        gender_wise_data = UserAdvertisementViewed.objects.filter(
            advertisement_id=self.id
        ).values("app_user__gender").annotate(c=Count("id")).values_list(
            "app_user__gender",
            "c"
        )

        date_wise_date = UserAdvertisementViewed.objects.filter(
            advertisement_id=self.id, view_start_at__gte=timezone.now()-timedelta(days=7)
        ).annotate(
            day=TruncDay('view_start_at')
        ).values("day").annotate(c=Count("id")).order_by("day").values_list(
            "day",
            "c"
        )

        geo_wise_time = UserAdvertisementViewed.objects.filter(
            advertisement_id=self.id, is_closed=True
        ).values('app_user__city').annotate(c=Avg(F('view_end_at')-F('view_start_at'))).order_by(
            'app_user__city').values_list(
            'app_user__city',
            'c'
        )

        location_labels, location_values = self.transform_data_for_charts(location_wise_data)
        gender_labels, gender_values = self.transform_data_for_charts(gender_wise_data)
        date_labels, date_values = self.transform_data_for_charts(date_wise_date)
        time_labels, time_values = self.transform_data_for_charts(geo_wise_time)
        context = {
            "total_views": total_views,
            "total_distinct": total_distinct,
            "avg_time_spent": time_spent_per_view_seconds,
            "returning_users": returning_users_count,
            "location_data": json.dumps(
                {
                    "labels": location_labels,
                    "values": location_values
                }
            ),
            "gender_data": json.dumps(
                {
                    "labels": gender_labels,
                    "values": gender_values
                }
            ),
            "date_data": json.dumps(
                {
                    "labels": date_labels,
                    "values": date_values
                }
            ),
            "time_data": json.dumps(
                {
                    "labels": time_labels,
                    "values": time_values
                }
            ),
            "id": self.id
        }

        return context

    def transform_data_for_charts(self, data):
        labels = []
        values = []
        for data_point in data:
            label = data_point[0]
            value = data_point[1]

            if type(label) is datetime:
                label = label.strftime("%d %b")
            if type(value) is datetime:
                value = value.strftime("%d %b")
            elif type(value) is timedelta:
                value = value.total_seconds()
            labels.append(label)
            values.append(value)

        return labels, values


class UserAdvertisementViewed(models.Model):
    app_user = models.ForeignKey(AppUser)
    advertisement = models.ForeignKey(Advertisement)
    view_start_at = models.DateTimeField(auto_now_add=True)
    view_end_at = models.DateTimeField(null=True)
    is_closed = models.BooleanField(default=False)
