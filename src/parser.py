import re
import json
import requests

# Fetch the card set from SteamDatabase
card_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-Artifact-Beta/master/game/dcg/resource/card_set_01_english.txt'
r = requests.get(card_url).text

reg = r'"Card(?:Name|Text)_(\d+)"\s*"(.*)"'
entries = [re.match(reg, l.strip()) for l in r.splitlines()]

# If it's a card entry, extract its name, ID and text
entries = [entry.groups() for entry in entries if entry]
cards = [[entries[i][0], entries[i][1], entries[i+1][1]] for i in range(0, len(entries), 2)]

# Clean card text to readable format
for card in cards:
    card[2] = card[2].replace('{s:thisCardName}', card[1])
    card[2] = re.sub(r'&#\d+;', '', card[2])
    card[2] = card[2].replace('\\n', '')

with open('../cards.json', 'w+') as f:
    card_dict = { 'card_set': { 'version': 1, 'card_list': [] } }
    
    card_dict['card_set']['card_list'] = [{
        'card_id': card[0], 'card_name': { 'english': card[1] }, 'card_text': { 'english': card[2] }
    } for card in cards]
    
    f.write(json.dumps(card_dict, indent=4))
    