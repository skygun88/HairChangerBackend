from django.shortcuts import render
import json
import sqlite3
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
import os
import sys
import base64
from PIL import Image


def test(request, content=None):
    print('Test API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        img_path = '/home/ubuntu/backend/repo/media/result/2020-12-05_033346.jpg'
        with open(img_path, mode='rb') as file:
            img = file.read()
        result['img'] = base64.encodebytes(img).decode("utf-8")
        result['len'] = 3
        result['list'] = ['a', 'b', 'c']
        result['status'] = 'OK'

    return JsonResponse(result)


# Create your views here.
def swapRequest(request, content=None):
    print('Swap API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get request information from json '''
        user_id = request.POST.get('id').replace('\"', '')
        hair_filename = request.POST.get('hair').split('/')[1].replace('\"', '')
        face_img1 = request.FILES.get('face1')
        if 'face2' in request.FILES:
            face_img2 = request.FILES.get('face2')
        if 'face3' in request.FILES:
            face_img3 = request.FILES.get('face3')

        print(f'uid: {user_id}, hair: {hair_filename}')
        print(request.FILES)

        ''' Save hair and face images '''
        currtime = str(datetime.datetime.now()).split('.')[0].replace(' ', '_').replace(':', '')
        faceDir = 'ori/'
        hairDir = 'hairs/'
        resultDir = 'result/'

        srcFaceDir = settings.MEDIA_ROOT+'/'+faceDir
        srcHairDir = settings.MEDIA_ROOT+'/'+hairDir

        srcFacePath = srcFaceDir+currtime
        srcHairPath = srcHairDir+hair_filename+'.jpg'
        absConvertedPath = settings.MEDIA_ROOT+'/'+resultDir+currtime+'.jpg'
        os.mkdir(srcFacePath)

        print(f'Source face path: {srcFacePath}')
        print(f'Source hair path: {srcHairPath}')

        default_storage.save(srcFacePath+'/'+str(face_img1), ContentFile(face_img1.read()))
        rotation(srcFacePath+'/'+str(face_img1))
        if 'face2' in request.FILES:
            default_storage.save(srcFacePath+'/'+str(face_img2), ContentFile(face_img2.read()))
            rotation(srcFacePath+'/'+str(face_img2))
        if 'face3' in request.FILES:
            default_storage.save(srcFacePath+'/'+str(face_img3), ContentFile(face_img3.read()))
            rotation(srcFacePath+'/'+str(face_img3))

        ''' Save request data to DB '''
        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()

        # Calculate index
        cur.execute(f"SELECT idx FROM requests_requestinfo;")
        idx_list = list(map(lambda x: x[0], cur.fetchall()))
        idx = 0
        if len(idx_list) != 0:
            while idx in idx_list:
                idx += 1
        
        # Calculate request id
        cur.execute(f"SELECT rid FROM requests_requestinfo WHERE uid=\'{user_id}\';")
        rid_list = list(map(lambda x: x[0], cur.fetchall()))
        request_id = 0
        if len(rid_list) != 0:
            while request_id in rid_list:
                request_id += 1
        
        progress = 0
        request_data = (idx, user_id, request_id, srcFacePath, srcHairPath, absConvertedPath, progress)

        cur.execute('INSERT INTO requests_requestinfo (idx, uid, rid, facePath, hairPath, convertedPath, progress) VALUES (?, ?, ?, ?, ?, ?, ?);', request_data)
        conn.commit()
        result['request_id'] = request_id
        result['progress'] = 0
        result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)

def update(request, content=None):
    print('Update API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get request information from json '''
        user_id = json.loads(request.body).get('uid')

        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()
        print(f'User ID: {user_id}')

        ''' Find all requests of uid from DB '''
        cur.execute(f"SELECT rid, hairPath, convertedPath, progress FROM requests_requestinfo WHERE uid=\'{user_id}\';")
        # 0: rid, 1: hairPath, 2: convertedPath, 3: Progress
        all_requests = cur.fetchall()

        
        requests_len = len(all_requests) # Number of requests of a user (INT)
        rid_list = list(map(lambda x: x[0], all_requests)) # Request ID list (INT list)
        hair_path_list = list(map(lambda x: x[1], all_requests)) # Hair image path list (String list)
        hair_name_list = list(map(lambda x: x.split('/')[-1].split('.')[0], hair_path_list))
        print(f'all requests: {rid_list}')
        # hair_bitmap_list = [] # Hair bitmap list' (String list)
        
        # ''' Convert hair image to bitmap format'''
        # for hair_path in hair_path_list:
        #     with open(hair_path, mode='rb') as file:
        #         img = file.read()
        #         file.close()
        #     hair_bitmap_list.append(base64.encodebytes(img).decode("utf-8"))

        progress_list = list(map(lambda x: x[3] if x[3] < 1 else x[3]-1, all_requests)) # Progress list (INT list)

        print(f'len: {requests_len}')
        ''' Put data into Json '''
        result['len'] = requests_len
        result['rids'] = rid_list
        result['hairs'] = hair_name_list
        result['progresses'] = progress_list
        result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)

def cancel(request):
    print('Cancel API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get request information from json '''
        user_id = json.loads(request.body).get('uid')
        request_id = json.loads(request.body).get('rid')

        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()

        ''' Find request to cancel '''
        cur.execute(f"SELECT uid, rid FROM requests_requestinfo WHERE uid=\'{user_id}\' and rid={request_id};")
        requests = cur.fetchall()

        if len(requests) == 1:
            ''' Delete request '''
            uid, rid = requests[0]
            print(f'uid: {uid}, rid: {rid}')
            cur.execute(f'DELETE FROM requests_requestinfo WHERE uid=\'{uid}\' and rid={rid};')
            conn.commit()
            result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)

def download(request):
    print('Download API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get request information from json '''
        user_id = json.loads(request.body).get('uid')
        request_id = json.loads(request.body).get('rid')

        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()

        ''' Find request to cancel '''
        cur.execute(f"SELECT idx, uid, rid, facePath, hairPath, convertedPath, progress FROM requests_requestinfo WHERE uid=\'{user_id}\' and rid={request_id};")
        requests = cur.fetchall()
    
        if len(requests) == 1:
            ''' Update request '''
            idx, uid, rid, facePath, hairPath, convertedPath, progress = requests[0]
            if progress > 3: # if done
                cur.execute(f'UPDATE requests_requestinfo SET progress=5  WHERE idx={idx};')
                conn.commit()
                print(f'converted: {convertedPath}')
                with open(convertedPath, mode='rb') as file:
                    img = file.read()
                    file.close()

                result['result'] = base64.encodebytes(img).decode("utf-8")
                result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)

def rotation(path):
    img = Image.open(path)
    rotated = img.rotate(180)
    img.save(path)
    return path 