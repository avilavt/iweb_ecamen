#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import urllib, json
from MensajesDatabase import MensajesDatabase
import sqlite3
import os
from datetime import date, datetime
import http.client
import base64
import codecs
from flask import Flask, render_template, redirect, url_for, request, session
import secrets
import requests
import json
import unicodedata
import xml.etree.ElementTree as ET

# http://localhost:5000

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = secrets.token_urlsafe(16)

#url_cliente = "http://127.0.0.1:5000"
url_cliente = "http://iwebexamen.appspot.com"

database_name =  'parcial_3.db'
database_file = './' + database_name

if not os.path.isfile(database_name):
    #creacion de base de datos y tabla Usuario
    mensajeDB = MensajesDatabase(database_name)
    mensajeDB.sql_connection()
    mensajeDB.sql_table
    #insercion de datos
    mensajeDB.sql_insert((0,'origen@email.iweb','destino@email.iweb','Primer mensaje', datetime.today()),0)

@app.route('/')
def home():
    origen = 'origen@email.iweb'
    if request.method == 'POST':
        response = request.form
        origen = response['email']
        print('Origen = '+ origen)

    return render_template('index.html',origen=origen,url_client=url_cliente)



@app.route('/messages', methods=['GET', 'POST'])
def home_email():
    origen = 'origen@email.iweb'
    destino = 'destino@email.iweb'
    if request.method == 'POST':
        response = request.form
        origen = response['origen']
        print('Origen = '+ origen)
        print('Destino = '+ destino)
        destino = response['destino']
        try:
            lista = list()
            index = 0
            mensajesDB = MensajesDatabase(database_name)
            mensajesDB.sql_connection()
            response = mensajesDB.sql_find_origen_destino(origen, destino)
            print(str(response))
            while index < len(response):
                mensaje = {'idMensaje' : response[index][0], 'origen' : response[index][1], 'destino': response[index][2], 'contenido': response[index][3], 'fecha_y_hora': response[index][4]}
                lista.append(mensaje)
                index += 1
            print(lista)
        except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    return render_template('mensajes.html',mensajes=lista,url_client=url_cliente)

@app.route('/send_messages', methods=['GET', 'POST'])
def send_messages():
    origen = 'origen@email.iweb'
    destino = 'destino@email.iweb'
    if request.method == 'POST':
        response = request.form
        origen = response['origen']
        print('Origen = '+ origen)
        destino = response['destino']
        print('Destino = '+ destino)
        contenido = response['contenido']
        print('Contenido = '+ contenido)
        try:
            mensajesDB = MensajesDatabase(database_name)
            mensajesDB.sql_connection()
            id = mensajesDB.sql_get_last_id() + 1
            mensajesDB.sql_insert((id, origen, destino, contenido, datetime.today()), id)
            lista = list()
            index = 0
            mensajesDB = MensajesDatabase(database_name)
            mensajesDB.sql_connection()
            response = mensajesDB.sql_find_origen_destino(origen, destino)
            print(str(response))
            while index < len(response):
                mensaje = {'idMensaje' : response[index][0], 'origen' : response[index][1], 'destino': response[index][2], 'contenido': response[index][3], 'fecha_y_hora': response[index][4]}
                lista.append(mensaje)
                index += 1
            print(lista)
        except RuntimeError as exc:
            mensaje, codigo = exc.args
            print(mensaje)
            print(codigo)
            return render_template("error.html", mensaje=mensaje, codigo=codigo)
    return render_template('mensajes.html',mensajes=lista,url_client=url_cliente)


if __name__ == '__main__':
    app.run(debug=True)
