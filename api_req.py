# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 23:23:11 2019

@author: M_Ark
"""
import requests

from tokens import apikey

def search_on_map(place, coord):
    url = f"https://search-maps.yandex.ru/v1/?apikey={apikey}"
    query = '&'.join([url, "lang=ru_RU", f"text={place}", "type=biz",
                      f"ll={','.join(map(str, coord[::-1]))}", "spn=0.1,0.1"])
    return requests.get(query).json()
