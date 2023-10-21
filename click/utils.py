import hashlib
import typing as t

from django.conf import settings


def click_authorization(
    click_trans_id: int, amount: int, action: int,
    sign_time: str, sign_string: str, merchant_trans_id: str,
    merchant_prepare_id: t.Union[int, None] = None, *args, **kwargs
) -> bool:
    assert settings.CLICK_SETTINGS.get('service_id') != None
    assert settings.CLICK_SETTINGS.get('secret_key') != None
    assert settings.CLICK_SETTINGS.get('merchant_id') != None

    service_id = settings.CLICK_SETTINGS['service_id']
    secret_key = settings.CLICK_SETTINGS['secret_key']

    text = f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}"

    if merchant_prepare_id != "" and merchant_prepare_id is not None:
        text += f"{merchant_prepare_id}"

    text += f"{amount}{action}{sign_time}"
    hash = hashlib.md5(text.encode('utf-8')).hexdigest()

    if hash != sign_string:
        return False

    return True


class StatusCodes:

    INVALID_AMOUNT = -2
    INVALID_ACTION = -4

    TRANSACTION_NOT_FOUND = -6
    ORDER_NOT_FOUND = -5

    A_LACK_OF_MONEY_CODE = -9
    AUTHORIZATION_FAIL_CODE = -1

    PREPARE = 0
    COMPLETE = 1

    A_LACK_OF_MONEY = -5017
    AUTHORIZATION_FAIL = 'AUTHORIZATION_FAIL'

    ORDER_FOUND = True
