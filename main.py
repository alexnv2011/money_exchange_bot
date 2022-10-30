import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN, keys_currency


bot = telebot.TeleBot(TOKEN)

# help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.reply_to(message, 'Бот конвертирует валюты в текущем курсе.\nСписок всех доступных валют: /values\nВведите команду в следующем формате:\
     \n<Имя валюты, цену которой надо узнать> <Имя валюты, в которой надо узнать цену первой валюты> <Количество первой валюты>')


# Доступные валюты
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys_currency:
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

# перевод валюты
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_m = message.text.split(' ')
        if len(values_m) != 3:
            raise APIException('Должно быть 3 параметра!')
        quote, base, amount = values_m
        total = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {keys_currency[quote]} в {keys_currency[base]}: {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
