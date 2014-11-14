# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

from entropy import base
from entropy.base import (
    TitleMixin, SlugMixin, CreatedMixin, ModifiedMixin, EnabledMixin,
    MetadataMixin, AttributeMixin
)

from templates.mixins import TemplateMixin

try:
    from images.mixins import ImageMixin
except ImportError:
    ImageMixin = models.Model


class PostManager(models.Manager):
    """
    Get items that should be visible to the currently logged in user
        - if no user is provided, only published items will be returned
        - if channels is provided, filter by channel

    """

    def published(self, user=None, channel=None):
        if user and user.is_staff:
            min_published_status = base.DRAFT
        else:
            min_published_status = base.PUBLISHED

        # Check channels is installed and set to true before using
        try:
            from channels import settings as channels_settings
            if channel and channels_settings.USE_CHANNELS:
                query = self.channel(channel)
            else:
                raise ImportError
        except ImportError:
            query = self.all()

        return query.filter(
            publishing_status__gte=min_published_status
        ).order_by('-created_at')


class PostBase(TitleMixin, SlugMixin, CreatedMixin, ModifiedMixin,
               EnabledMixin, MetadataMixin, AttributeMixin, TemplateMixin,
               ImageMixin):
    """
    Post is the elemetary model of Content.  This class is abstract and
    utilised by the class below.

    """

    # title
    # short_title
    # slug
    # enabled
    # created_at
    # created_by
    # modified_at
    # modified_by
    # attributes
    # images

    byline = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    published_date = models.DateField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Post(PostBase):
    def get_absolute_url(self):
        """Returns the absolute url for a single post instance"""

        return reverse('posts_detail_post', args=(self.slug, ))

    @staticmethod
    def get_list_url():
        """
        Returns the absolute url for all post objects. This is a static method.

        """

        return reverse('posts_all_posts')
