import telebot
from config import keys, TOKEN
from extensions import APIExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '''Бот создан для конвертации валют.
Инструкция по использованию бота.
Чтобы конвертировать валюту отправьте боту сообщение в формате:
<имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>
Для просмотра доступных валют введите комманду "/values"'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюту'
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        params = message.text.split(' ')

        if len(params) != 3:
            raise APIExeption('''Введён неверный формат запроса.
Чтобы конвертировать валюту отправьте боту сообщение в формате:
<имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>''')

        quote, base, amount = params
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f' Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()