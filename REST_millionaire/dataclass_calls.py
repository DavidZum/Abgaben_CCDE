import requests

host = 'http://localhost:5000/millionaire'

# print('Speichere einen Eintrag am Server:')
# response = requests.put('%s/%d' % (host, 1000), json={'level' : 0, 'frage' : 'Was ist das?', 'antworten' : ['Keine Ahnung', 'ich weiß es nicht', 'Frag jemand anderen', '...'], 'richtig': 3}).json()
# print (response)

# print('---------------------------')
# print('Hole diesen Eintrag wieder:')
# response = requests.get('%s/%d' % (host, 1000)).json()
# print (response)


# print('---------------------------')
# print('Löschen eines Eintrags')
# response = requests.delete('%s/%d' % (host, 1000)).json()
# print(response)

# print('---------------------------')
# print('Hole diesen Eintrag wieder:')
# response = requests.get('%s/%d' % (host, 1000)).json()
# print (response)

# response = requests.patch('%s/%s' % (host, 1),  json={'level' : 3}).json()
# print (response)

# print('---------------------------')
# print('Hole diesen Eintrag wieder:')
# response = requests.get('%s/%d' % (host, 1)).json()
# print (response)

response = requests.get(host + '/random_question')
print(response.json())
