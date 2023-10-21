from rest_framework import serializers


class ClickUzSerializer(serializers.Serializer):
    # https://docs.click.uz/click-api-request/

    click_trans_id = serializers.CharField(allow_blank=True)
    service_id = serializers.CharField(allow_blank=True)
    click_paydoc_id = serializers.CharField(allow_blank=True)
    merchant_trans_id = serializers.CharField(allow_blank=True)
    amount = serializers.IntegerField()
    action = serializers.IntegerField()
    error = serializers.IntegerField()
    error_note = serializers.CharField(allow_blank=True)
    sign_time = serializers.CharField()
    sign_string = serializers.CharField(allow_blank=True)

    merchant_prepare_id = serializers.IntegerField(
        required=False, allow_null=True
    )
