# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 00:04:57 2019

@author: M_Ark
"""
from random import choice

from api_req import search_on_map
from db_req import select_places_by_type


class DateGenerator(object):
    """"""
    types_in_db = ["кафе", "столовая", "закусочная", "кулинария", "фастфуд",
                   "ресторан", "кафетерий", "буфет", "бар", "метро", "загс"]
    
    def __init__(self, place_seq, init_coord):
        assert isinstance(place_seq, list) and \
            len(place_seq) > 0, "Incorrect place sequence"
        self.place_seq = place_seq
        self.init_coord = init_coord
        self.set_gened_seq(list())
        
    def set_gened_seq(self, gened_seq):
        self.gened_seq = gened_seq
        
    def get_types_in_db(self):
        return self.types_in_db
    
    def get_gened_seq(self):
        if not self.gened_seq:
            self.gen_seq()
        return self.gened_seq

    def gen_seq(self):
        gened_seq = list()
        for pl_type in self.place_seq:
            if len(gened_seq) == 0:
                coord = self.init_coord
            else:
                coord = (gened_seq[-1]["latitude"], gened_seq[-1]["longitude"])            
            if pl_type in self.get_types_in_db():
                options = self.gen_db(pl_type, coord, gened_seq)
            else:
                options = self.gen_api(pl_type, coord, gened_seq)
            
            options = list(filter(lambda x: x not in gened_seq, options))
            gened_place = choice(options)
            
            gened_seq.append(gened_place)
            
        self.set_gened_seq(gened_seq)


    def gen_db(self, pl_type, coord, gened_seq):
        df = select_places_by_type(pl_type)
        
        df["distance"] = df.apply((lambda x:
            ((x["latitude"]-coord[0])**2 + (x["longitude"]-coord[1])**2)**0.5),
            axis=1)
        options = df.sort_values(by="distance")[:10].to_dict("records")
        return options


    def gen_api(self, place, coord, gened_seq):
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
