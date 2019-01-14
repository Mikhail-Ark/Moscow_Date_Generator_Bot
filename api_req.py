# -*- coding: utf-8 -*-
"""The file contains functions of interaction with the Yandex Map API."""

import requests

from tokens import APIKEY


def search_on_map(place, coord):
    """Function interacts with the Yandex Map API in order to find places
    on the map in some area around certain coordinates.

    Attributes:
        place(str): Place to look for on the map.
        coord(tuple): Two floats as coordinates of the middle of an area.

    Returns:
        JSON response of the API in the form of python dict.
    """
    url = f"https://search-maps.yandex.ru/v1/?apikey={APIKEY}"
    query = '&'.join([url, "lang=ru_RU", f"text={place}", "type=biz",
                      f"ll={','.join(map(str, coord[::-1]))}", "spn=0.1,0.1"])
    return requests.get(query).json()
