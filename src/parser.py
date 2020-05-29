import re
import json
import requests

cards = []

# Fetch the card set from SteamDatabase
card_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-Artifact-Beta/master/game/dcg/resource/card_set_01_english.txt'
r = requests.get(card_url).text

reg = r'"CardName_(\d+)"\s*"(.*)"'
entries = [re.match(reg, l.strip()) for l in r.splitlines()]

# If it's a card entry, extract its name and ID
cards = [entry.groups() for entry in entries if entry]

with open('../cards.json', 'w+') as f:
    card_dict = { 'card_set': { 'version': 1, 'card_list': [] } }
    
    card_dict['card_set']['card_list'] = [{
        'card_id': card[0], 'card_name': { 'english': card[1] }
    } for card in cards]
    
    f.write(json.dumps(card_dict, indent=4))
    