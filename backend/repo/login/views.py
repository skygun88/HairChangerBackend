from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse, FileResponse
import sqlite3
import json

def login(request, content=None):
    print('Login API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get ID & Password data from POST request'''
        user_id = json.loads(request.body).get('id')
        user_pw = json.loads(request.body).get('password')
        print(f'Received : {user_id} / {user_pw}')

        ''' Get all user login data from sqlite3 DB '''
        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT * FROM login_logininfo;")
        rows = cur.fetchall()
        rows = list(map(lambda x: (x[0], x[1]), rows))
        print(rows)

        ''' Check whether requested ID & Password is in DB '''
        if (user_id, user_pw) in rows:
            print('found id')
            cur.execute(f'SELECT uid, username, usertype, profile_image  FROM user_userinfo WHERE uid=\'{user_id}\';')
            user_infos = cur.fetchall()[0]
            print(user_infos)

            ''' Get profile image from DB '''
            result['profile'] = ''
            if user_infos[3] != None:
                profile_path = user_infos[3]
                with open(profile_path, mode='rb') as file:
                    img = file.read()
                result['profile'] = base64.encodebytes(img).decode("utf-8")
                
            result['user_id'] = user_infos[0]
            result['user_name'] = user_infos[1]
            result['user_type'] = user_infos[2]
            result['status'] = 'OK'
        else:
            print('not found')
        conn.close()

    return JsonResponse(result)


def register(request, content=None):
    print('Register API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get ID & Password & Name & Type data from POST request'''
        user_id = json.loads(request.body).get('id')
        user_pw = json.loads(request.body).get('password')
        user_name = json.loads(request.body).get('name')
        # user_type = int(json.loads(request.body).get('user_type'))
        user_type = 0
        print(f'Received : {user_id} / {user_pw} / {user_name} / {user_type}')

        ''' Get all user login data from sqlite3 DB '''
        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT * FROM login_logininfo;")
        rows = cur.fetchall()
        rows = list(map(lambda x: x[0], rows))

        ''' Append new user data into DB '''
        if not user_id in rows:
            cur.execute('INSERT INTO login_logininfo (uid, password) VALUES (?, ?);', (user_id, user_pw))
            cur.execute('INSERT INTO user_userinfo (uid, username, usertype, profile_image) VALUES (?, ?, ?, null);', (user_id, user_name, user_type))
            conn.commit()
            result['status'] = 'OK'
        else:
            print('Duplicate ID error')
        conn.close()
    return JsonResponse(result)
