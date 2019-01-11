# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 20:23:51 2019

@author: M_Ark
"""

class Task(object):
    def __init__(self):
        self.users = {}
        
    def add_user(self, u_id):
        self.users[u_id] = {"init_coord": tuple(), "seq": list()}
        
    def is_exist(self, u_id):
        try:
            self.users[u_id]
            return True
        except KeyError:
            return False
        
    def set_init_coord(self, u_id, coord):
        self.users[u_id]["init_coord"] = coord
        
    def set_seq(self, u_id, seq):
        print(seq)
        self.users[u_id]["seq"] = seq

    
    def get_init_coord(self, u_id):
        return self.users[u_id]["init_coord"]
    
    def get_seq(self, u_id):
        return self.users[u_id]["seq"]
