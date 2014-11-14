# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView

try:
    # Only import from channels if it is a dependancy
    from channels import views as channels_views

    # Use channel mixin if channels is found as a dependancy
    ChannelListMixin = channels_views.ChannelListMixin
    ChannelDetailMixin = channels_views.ChannelDetailMixin
except ImportError:
    ChannelDetailMixin = ChannelListMixin = object

from .models import Post


class AllPosts(ChannelListMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        if hasattr(self.request, 'channel'):
            channel = self.request.channel
        else:
            channel = None

        return self.model.objects.published(
            self.request.user,
            channel).filter(**self.kwargs)


all_posts = AllPosts.as_view()


class DetailPost(ChannelDetailMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_queryset(self):
        if hasattr(self.request, 'channel'):
            channel = self.request.channel
        else:
            channel = None

        return self.model.objects.published(
            self.request.user,
            channel).filter(**self.kwargs)


detail = DetailPost.as_view()
