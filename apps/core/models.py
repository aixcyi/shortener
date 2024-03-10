from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.timezone import now

from utils.models import SnakeModel


class MemberManger(UserManager):
    """
    系统用户管理器。

    这个管理器的默认查询集会剔除已注销用户（is_active=False）。
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser, metaclass=SnakeModel):
    """
    系统用户。
    """
    username = models.CharField('用户名', max_length=50, unique=True, validators=[AbstractUser.username_validator])
    nickname = models.CharField('昵称', max_length=100, null=True, default=None)

    objects = UserManager()
    members = MemberManger()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ShortLink(models.Model, metaclass=SnakeModel):
    """
    短链接记录表。
    """
    shorts = models.CharField('短链接字符', max_length=16, unique=True, db_index=True)
    target = models.URLField('长链接', max_length=256)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    create_at = models.DateTimeField('创建时间')
    expire_at = models.DateTimeField('过期时间', null=True, default=None, blank=True)

    @property
    def link(self) -> str:
        return f'{settings.ROOT}/{self.shorts}'

    @property
    def is_expired(self) -> bool:
        return self.expire_at < now()
