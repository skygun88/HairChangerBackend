import sqlite3
import time
import os
import threading

def createDeepfakeImage(target, curr_requests):
    iters = 100000
    ''' idx, facePath, hairPath, coonvertedPath, iteration '''
    # print(f'python runFaceSwap.py {target[0]} {target[3]} {target[4]} {target[5]} {iters}')
    os.system(f'python runFaceSwap.py {str(target[0])} {target[3]} {target[4]} {target[5]} {str(iters)}')
    curr_requests.pop()
    print('Done ---')
    return True

if __name__ == '__main__':
    max_request = 0
    curr_requests = []
    conn = sqlite3.connect("/home/ubuntu/backend/repo/db.sqlite3")
    cur = conn.cursor()
    while True:
        ''' if running deepfake is more than two, skip the loop '''
        if len(curr_requests) > max_request:
            print('request queue is full')
            time.sleep(30)
            continue

        ''' Get all requests from DB '''
        cur.execute(f"SELECT idx, uid, rid, facePath, hairPath, convertedPath, progress  FROM requests_requestinfo;")
        rows = cur.fetchall()

        print(f'All requests: \n{list(map(lambda x: (x[1], x[2], x[3], x[-1]), rows))}')
        target = None

        ''' Find the request which is not yet started '''
        for i in range(len(rows)):
            if rows[i][6] == 0:
                target = rows[i]
                break

        ''' Run the deepfake processing thread '''
        if target != None:
            print('start deepfake')
            curr_requests.append(0)
            print(target)
            cur.execute(f'UPDATE requests_requestinfo SET progress=1  WHERE uid=\'{target[1]}\' and rid={target[2]};')
            conn.commit()
            t1 = threading.Thread(target=createDeepfakeImage, args=(target[:],curr_requests,))
            t1.start()
            # iters = 50000
            # os.system(f'python runFaceSwap.py {str(target[0])} {target[3]} {target[4]} {target[5]} {str(iters)}')

        print('loop fin')
        time.sleep(30)





