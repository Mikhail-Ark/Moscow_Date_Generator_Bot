# -*- coding: utf-8 -*-
"""File contains class for interaction with the DB."""

import sqlite3 as sql
import pandas as pd


class DataBase:
    """Class for keeping DB interactions in one place."""

    DB = "./data/data.db"

    def create_connection(self):
        """Creates a connection with DB according to the documentation of
        sqlite3.

        Attributes:
            db(path): Location of .db file in the system.
        """
        try:
            conn = sql.connect(self.DB)
            return conn
        except sql.Error as e:
            print(e)
        return None

    def select_places_by_type(self, pl_type):
        """Requests DB in a certain form.

        Attributes:
            pl_type(str): Type of places to select.

        Returns:
            Pandas DataFrame which contains all information about places
                of the given type from the DB.
        """
        conn = self.create_connection()
        with conn:
            query = f"SELECT * FROM places WHERE type='{pl_type}'"
            return pd.read_sql_query(query, conn)
