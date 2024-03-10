from django.db.models import IntegerChoices
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class ResponseCode(IntegerChoices):
    SUCCESS = 1, '成功'
    DONE = 0, '完毕'
    FAIL = -1, '失败'


def resp(data=None, msg: str = None, code: ResponseCode = ResponseCode.FAIL):
    return Response({
        'code': code.value,
        'message': msg or code.label,
        'data': data,
    })
