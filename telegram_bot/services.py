import telebot
from django.conf import settings

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


def send_telegram_message(chat_id: int, text: str) -> bool:
    """
    Отправляет сообщение в Telegram.

    :param chat_id: ID чата (пользователя)
    :param text: Текст сообщения
    :return: True, если отправка успешна
    """
    try:
        bot.send_message(chat_id, text)
        return True
    except Exception as e:
        print(f'Ошибка отправки сообщения: {e}')
        return False
