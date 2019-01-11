# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 13:28:36 2019

@author: annak
"""
import pandas as pd
import sqlite3 as sql

db = "./data/data.db"
 
def create_connection(db):
    try:
        conn = sql.connect(db)
        return conn
    except sql.Error as e:
        print(e)
    return None
    
def select_places_by_type(pl_type):
    conn = create_connection(db)
    with conn:
        query = f"SELECT * FROM places WHERE type='{pl_type}'"
        return pd.read_sql_query(query, conn)
