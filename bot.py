import telebot
from peewee import fn
from telebot.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

from MySqlConnection import TicketModel, my_database

bot = telebot.TeleBot('8071747416:AAHiZBONpp9_I0jjQOViK91Yzrh_3Y5J5Gg')


@bot.message_handler(commands=['start'])
def start_type(message):
    btn = telebot.types.InlineKeyboardMarkup()
    first_type = InlineKeyboardButton(text='Номер билета', callback_data='btn-1')
    second_type = InlineKeyboardButton(text='Названия title билета', callback_data='btn-2')
    third_type = InlineKeyboardButton(text='Все билеты', callback_data='btn-3')
    btn.add(first_type, second_type, third_type)
    bot.send_message(message.chat.id, 'Hello world, how are you today?', reply_markup=btn)


@bot.callback_query_handler(func=lambda callback: True)
def check_callback(callback):
    if callback.data == 'btn-2':
        bot.send_message(callback.message.chat.id, 'Введите название title билета')
        bot.register_next_step_handler(callback.message, handle_ticket_title)

    elif callback.data == 'btn-3':
        new_ticket_title(callback.message)


    elif callback.data == '/start':
        start_type(callback.message)
    else:

        ticket = TicketModel.get(number_of_ticket=int(callback.data))

        media = [InputMediaPhoto(file_url) for file_url in ticket.files]

        # Send the media group as a single message
        bot.send_message(callback.message.chat.id, f'{ticket.number_of_ticket} {ticket.title}')
        bot.send_media_group(callback.message.chat.id, media)
        markup = InlineKeyboardMarkup()
        start_button = InlineKeyboardButton(text="Вернуться к началу", callback_data='/start')
        markup.add(start_button)

        # Send the keyboard
        bot.send_message(callback.message.chat.id, "Нажмите кнопку ниже, чтобы вернуться к началу", reply_markup=markup)
        # bot.send_photo()


def handle_ticket_title(message):
    ticket_title = message.text  # The title entered by the user
    # print(ticket_title)
    query = TicketModel.select().where(fn.LOWER(TicketModel.title).contains(ticket_title.lower()))

    btn = telebot.types.InlineKeyboardMarkup()
    if query.count() > 0:
        for ticket in query:
            # print(ticket.title)
            new_type_btn = InlineKeyboardButton(text=f'{ticket.number_of_ticket}. {ticket.title}',
                                                callback_data=ticket.number_of_ticket)
            btn.add(new_type_btn)

    btn.add(InlineKeyboardButton(text='Назад', callback_data='/start'))
    bot.send_message(
        message.chat.id,
        'Результаты' if query.count() > 0 else 'Ничего не найдено',
        reply_markup=btn
    )
    # Here you can add more processing logic for ticket_title


def new_ticket_title(message):
    all_tickets = TicketModel.select().order_by('number_of_ticket')
    btn = telebot.types.InlineKeyboardMarkup()
    for ticket in all_tickets:
        new_type_btn = InlineKeyboardButton(text=f'{ticket.number_of_ticket}. {ticket.title}',
                                            callback_data=ticket.number_of_ticket)
        btn.add(new_type_btn)
    btn.add(InlineKeyboardButton(text='Назад', callback_data='/start'))
    bot.send_message(message.chat.id, 'Все билеты', reply_markup=btn)


bot.polling(none_stop=True)
