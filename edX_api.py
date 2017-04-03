import requests, json, pickle
from requests.auth import HTTPBasicAuth

import requests # pip install requests

url = 'https://api.edx.org/oauth2/v1/access_token'
r = requests.post(url, dict(
	'grant_type=client_credentials',
	'client_id=14TIRydxjYn2TTzKBjo1PHddKtClV3DEOeWnZCBL',
	'client_secret=XiqlqBFgCwpj6WajRndn3A2hX77nzq6pd1ujkmtwuM6ixzQcsaNoXdk7cDyNteKrVpoauXs9WBvsEHkMgomfknW1YPuJtExRYOKdOtvG3LY6fjwaHxi5v0AuFX5AQusW',
	'token_type=jwt'))

print(r.headers)
print(r.text) # or r.json()

"""def make_response(url):
	response = requests.get(url, auth=requests.auth.HTTPBasicAuth('14TIRydxjYn2TTzKBjo1PHddKtClV3DEOeWnZCBL','XiqlqBFgCwpj6WajRndn3A2hX77nzq6pd1ujkmtwuM6ixzQcsaNoXdk7cDyNteKrVpoauXs9WBvsEHkMgomfknW1YPuJtExRYOKdOtvG3LY6fjwaHxi5v0AuFX5AQusW'))
	json_response = json.loads(response.text)
	return json_response

json_response = make_response('https://api.edx.org/oauth2/v1/access_token')

print(json_response)"""