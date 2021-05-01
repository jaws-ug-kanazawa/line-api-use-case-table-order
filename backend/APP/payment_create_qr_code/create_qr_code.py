import json
import os
import logging

from common import (common_const, utils, line)
from validation.table_order_param_check import TableOrderParamCheck
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501

import paypayopa

# 環境変数
REDIRECT_URL = os.environ.get("REDIRECT_URL")
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
LIFF_CHANNEL_ID = os.getenv('LIFF_CHANNEL_ID', None)
# Pay Pay API情報
PAY_PAY_API_KEY = os.environ.get("PAY_PAY_API_KEY")
PAY_PAY_API_SECRET = os.environ.get("PAY_PAY_API_SECRET")
PAY_PAY_API_MERCHANTPAYMENTID = os.environ.get("PAY_PAY_API_MERCHANTPAYMENTID")
if (os.environ.get("PAY_PAY_IS_PROD") == 'True'
    or os.environ.get("PAY_PAY_IS_PROD") == 'true'): 
    PAY_PAY_IS_PROD = True
else:
    PAY_PAY_IS_PROD = False

client = paypayopa.Client(auth=(PAY_PAY_API_KEY, PAY_PAY_API_SECRET),
                         production_mode=PAY_PAY_IS_PROD)
client.set_assume_merchant(PAY_PAY_API_MERCHANTPAYMENTID)

# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
# テーブル操作クラスの初期化
payment_order_table_controller = TableOrderPaymentOrderInfo()


def lambda_handler(event, context):
    """
    PayPay API(reserve)の通信結果を返す
    Parameters
    ----------
    event : dict
        POST時に渡されたパラメータ
    context : dict
        コンテキスト内容
    Returns
    -------
    response : dict
        PayPay APIの通信結果
    """

    logger.info(event)
    if event['body'] is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)
    req_body = json.loads(event['body'])

    # ユーザーID取得
    try:
        user_profile = line.get_profile(req_body['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            req_body['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    # パラメータバリデーションチェック
    param_checker = TableOrderParamCheck(req_body)

    if error_msg := param_checker.check_api_payment_reserve():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    payment_id = req_body['paymentId']
    payment_info = payment_order_table_controller.get_item(payment_id)
    amount = int(payment_info['amount'])
    request = {
        "merchantPaymentId": payment_id,
        "codeType": "ORDER_QR",
        "redirectUrl": f'{REDIRECT_URL}/tableorder/paymentCompleted?orderId={payment_id}',
        "redirectType":"WEB_LINK",
        "orderDescription":'LINE Use Case Barger',
        "orderItems": [{
            "name": 'オーダー商品',
            "category": "pasteries",
            "quantity": 1,
            "productId": "67678",
            "unitPrice": {
                "amount": amount,
                "currency": "JPY"
            }
        }],
        "amount": {
            "amount": amount,
            "currency": "JPY"
        },
    }

    try:
        resp = client.Code.create_qr_code(request)
        
        # 返却データ
        res_body = json.dumps(resp)
    except Exception as e:
        logger.error('Occur Exception: %s', e)
        return utils.create_error_response("Error")
    else:
        if resp['resultInfo']['code'] == 'SUCCESS':
            return utils.create_success_response(res_body)
        else:
            return utils.create_error_response("Error")
