# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'posts.views',

    url(r'^$', 'all_posts', name='posts_all_posts'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail', name='posts_detail_post'),
)
