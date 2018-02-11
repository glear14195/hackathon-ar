from __future__ import absolute_import

from django.conf.urls import url

from appStuff.views import AdvertisementAnalyticsView, UserAuthView, UserAdView

urlpatterns = [
    url(r'analytics/', AdvertisementAnalyticsView.as_view()),
    url(r'post_login/', UserAuthView.as_view()),
    url(r'history/', UserAdView.as_view()),
    url(r'ad_view/', UserAdView.as_view())
]
