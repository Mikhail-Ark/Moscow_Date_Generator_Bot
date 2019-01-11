# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 22:53:32 2019

@author: M_Ark
"""

from random import choice
import re
import telebot

from date_gen import DateGenerator
from db_req import select_places_by_type
from task import Task
from tokens import TOKEN
from utility import texts, eat, drink, fun


bot = telebot.TeleBot(TOKEN)
task = Task()


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    u_id = message.chat.id
    task.add_user(u_id)
    next_step(message, "hello", ask_coord)
        

@bot.message_handler(content_types=['text'])
def text_handler(message):
    u_id = message.chat.id
    if not task.is_exist(u_id):
        task.add_user(u_id)
    text = message.text.strip().lower()
    if text == "заново" or \
            not task.get_init_coord(u_id) or not task.get_seq(u_id):
        task.set_init_coord(u_id, tuple())
        task.set_seq(u_id, list())
        next_step(message, "ask_coord", ask_coord)
    elif text in ["ещё", "еще"]:
        next_step(message, "ready", response)
    elif text == "начало":
        task.set_init_coord(u_id, tuple())
        next_step(message, "ask_coord", ask_coord)
    elif text == "места":
        task.set_seq(u_id, list())
        next_step(message, "ask_seq", ask_seq)
    else:
        bot.send_message(u_id, texts["end"])


def ask_coord(message):
    u_id = message.chat.id
    text = message.text.strip().lower()
    init_coord = tuple()
    check = re.findall(r"\d+[\,\.]\d+", text)
    if len(check) == 2:
        init_coord = tuple(float(x.replace(',', '.')) for x in check)
    else:
        df_m = select_places_by_type("метро")        
        if text in df_m["name"].values:
            row = df_m[df_m["name"] == text]
            init_coord = (row["latitude"].iloc[0], row["longitude"].iloc[0])
        else:
            next_step(message, "wrong_coord", ask_coord)
            return

    task.set_init_coord(u_id, init_coord)
    
    if not task.get_seq(u_id):
        next_step(message, "ask_seq", ask_seq)
    else:
        next_step(message, "ready", response)
        

def ask_seq(message):
    u_id = message.chat.id
    text = message.text.strip().lower()
    check = re.findall(r"[a-zа-яё]+", text)
    if len(check) == 0:
        next_step(message, "wrong_seq", ask_seq)
        return
    elif "случайно" in check:
        task.set_seq(u_id,
            [choice(fun), choice(eat + drink), "загс"])
        print(task.get_seq(u_id))
        next_step(message, "ready", response)
    else:
        for i in range(len(check)):
            if check[i] in ["покушать", "поесть", "есть"]:
                check[i] = choice(eat)
            elif check[i] in ["выпить", "попить", "пить"]:
                check[i] = choice(drink)
            elif check[i] in ["повеселиться", "развлечься",
                      "поразвлекаться", "развлекаться"]:
                check[i] = choice(fun)                
        task.set_seq(u_id, check)
        next_step(message, "ready", response)


def response(u_id):
    if len(task.get_seq(u_id)) > 8:
        bot.send_message(u_id, texts["too_much"])
    dg = DateGenerator(task.get_seq(u_id)[:8], task.get_init_coord(u_id))
    for place in dg.get_gened_seq():
        bot.send_message(u_id, texts["place"](place))
    bot.send_message(u_id, texts["end"])
    


def next_step(message, text, func):
    msg = bot.send_message(message.chat.id, texts[text])
    if func.__name__ == "response":
        response(message.chat.id)
    else:
        bot.register_next_step_handler(msg, func)


bot.polling()
