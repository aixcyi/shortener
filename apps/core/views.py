import logging
from datetime import timedelta
from itertools import chain
from random import choices

from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.core.models import ShortLink
from apps.core.serializers import ShortLinkSerializer
from utils.http import BearerAuthentication, ResponseCode, resp

logger = logging.getLogger('shortener')
CHARSET = ''.join(chain(
    map(chr, range(ord('0'), ord('9'))),
    map(chr, range(ord('A'), ord('Z'))),
    map(chr, range(ord('a'), ord('z'))),
)) + '-_'


def generate() -> str:
    return ''.join(choices(CHARSET, k=settings.BITS))


class ShortLinkView(APIView):
    """
    管理短链接的 API 接口。
    """
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)
    throttle_classes = ()

    def get(self, request, *args, **kwargs):
        """
        列出用户生成的所有短链接。
        """
        recodes = ShortLink.objects.filter(creator=self.request.user)
        serializer = ShortLinkSerializer(recodes, many=True)
        return resp(serializer.data, code=ResponseCode.DONE)

    def post(self, request, *args, **kwargs):
        """
        生成短链接。
        """
        try:
            target: str = self.request.data['target']
            duration: int | None = self.request.data['during_days']
        except KeyError:
            return resp(msg='缺少参数。')
        if type(target) is not str or type(duration) is not int and duration is not None:
            return resp(msg='参数类型错误。')

        instant = now()
        expire_at = (instant + timedelta(days=duration)) if duration else None
        try:
            record = ShortLink.objects.create(
                shorts=generate(),
                target=target,
                creator=self.request.user,
                create_at=instant,
                expire_at=expire_at,
            )
        except Exception as e:
            logger.exception('短链接生成失败', exc_info=e)
            return resp(msg='短链接生成失败。')

        serializer = ShortLinkSerializer(record)
        return resp(serializer.data, code=ResponseCode.SUCCESS)

    def delete(self, request, *args, **kwargs):
        """
        删除短链接。
        """
        indexes = self.request.query_params.getlist('id')
        if not indexes:
            return resp(msg='缺少参数。')
        try:
            indexes = list(map(int, indexes))
        except ValueError:
            return resp(msg='参数类型错误。')

        recodes = ShortLink.objects.filter(creator=self.request.user, id__in=indexes)
        recodes.delete()
        return resp(code=ResponseCode.DONE)


class AccessView(APIView):
    """
    短链接跳转原链接的视图。
    """
    authentication_classes = ()
    permission_classes = ()
    throttle_classes = ()

    def get(self, request: Request, shorts: str, *args, **kwargs):
        # 查找缓存
        target = cache.get(f'target:{shorts}', default=None)
        if target:
            return redirect(target)

        # 查找数据库
        try:
            record = ShortLink.objects.get(shorts=shorts)
        except ShortLink.DoesNotExist:
            raise Http404 from None
        cache.set(f'target:{record.shorts}', record.target, timeout=1 * 60 * 60)  # 缓存1个小时

        # 进行重定向
        return redirect(record.target)
