import sqlite3

conn = sqlite3.connect('/home/ubuntu/backend/repo/db.sqlite3')
cur = conn.cursor()

# cur.execute("SELECT * FROM user_userinfo;")
# rows = cur.fetchall()
# rows = list(map(lambda x: (x[0], x[1]), rows))
# print(rows)

# cur.execute("SELECT * FROM login_logininfo;")
# rows = cur.fetchall()
# print(rows)

# if ('testid', 'password') in rows:
#     print('found id')
# else:
#     print('not found')

# idx = 0
# user_id = 'asdf'
# request_id = 1
# srcFacePath = 'qwe'
# srcHairPath = 'zcxv'
# absConvertedDir = 'qcvdg'
# print(type(idx))
# request_data = (idx, user_id, request_id, srcFacePath, srcHairPath, absConvertedDir, 0)
# cur.execute('INSERT INTO requests_requestinfo (idx, uid, rid, facePath, hairPath, convertedPath, progress) VALUES (?, ?, ?, ?, ?, ?, ?);', request_data)
# conn.commit()

# cur.execute(f"SELECT * FROM requests_requestinfo;")
# rows = cur.fetchall()
# print(rows)