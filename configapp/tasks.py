import time
import requests
import logging
from django.conf import settings
from celery import shared_task
logger = logging.getLogger(__name__)
@shared_task
def send_telegram_notification(order_id, product_name, quantity, customer_email, phone_number):
    logger.info(f"Telegram task started for order #{order_id}")
    logger.info("Sleeping for 5 seconds...")
    time.sleep(5)
    token = settings.TELEGRAM_BOT_TOKEN
    method = 'sendMessage'
    message_text = (
        f"Yangi buyurtma\n\n"
        f"Order ID: {order_id}\n"
        f"Product: {product_name}\n"
        f"Quantity: {quantity}\n"
        f"Client: {customer_email}\n"
        f"Tel: {phone_number}"
    )
    try:
        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/{method}',
            data={'chat_id': 6038582393, 'text': message_text}
        ).json()
        logger.info(f"Telegramga yuborildi: {response}")
    except Exception as e:
        logger.error(f"Telegram xatosi: {e}")
    logger.info(f" Task finished for order #{order_id}")
