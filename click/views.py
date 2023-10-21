from typing import Type

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Request, Response

from click.interfaces import ClickUz
from click.models import Status, Transaction
from click.serializer import ClickUzSerializer
from click.utils import StatusCodes, click_authorization


class ClickUzMerchantAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    VALIDATE_CLASS: Type[ClickUz] = None

    @swagger_auto_schema(
        operation_id='Prepare/Complete Endpoint',
        request_body=ClickUzSerializer, tags=['Click']
    )
    def post(self, request: Request):
        serializer = ClickUzSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        METHODS = {
            StatusCodes.PREPARE: self.prepare,
            StatusCodes.COMPLETE: self.complete
        }

        merchant_trans_id = serializer.validated_data['merchant_trans_id']
        amount = serializer.validated_data['amount']
        action = serializer.validated_data['action']

        if click_authorization(**serializer.validated_data) is False:
            return Response(
                {
                    "error": StatusCodes.AUTHORIZATION_FAIL_CODE,
                    "error_note": StatusCodes.AUTHORIZATION_FAIL
                }
            )

        assert self.VALIDATE_CLASS != None
        check_order = self.VALIDATE_CLASS().process_check_order(
            order_id=merchant_trans_id, amount=amount
        )
        if check_order is True:
            result = METHODS[action](
                **serializer.validated_data,
                response_data=serializer.validated_data
            )
            return Response(result)

        return Response({"error": check_order})

    def prepare(
        self,  # https://docs.click.uz/click-api-request/
        click_trans_id: int, amount: int,
        sign_string: str, sign_time: str,
        merchant_trans_id: str, response_data: dict,
        action: int, *args, **kwargs
    ) -> dict:
        transaction = Transaction.objects.create(
            click_trans_id=click_trans_id,
            merchant_trans_id=merchant_trans_id,
            amount=amount,
            action=StatusCodes.PREPARE,
            sign_string=sign_string,
            sign_datetime=sign_time,
        )
        response_data.update(merchant_prepare_id=transaction.pk)

        return self.filter_response(action, response_data)

    def complete(
        self,  # https://docs.click.uz/click-api-request/
        click_trans_id: int, amount: int, error: int,
        merchant_prepare_id: int, response_data: dict,
        action: int, *args, **kwargs
    ) -> dict:
        try:
            transaction = Transaction.objects.get(pk=merchant_prepare_id)

            if error == StatusCodes.A_LACK_OF_MONEY:
                response_data.update(error=StatusCodes.A_LACK_OF_MONEY_CODE)
                transaction.action = StatusCodes.A_LACK_OF_MONEY
                transaction.status = Status.CANCELED.as_string
                transaction.save()

                self.VALIDATE_CLASS().cancel_payment(
                    transaction.merchant_trans_id, transaction
                )
                return response_data

            if transaction.action == StatusCodes.A_LACK_OF_MONEY:
                response_data.update(error=StatusCodes.A_LACK_OF_MONEY_CODE)
                return response_data

            if transaction.amount != amount:
                response_data.update(error=StatusCodes.INVALID_AMOUNT)
                return response_data

            if transaction.action == action:
                response_data.update(error=StatusCodes.INVALID_ACTION)
                return response_data

            transaction.action = action
            transaction.status = Status.FINISHED.as_string
            transaction.save()

            response_data.update(merchant_confirm_id=transaction.pk)

            self.VALIDATE_CLASS().process_successful_payment(
                transaction.merchant_trans_id, transaction
            )

            return self.filter_response(action, response_data)
        except Transaction.DoesNotExist:
            response_data.update(error=StatusCodes.TRANSACTION_NOT_FOUND)
            return response_data

    def filter_response(self, action: int, data: dict) -> dict:
        default_keys = [
            'click_trans_id',
            'merchant_trans_id',
            'error',
            'error_note'
        ]
        desired_keys = {
            0: default_keys + ['merchant_prepare_id'],
            1: default_keys + ['merchant_confirm_id'],
        }

        return {
            key: data[key] for key in desired_keys[action] if key in data
        }
