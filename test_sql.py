from MensajesDatabase import MensajesDatabase

import os
import datetime

database_name =  'parcial_3.db'
database_file = './' + database_name

if not os.path.isfile(database_file):
    #creacion de base de datos y tabla Usuario
    mensajeDB = MensajesDatabase(database_name)
    mensajeDB.sql_connection()
    mensajeDB.sql_table
    #insercion de datos
    mensajeDB.sql_insert((0,'origen@email.iweb','destino@email.iweb','Primer mensaje', date.today()),0)


db = MensajesDatabase(database_name)
db.sql_connection()
print(db.sql_find_all())
print(db.sql_find_origen_destino('origen@email.iweb', 'destino@email.iweb'))
