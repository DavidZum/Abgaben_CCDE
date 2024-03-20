import requests
host = "http://127.0.0.1:5000/millionaire/question"


response = requests.get('%s/%d' % (host, 100)).json()
print(response)