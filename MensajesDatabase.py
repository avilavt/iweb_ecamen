import sqlite3
from sqlite3 import Error
from flask import Flask, request, Response, jsonify, json
import urllib, json


class MensajesDatabase:

    def __init__(self, database):
        self.database = database

    def sql_connection(self):
        try:
            self.con = sqlite3.connect(self.database)
            self.cursorObj = self.con.cursor()
            print("Connection is established: Database is created in memory")
        except Error:
            print(Error)

    def sql_table(self):
        query = "CREATE TABLE if not exists mensajes(id_mensaje integer PRIMARY KEY,origen text, destino text, contenido text, fecha_y_hora date)"
        self.cursorObj.execute(query)
        self.con.commit()

    def sql_insert(self,entities,id):
        query = "INSERT INTO mensajes(id_mensaje, origen, destino, contenido, fecha_y_hora) VALUES(?, ?, ?, ?, ?)"
        self.cursorObj.execute(query,entities)
        self.con.commit()
        response = self.sql_find(id)
        if len(response)==0:
            raise ValueError(['Operation not realized',"412"])
        return len(response)

    def sql_update_origen(self,new_origen,id):
        query = "UPDATE mensajes SET origen = \"" + str(new_origen) + "\" where id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_origen(id)
        return str(response) == str(new_origen)

    def sql_get_origen(self,id):
        lista = list()
        query = "SELECT origen FROM mensajes WHERE id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]


    def sql_update_destino(self,new_destino,id):
        query = "UPDATE mensajes SET destino = \"" + str(new_destino) + "\" where id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_destino(id)
        return str(response) == str(new_destino)

    def sql_get_destino(self,id):
        lista = list()
        query = "SELECT destino FROM mensajes WHERE id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_update_contenido(self,new_contenido,id):
        query = "UPDATE mensajes SET contenido = \"" + str(new_contenido) + "\" where id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_contenido(id)
        return str(response) == str(new_contenido)

    def sql_get_contenido(self,id):
        lista = list()
        query = "SELECT contenido FROM mensajes WHERE id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]


    def sql_update_fecha_y_hora(self,new_fecha_y_hora,id):
        query = "UPDATE mensajes SET fecha_y_hora = \"" + str(new_fecha_y_hora) + "\" where id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_fecha_y_hora(id)
        return str(response) == str(new_fecha_y_hora)

    def sql_get_fecha_y_hora(self,id):
        lista = list()
        query = "SELECT fecha_y_hora FROM mensajes WHERE id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_find_all(self):
        lista = list()
        query = "SELECT * FROM mensajes"
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Messages not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find(self,id):
        lista = list()
        query = "SELECT * FROM mensajes WHERE id_mensaje = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find_origen_destino(self,origen,destino):
        lista = list()
        query = "SELECT * FROM mensajes WHERE origen = \"" + str(origen) + "\" and destino = \"" + str(destino) + "\""
        #print('sql_find_origen_destino = ' + query)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find_by_patron(self,contenido):
        lista = list()
        patron = str('\"%') + contenido + str('%\"')
        patron.lower()
        print('El patron es: ' + patron)
        query = "SELECT * FROM mensajes WHERE lower(contenido) LIKE " + patron
        print(query)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Message not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_count(self):
        lista = list()
        response = self.sql_find_all()
        return len(response)

    def sql_remove(self,id):
        query = "DELETE FROM mensajes WHERE id_mensaje = "  + str(id)
        response = self.cursorObj.execute(query).rowcount
        self.con.commit()
        if response == 0:
            raise ValueError(['Message not found',"404"])
        return response

    def sql_close(self):
        self.con.close()

    def sql_get_last_id(self):
        last_index = 0;
        query = "SELECT max(id_mensaje) FROM mensajes"
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if rows:
            for row in rows:
                last_index = row
        return last_index[0]

if __name__ == '__main__':
    db = MensajesDatabase('parcial_3.db')
    db.sql_connection()
    db.sql_table()
