import typing as t
from urllib.parse import urlencode

from django.conf import settings

from click.utils import StatusCodes


class ClickUz:
    ORDER_FOUND = StatusCodes.ORDER_FOUND
    ORDER_NOT_FOUND = StatusCodes.ORDER_NOT_FOUND
    INVALID_AMOUNT = StatusCodes.INVALID_AMOUNT

    def process_check_order(self, order_id: str, amount: int):
        """
        Check the status of an order.

        :param order_id: The unique identifier for the order.
        :param amount: The total amount of the order.

        :return: Possible return values:
            - 'ORDER_NOT_FOUND' if the order does not exist.
            - 'ORDER_FOUND'     if the order is found and its amount matches.
            - 'INVALID_AMOUNT'  if the order is found but the amount doesn't match.
        """
        raise NotImplemented

    def process_successful_payment(self, order_id: str, transaction: object) -> None:
        """
        Process a successful payment for an order.

        :param order_id:    The unique identifier for the order.
        :param transaction: A transaction object containing payment details.

        This method should be implemented to handle a successful payment.
        """
        raise NotImplemented

    def cancel_payment(self, order_id: str, transaction: object) -> None:
        """
        Cancel a payment transaction.

        This method is not yet implemented for cancellation of transactions.
        :param order_id:    The unique identifier for the order.
        :param transaction: A transaction object to be canceled.

        Subclasses may implement this method in the future to support transaction cancellation.
        """
        raise NotImplemented

    @staticmethod
    def generate_url(order_id: str, amount: int, return_url: t.Union[str, None] = None) -> str:
        service_id = settings.CLICK_SETTINGS['service_id']
        merchant_id = settings.CLICK_SETTINGS['merchant_id']

        base_url = "https://my.click.uz/services/pay"
        params = {
            "service_id": service_id,
            "merchant_id": merchant_id,
            "amount": amount,
            "transaction_param": order_id,
        }

        if return_url:
            params["return_url"] = return_url

        url = f"{base_url}?{urlencode(params)}"

        return url
