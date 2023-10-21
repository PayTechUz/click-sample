import typing as t

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import Request, Response

from click.interfaces import ClickUz
from click.views import ClickUzMerchantAPIView
from shop.models import Order
from shop.serializer import URLSerializer


class OrderCheckAndPayment(ClickUz):
    def process_check_order(self, order_id: str, amount: int):
        try:
            # check the availability of your order
            order = Order.objects.get(order_id=order_id)

            # is the order amount entered correctly?
            if order.amount != amount:
                return ClickUz.INVALID_AMOUNT

            return ClickUz.ORDER_FOUND
        except Order.DoesNotExist:
            return ClickUz.ORDER_NOT_FOUND

    def process_successful_payment(self, order_id: str, _: object):
        # change order status
        order = Order.objects.get(order_id=order_id)
        order.status = True
        order.save()

        # notify users or admins
        ...

    def cancel_payment(self, order_id: str, _: object):
        # change order status
        order = Order.objects.get(order_id=order_id)
        order.status = False
        order.save()

        # refund or smth
        ...


class MyView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment

    @swagger_auto_schema(
        operation_id='GenerateLink/CheckOrderStatus Endpoint',
        query_serializer=URLSerializer, tags=['User']
    )
    def get(self, request: Request):
        serializer = URLSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data.get('order_id')
        return_url = serializer.validated_data.get('return_url')

        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

        return Response(
            {
                "link": ClickUz.generate_url(order.pk, order.amount, return_url),
                "status": order.status
            }
        )
