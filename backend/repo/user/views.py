from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.
def upgrade(request):
    print('Upgrade API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get ID & Password data from POST request'''
        user_id = json.loads(request.body).get('uid')
    conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
    cur = conn.cursor()
    cur.execute(f'SELECT usertype FROM user_userinfo WHERE uid=\'{user_id}\';')
    rows = cur.fetchall()
    if len(rows) == 0:
        user_info = rows[0]
        if user_info[0] == 0:
            cur.execute(f'UPDATE user_userinfo SET usertype=1  WHERE uid=\'{user_id}\';')
            conn.commit()
            result['status'] = 'OK'
        else:
            print('This user is already Premium user.')
            result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)


def downgrade(request):
    print('Upgrade API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get ID & Password data from POST request'''
        user_id = json.loads(request.body).get('uid')
    conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
    cur = conn.cursor()
    cur.execute(f'SELECT usertype FROM user_userinfo WHERE uid=\'{user_id}\';')
    rows = cur.fetchall()
    if len(rows) == 0:
        user_info = rows[0]
        if user_info[0] == 1:
            cur.execute(f'UPDATE user_userinfo SET usertype=0  WHERE uid=\'{user_id}\';')
            conn.commit()
            result['status'] = 'OK'
        else:
            print('This user is already Normal user.')
            result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)


def setProfile(request, content=None):
    print('Set profile API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get request information from FILES '''
        user_id = request.POST.get('uid')
        profile = request.FILES.get('profile')
        print(f'uid: {user_id}, profile: {profile}')

        ''' Save profile image file '''
        profileDir = 'profile/'
        absProfileDir = settings.MEDIA_ROOT+'/'+profileDir
        absProfilePath = absProfileDir + user_id + '.jpg'
        default_storage.save(absProfilePath, ContentFile(profile.read()))
        print(f'Profile img path: {absProfilePath}')

        ''' Save profile path to DB '''
        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()

        # Calculate index
        cur.execute(f"SELECT profile_image FROM user_userinfo WHERE uid=\'{user_id}\';")
        rows = cur.fetchall()
        previous_profile = rows[0]
        if previous_profile == None:
            cur.execute(f'UPDATE user_userinfo SET profile_image=\'{absProfilePath}\' WHERE uid=\'{user_id}\';')
            conn.commit()

        result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)

def resetProfile(request, content=None):
    print('Set profile API executed')
    result = {'status': 'FAIL'}
    if request.method == 'POST':
        ''' Get request information from FILES '''
        user_id = json.loads(request.body).get('uid')
        print(f'uid: {user_id}')

        ''' Find profile image on local directory '''
        profileDir = 'profile/'
        absProfileDir = settings.MEDIA_ROOT+'/'+profileDir
        absProfilePath = absProfileDir + user_id + '.jpg'
        if os.path.isfile(absProfilePath):
            os.remove(absProfilePath)
        print(f'Removed the profile')

        ''' remove profile path from DB '''
        conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
        cur = conn.cursor()

        cur.execute(f"SELECT profile_image FROM user_userinfo WHERE uid=\'{user_id}\';")
        rows = cur.fetchall()
        previous_profile = rows[0]
        if previous_profile != None:
            cur.execute(f'UPDATE user_userinfo SET profile_image=null WHERE uid=\'{user_id}\';')
            conn.commit()

        result['status'] = 'OK'

    conn.close()
    return JsonResponse(result)
