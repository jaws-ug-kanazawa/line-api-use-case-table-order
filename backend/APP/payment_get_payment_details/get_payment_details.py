import json
import logging
import os
import sys

from table_order import table_order_const
from common import (common_const, line, utils)
from validation.table_order_param_check import TableOrderParamCheck
from common.channel_access_token import ChannelAccessToken
from table_order.table_order_payment_order_info import TableOrderPaymentOrderInfo  # noqa501

import paypayopa

# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# PayPay API
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
channel_access_token_controller = ChannelAccessToken()

# LINE BOTリソースの宣言
CHANNEL_ID = os.getenv('LINE_CHANNEL_ID', None)
if CHANNEL_ID is None:
    logger.error('Specify CHANNEL_ID as environment variable.')
    sys.exit(1)


def send_messages(body):
    """
    OAにメッセージを送信する
    Parameters
    ----------
    body:dict
        該当ユーザーの支払情報
    Returns
    -------
    なし
    """
    flex_obj = table_order_const.const.FLEX_COUPON
    # DBより短期チャネルアクセストークンを取得
    channel_access_token = channel_access_token_controller.get_item(CHANNEL_ID)
    if channel_access_token is None:
        logger.error(
            'CHANNEL_ACCESS_TOKEN in Specified CHANNEL_ID: %s is not exist.',
            CHANNEL_ID)
    else:
        line.send_push_message(
            channel_access_token['channelAccessToken'], flex_obj, body['userId'])


def lambda_handler(event, context):
    """
    PayPay API(confirm)の処理結果を返す
    Parameters
    ----------
    event : dict
        POST時に渡されたパラメータ
    context : dict
        コンテキスト内容。
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

    # パラメータバリデーションチェック
    param_checker = TableOrderParamCheck(req_body)

    if error_msg := param_checker.check_api_get_payment_details():
        error_msg_disp = ('\n').join(error_msg)
        logger.error(error_msg_disp)
        return utils.create_error_response(error_msg_disp, status=400)  # noqa: E501

    payment_id = req_body['paymentId']
    transaction_id = 99999999999999

    try:
        # 注文履歴から決済金額を取得
        payment_info = payment_order_table_controller.get_item(
            payment_id)
        amount = float(payment_info['amount'])
        currency = 'JPY'
        # 会計テーブルを更新
        payment_order_table_controller.update_payment_info(
            payment_id, transaction_id)
        # PayPayAPI決済詳細取得
        try:
            resp = client.Payment.get_payment_details(payment_id)
            
            res_body = json.dumps(resp)
        except Exception as e:
            # PayPay側でエラーが発生した場合は会計テーブルを戻す
            logger.error('Occur Exception: %s', e)
            transaction_id = 0
            payment_order_table_controller.update_payment_info(
                payment_id, transaction_id)
            return utils.create_error_response("Error")
        else:
            if resp['resultInfo']['code'] == 'SUCCESS':
                # プッシュメッセージ送信
                send_messages(payment_info)
                return utils.create_success_response(res_body)
            else:
                # PayPay側でエラーが発生した場合は会計テーブルを戻す
                logger.error('Occur Exception: %s', e)
                transaction_id = 0
                payment_order_table_controller.update_payment_info(
                    payment_id, transaction_id)
                return utils.create_error_response("Error")


    except Exception as e:
        if transaction_id is not None and transaction_id == 0:
            logger.critical(
                'payment_id: %s could not update, please update transaction_id = 0 manually and confirm the payment',  # noqa 501
                payment_id)
        else:
            logger.error('Occur Exception: %s', e)
        return utils.create_error_response("Error")

