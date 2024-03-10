from django.urls import re_path

from apps.core.views import AccessView, ShortLinkView

urlpatterns = [
    re_path('^links/$', ShortLinkView.as_view()),
    re_path('^(?P<shorts>[0-9A-Za-z_-]{1,16})$', AccessView.as_view()),  # 数据库最多存储 16 个字符。
]
