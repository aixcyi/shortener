from rest_framework import serializers

from apps.core.models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):
    """
    短链接记录的序列化器。
    """
    link = serializers.SerializerMethodField()

    def get_link(self, instance: ShortLink):
        return instance.link

    class Meta:
        model = ShortLink
        fields = ('id', 'link', 'target', 'expire_at')
