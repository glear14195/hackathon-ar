from __future__ import absolute_import

from django.conf.urls import url
from appStuff.views import UserAuthView

urlpatterns = [
    url(r'post_login/', UserAuthView.as_view()),
]
