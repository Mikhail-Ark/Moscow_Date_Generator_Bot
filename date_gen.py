# -*- coding: utf-8 -*-
"""The file contains a class which gets a request from bot.py, queries a list
of possible places to visit from db_req.py and api_req.py, post-processes
responses and makes the final list of places. In fact, this is middle layer
between user interface (bot.py) and inner information-getters.
"""

from random import choice

from api_req import search_on_map
from db_req import DataBase


class DateGenerator:
    """Uses the given data to generate a list of places for visiting.

    Demands sequence of places and coordinates for start.
    Generates list according to the rules: for each place in the sequence
    checks if such type in the DB. If so asks DB for 10 closest places
    of the type, filters it and randomly chooses one of them as the next
    element of the list. Uses previous element as the starting point.
    Yandex Map API is used for types not in DB.
    get_gened_seq method returns generated list of places.
    """
    types_in_db = ["кафе", "столовая", "закусочная", "кулинария", "фастфуд",
                   "ресторан", "кафетерий", "буфет", "бар", "метро", "загс"]

    def __init__(self, place_seq, init_coord):
        """Creates an empty object with the sequence and the starting
        coordinates.

        Attributes:
            place_seq(list): List of strings. Sequence of places' types.
            init_coord(tuple): Two floats as starting coordinates.
        """
        self.place_seq = place_seq
        self.init_coord = init_coord
        self.set_gened_seq(list())

    def set_gened_seq(self, gened_seq):
        """Setter for places' sequence.

        Attributes:
            gened_seq(list): Chain of places to visit.
        """
        self.gened_seq = gened_seq

    def get_types_in_db(self):
        """Getter of places' types which must be taken from DB.

        Returns:
            List of strings.
        """
        return self.types_in_db

    def get_gened_seq(self):
        """Getter of the generated list. Calls generating function if needed.

        Returns:
            List of dicts. Each dict contains info about a place to visit.
        """
        if not self.gened_seq:
            self.gen_seq()
        return self.gened_seq

    def gen_seq(self):
        """Generates a list of places to visit.

        Defines the way (DB or API) of getting options to choose from. Calls
        function to get the top 10 most suitable places. Randomly chooses one
        of them. Avoids repetitions by filtering in advance.
        """
        gened_seq = list()
        for pl_type in self.place_seq:
            if not gened_seq:
                coord = self.init_coord
            else:
                coord = (gened_seq[-1]["latitude"], gened_seq[-1]["longitude"])
            if pl_type in self.get_types_in_db():
                options = self.gen_db(pl_type, coord)
            else:
                options = self.gen_api(pl_type, coord)

            options = list(filter(lambda x: x not in gened_seq, options))
            gened_place = choice(options)

            gened_seq.append(gened_place)

        self.set_gened_seq(gened_seq)

    def gen_db(self, pl_type, coord):
        """Generates the top 10 closest places of the type using DB.

        Calls function from db_req.py to select all places of the type.
        Counts distance and takes the top 10 closest.

        Attributes:
            pl_type(str): Place type to take.
            coord(tuple): Two floats as coordinates to count distance.

        Returns:
            List of 10 dicts to choose from. Each dict contains info about
                a place such as name, address etc.
        """
        df = DataBase().select_places_by_type(pl_type)

        df["distance"] = df.apply((lambda x:
                                   ((x["latitude"]-coord[0])**2 +
                                    (x["longitude"]-coord[1])**2)**0.5),
                                  axis=1)
        options = df.sort_values(by="distance")[:10].to_dict("records")
        return options

    def gen_api(self, place, coord):
        """Generates the top 10 closest places of the type using Yandex API.

        Calls function from api_req.py to find the top 10 suitable places
        matching a query.
        Processes response of the API to make a list of dicts.

        Attributes:
            place(str): Place to look for on the map.
            coord(tuple): Two floats as coordinates to count distance.

        Returns:
            List of 10 dicts to choose from. Each dict contains info about
                a place such as a name, an address etc.
        """
        raw_resp = search_on_map(place, coord)
        options = list()
        for i in raw_resp["features"]:
            variant = dict()
            variant["longitude"] = i["geometry"]["coordinates"][0]
            variant["latitude"] = i["geometry"]["coordinates"][1]

            info = i["properties"]["CompanyMetaData"]
            variant["name"] = info["name"]
            variant["address"] = info["address"]
            variant["type"] = info["Categories"][0]["name"]

            try:
                variant["phone"] = info["Phones"][0]["formatted"]
            except KeyError:
                pass

            options.append(variant)
        return options
