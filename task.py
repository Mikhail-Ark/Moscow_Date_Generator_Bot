# -*- coding: utf-8 -*-
"""The file contains class objects of which tracks states of requests."""


class Task:
    """Object tracks a user's state of a request. Can maintain interactions
    with several users at the same time.
    """
    def __init__(self):
        """Creates a dict of users, each user will have unique u_id."""
        self.users = {}

    def add_user(self, u_id):
        """Add a user to the dict of users. Each user is also a dict with
        two fields: coordinates to start with and required sequence of places
        to visit, both initially empty.

        Attributes:
            u_id(int): ID of a user got from telebot's message object.
        """
        self.users[u_id] = {"init_coord": tuple(), "seq": list()}

    def is_exist(self, u_id):
        """Returns True if the user with the given u_id is in the list."""
        return u_id in self.users
#        try:
#            self.users[u_id]
#            return True
#        except KeyError:
#            return False

    def set_init_coord(self, u_id, coord):
        """Setter for the given user's initial coordinates.

        Attrubutes:
            u_id(int): ID of a user got from telebot's message object.
            coord(tuple): Two floats as coordinates of a start.
        """
        self.users[u_id]["init_coord"] = coord

    def set_seq(self, u_id, seq):
        """Setter for the given user's sequence of places.

        Attributes:
            u_id(int): ID of a user got from telebot's message object.
            seq(list): List of strings. Sequence of places' types.
        """
#        print(seq)  # for tracking sequences generated randomly.
        self.users[u_id]["seq"] = seq

    def get_init_coord(self, u_id):
        """Getter for specified user's starting coordinates.

        Attributes:
            u_id(int): ID of a user got from telebot's message object.

        Returns:
            coord(tuple): Two floats as coordinates.
        """
        return self.users[u_id]["init_coord"]

    def get_seq(self, u_id):
        """Getter for specified user's choosen sequence of places to visit.

        Attributes:
            u_id(int): ID of a user got from telebot's message object.

        Returns:
            seq(list): List of strings. Sequence of places' types.
            """
        return self.users[u_id]["seq"]
