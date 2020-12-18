import requests

data = {'id': 'test_id1', 'password': 'test123', 'user_name': 'team1', 'user_type': '0'}
URL = 'http://127.0.0.1:80/'
api = 'login/register/'
res = requests.post(URL+api, data=data)
print(res.text)

data = {'id': 'test_id1', 'password': 'test123'}
URL = 'http://127.0.0.1:80/'
api = 'login/login/'
res = requests.post(URL+api, data=data)
print(res.text)