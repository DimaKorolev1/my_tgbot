import telebot
import emoji
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

# подключаем токен бота
bot = telebot.TeleBot(TOKEN)


# обработчик команд start и help
@bot.message_handler(commands=["start", "help"])
def start_test(message: telebot.types.Message):
    text = f"Hello, *{message.from_user.first_name}*\n"\
           "I can search for courses currencies.\n"\
           "Click to see available currencies:  /values"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# обработчик команды values. Каждая валюта выводится на новой строке
@bot.message_handler(commands=["values"])
def values_com(message: telebot.types.Message):
    text = "*Available currency:*"
    for key in keys.keys():
        text = emoji.emojize("\n:white_small_square: ".join((text, key)))
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    # инструкция ввода для пользователя
    bot.send_message(message.chat.id, "*Example entry: currency currency 1 (with a space)*", parse_mode="Markdown")


# обработчик текста от пользователя
@bot.message_handler(content_types=["text"])
def converter(message: telebot.types.Message):
    try:
        # полученный текст делаем строчным и разделяем пробелом три переменные
        values = message.text.lower().split(" ")

        # если пользователь ввел меньше 2 объектов
        if len(values) != 3:
            raise ConvertionException("Incorrect number of parameters.")

        # три переменные, полученные от пользователя - две валюты и количество
        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
        # определение ошибок внутри бота и ошибок пользователя
    except ConvertionException as e:
        bot.send_message(message.chat.id, f"User error:\n{e}", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to process command:\n{e}.")
        # вывод ответа пользователю
    else:
        text = f"*{amount} {base} = {total_base} {quote}*"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")


# бесконечная работа бота
bot.polling(none_stop=True)