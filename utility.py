# -*- coding: utf-8 -*-
"""The file contains some helpful objects for interaction with a user, such as
texts of answers and lists for random generation."""


def place_str(place):
    """Function prettifies response string

    Attributes:
        place(dict): Contains info about place such as a name, an address etc.

    Returns:
        Text describing one generated place to visit.
    """
    fields = list()
    if place["type"].split()[0].lower() not in place['name'].lower():
        fields.append(place["type"].capitalize())
    fields += [place["name"], place["address"]]
    try:
        fields.append(place["phone"])
    except KeyError:
        pass
    return "\n".join(fields)


TEXTS = {"hello": """Привет, это генератор свиданий!

Сначала напиши метро начала свидания или координаты.
Например "юго-западная"
или "55.66 37.48".""",
         "ask_seq": """Напиши чем бы хотел заняться или куда сходить.
Например "ресторан кинотеатр бар"
или "поесть, повеселиться, выпить".
Можно довериться судьбе командой "случайно".""",
         "ask_coord": """Напиши метро начала свидания или координаты.
Например "юго-западная"
или "55.66 37.48".""",
         "wrong_coord": """Где-то ошибка!
Напиши метро начала свидания или координаты.
Например "юго-западная"
или "55.66 37.48".""",
         "ready": "Спасибо! Генерирую вам свидание как заказывали...",
         "wrong_seq": """Где-то ошибка!
Напиши чем бы хотел заняться или куда сходить.
Например "ресторан кинотеатр бар"
или "поесть, повеселиться, выпить".
Можно довериться судьбе командой "случайно".""",
         "end": """"еще" сгенерировать ничего не меняя
"начало" чтобы изменить стартовую точку
"места" чтобы изменить список мест
"заново" чтобы начать заново""",
         "place": place_str,
         "too_much": """Врятли сможете за раз столько посетить...
Вот вам для начала!"""}

WORDS = {"eat": ["кафе", "столовая", "закусочная", "кулинария",
                 "фастфуд", "ресторан", "кафетерий", "буфет"],
         "drink": ["ресторан", "бар"],
         "fun": ["кинотеатр", "парк", "каток", "театр", "музей",
                 "боулинг", "аквапарк", "тир"]}
