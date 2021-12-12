from database import write_to_database
from transitions import Machine
from dotenv import load_dotenv
from datetime import datetime
from os import getenv
import telebot


load_dotenv()


class MyState(object):
    states = ['asleep', 'stage 1', 'stage 2', 'stage 3']

    def __init__(self):
        self.machine = Machine(model=self, states=MyState.states, initial='asleep')
        self.machine.add_transition(trigger='wake_up', source='asleep', dest='stage 1')
        self.machine.add_transition(trigger='operate_1', source='stage 1', dest='stage 2')
        self.machine.add_transition(trigger='operate_2', source='stage 2', dest='stage 3')
        self.machine.add_transition(trigger='operate_3', source='stage 3', dest='asleep')
        self.machine.add_transition(trigger='cancel', source='*', dest='asleep')


bot = telebot.TeleBot(getenv('TOKEN'))

my_state = MyState()

data = {'messenger': 'telegram'}


def handler_my_state(_):
    match my_state.state:
        case 'stage 1':
            return True
        case 'stage 2':
            return True
        case 'stage 3':
            return True
        case _:
            return False


def data_definition(message):
    match message.text.lower():
        case 'маленькая' | 'маленькую':
            data['size'] = 'маленькую'
        case 'большая' | 'большую':
            data['size'] = 'большую'
        case 'наличка' | 'наличные' | 'наличными':
            data['payment'] = 'наличными'
        case 'картой' | 'карта':
            data['payment'] = 'картой'
        case 'отмена' | 'отменить':
            my_state.cancel()
            bot.send_message(message.chat.id, 'Заказ отменен.')
        case _:
            my_state.cancel()
            bot.send_message(message.chat.id, 'Не верный ввод. Заказ отменен.')


@bot.message_handler(commands=['start'])
def welcome_message(message):
    my_state.wake_up()
    bot.send_message(message.chat.id, 'Маленькую или большую?')


@bot.message_handler(func=handler_my_state)
def get_size(message):
    data_definition(message)
    my_state.operate_1()
    msg = bot.send_message(message.chat.id, 'Наличка или карта?')
    bot.register_next_step_handler(msg, get_pyment)


@bot.message_handler(func=handler_my_state)
def get_pyment(message):
    data_definition(message)
    my_state.operate_2()
    msg = bot.send_message(message.chat.id, f'Вы хотите {data["size"]} пиццу, оплата {data["payment"]}, верно?')
    bot.register_next_step_handler(msg, confirm)


@bot.message_handler(func=handler_my_state)
def confirm(message):
    match message.text.lower():
        case 'да' | 'yes' | 'д' | 'y':
            data['confirm'] = True
            data['date'] = datetime.now()
            my_state.operate_3()
            write_to_database(data)
            bot.send_message(message.chat.id, 'Готово.')

        case 'нет' | 'no' | 'н' | 'n':
            my_state.operate_3()
            data['confirm'] = False
            data['date'] = datetime.now()
            write_to_database(data)
            bot.send_message(message.chat.id, 'Не подтверждено.')
        case _:
            my_state.cancel()
            bot.send_message(message.chat.id, 'Не верный ввод.')


bot.infinity_polling(logger_level=10)
