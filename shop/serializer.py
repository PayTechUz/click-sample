from rest_framework import serializers


class URLSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True)
    return_url = serializers.URLField(required=False, allow_null=True)
