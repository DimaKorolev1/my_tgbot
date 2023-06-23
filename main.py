import telebot
import emoji
import config
from config import *
from telebot import types
from extensions import ConvertionException, CryptoConverter


def create_markup(base=None):
    base_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for key in keys.keys():
        if key != base:
            buttons.append(types.KeyboardButton(key.capitalize()))

    base_markup.add(*buttons)
    return base_markup


# подключаем токен бота
bot = telebot.TeleBot(TOKEN)


# обработчик команд start и help
@bot.message_handler(commands=["start", "help"])
def start_bot(message: telebot.types.Message):
    text = f"Hello, *{message.from_user.first_name}*\n"\
           "I can search for courses currencies.\n"\
           "Click to see available currencies:  /convert"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["convert"])
def values_com(message: telebot.types.Message):
    text = "Select the currency from which to convert:"
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = "Select the currency to convert to:"
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, sym_handler, base)


def sym_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = "Select the amount of currency:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)


def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = CryptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Data entry error..")
    else:
        text = f"*{amount}* {base} = *{new_price}* {quote}"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")


# бесконечная работа бота
bot.polling(none_stop=True)