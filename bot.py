# -*- coding: utf-8 -*-
"""Telegram bot generates route of date by parameters given by a user.

Asks for starting point of the date as coordinates or metro-station.
Gets a sequence of places' types you would like to visit. Lastly returns
generated chain of specific locations according to the given sequence and
starting point.
"""

from random import choice
import re
import telebot

from date_gen import DateGenerator
from db_req import DataBase
from task import Task
from tokens import TOKEN
from utility import TEXTS, WORDS


BOT = telebot.TeleBot(TOKEN)
TASK = Task()  # Keeps track of users' state.


@BOT.message_handler(commands=['start', 'go'])
def start_handler(message):
    """Answers to the initial message of each user.

    Creates the user in Task. Asks for the coordinates as the first step of
    collecting information. Passes action to an ask_coord function.

    Attributes:
        message(obj): Object specific for telebot. Contains data such as text
            and chat.id.
    """
    u_id = message.chat.id
    TASK.add_user(u_id)
    next_step(message, "hello", ask_coord)


@BOT.message_handler(content_types=['text'])
def text_handler(message):
    """Answers to the user once generating is done or there is no information
    about user (because of reset or so).

    Depends on input redirects user to needed message-handler.

    Attributes:
        message(obj): Object specific for telebot. Contains data such as text
            and chat.id.
    """
    u_id = message.chat.id
    if not TASK.is_exist(u_id):
        TASK.add_user(u_id)
    text = message.text.strip().lower()
    if text == "заново" or \
            not TASK.get_init_coord(u_id) or not TASK.get_seq(u_id):
        TASK.set_init_coord(u_id, tuple())
        TASK.set_seq(u_id, list())
        next_step(message, "ask_coord", ask_coord)
    elif text in ["ещё", "еще"]:
        next_step(message, "ready", response)
    elif text == "начало":
        TASK.set_init_coord(u_id, tuple())
        next_step(message, "ask_coord", ask_coord)
    elif text == "места":
        TASK.set_seq(u_id, list())
        next_step(message, "ask_seq", ask_seq)
    else:
        BOT.send_message(u_id, TEXTS["end"])


def ask_coord(message):
    """Tries to get a starting point from an input.

    First uses regex to check if there are coordinates in the given message.
    Absent coordinates lead to checking if the message is a name of the metro
    station. If so takes the station's coordinates as the starting point.
    Choice of the next function depends on Task state.

    Attributes:
        message(obj): Object specific for telebot. Contains data such as text
            and chat.id.
    """
    u_id = message.chat.id
    text = message.text.strip().lower()
    init_coord = tuple()
    check = re.findall(r"\d+[\,\.]\d+", text)
    if len(check) == 2:
        init_coord = tuple(float(x.replace(',', '.')) for x in check)
    else:
        df_m = DataBase().select_places_by_type("метро")  # Uses db_req.py.
        if text in df_m["name"].values:
            row = df_m[df_m["name"] == text]
            init_coord = (row["latitude"].iloc[0], row["longitude"].iloc[0])
        else:
            next_step(message, "wrong_coord", ask_coord)
            return

    TASK.set_init_coord(u_id, init_coord)

    if not TASK.get_seq(u_id):
        next_step(message, "ask_seq", ask_seq)
    else:
        next_step(message, "ready", response)


def ask_seq(message):
    """Tries to get a sequence from the input.

    First uses regex to check if there are words in the given message.
    Can generate short random sequence. Passes action to response function.

    Attributes:
        message(obj): Object specific for telebot. Contains data such as text
            and chat.id.
    """
    u_id = message.chat.id
    text = message.text.strip().lower()
    check = re.findall(r"[a-zа-яё]+", text)
    if not check:
        next_step(message, "wrong_seq", ask_seq)
        return
    if "случайно" in check:
        check = [choice(WORDS["fun"]), choice(WORDS["eat"] + WORDS["drink"]),
                 "загс"]
    else:  # Handles some generalizing words.
        for i in range(len(check)):
            if check[i] in ["покушать", "поесть", "есть"]:
                check[i] = choice(WORDS["eat"])
            elif check[i] in ["выпить", "попить", "пить"]:
                check[i] = choice(WORDS["drink"])
            elif check[i] in ["повеселиться", "развлечься",
                              "поразвлекаться", "развлекаться"]:
                check[i] = choice(WORDS["fun"])
    TASK.set_seq(u_id, check)
    next_step(message, "ready", response)


def response(u_id):
    """Generates date and sends it to the user.

    Function called once the collection of the needed information is over.
    Cuts sequence if it is too large. Uses date_gen.py to get generated list.

    Attributes:
        u_id(int): ID of the user for sending the message to. Uses id directly
            instead of a message object, because the function does not need
            to proceed action any further.
    """
    if len(TASK.get_seq(u_id)) > 8:
        BOT.send_message(u_id, TEXTS["too_much"])
    d_g = DateGenerator(TASK.get_seq(u_id)[:8], TASK.get_init_coord(u_id))
    for place in d_g.get_gened_seq():
        BOT.send_message(u_id, TEXTS["place"](place))
    BOT.send_message(u_id, TEXTS["end"])


def next_step(message, text, func):
    """Passes action to the next stage.

    Function increases code readability and manages the absence of the needed
    message on the last stage.

    Attributes:
        message(obj): Object specific for telebot. Contains data such as text
            and chat.id.
        text(str): Name of text from the utility.py to send.
        func(function): Function for giving action to.
    """
    msg = BOT.send_message(message.chat.id, TEXTS[text])
    if func.__name__ == "response":
        response(message.chat.id)
    else:
        BOT.register_next_step_handler(msg, func)


BOT.polling()
