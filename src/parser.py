import re
import json
import requests

def remove_attr_syntax(s): 
    m = re.findall(r'(?<=\[)([^\[\]]+)(?=\[)', s)

    for token in m:
        s = s.replace(token, '')

    return re.sub('[\[\]]', '', s)

# Fetch the card set from SteamDatabase
card_url = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-Artifact-Beta/master/game/dcg/resource/card_set_01_english.txt'
r = requests.get(card_url).text

reg = r'"Card(?:Name|Text)_(\d+)"\s*"(.*)"'
entries = [re.match(reg, l.strip()) for l in r.splitlines()]

# If it's a card entry, extract its name, ID and text
entries = [entry.groups() for entry in entries if entry]
cards = [[entries[i][0], entries[i][1], entries[i+1][1]] for i in range(0, len(entries), 2)]

def get_card(card_dict, identifier):
    card_list = card_dict['card_set']['card_list']
    
    try: 
        int(identifier)
        return [card for card in card_list if card['card_id'] == identifier][0]
    
    except ValueError:
        return [card for card in card_list if card['card_name']['english'] == identifier][0]


with open('../cards.json', 'w+') as f:
    card_dict = { 'card_set': { 'version': 1, 'card_list': [] } }
    
    # Clean card text to readable format
    for card in cards:
        card[2] = card[2].replace('{s:thisCardName}', card[1])
        card_text = remove_attr_syntax(card[2])

        card_info = {
            'card_id': card[0],
            'card_name': { 'english': card[1] },
            'card_text': { 'english': card_text },
            'references': []
        }

        card_dict['card_set']['card_list'].append(card_info)

    # Add reference to ability cards
    for card in cards:
        for ability in re.findall('\[abilityname\[([^\[\]]+)\]\]', card[2]):
            
            parent_card = get_card(card_dict, card[1])
            child_card = get_card(card_dict, ability)

            # Replace possible {s:parentCardName} references by parent name
            repl = child_card['card_text']['english'].replace('{s:parentCardName}', parent_card['card_name']['english'])
            child_card['card_text']['english'] = repl

            parent_card['references'].append(child_card['card_id'])

    # Add remaining {s:parentCardName} (possibly unreleased or unfinished cards)
    for card in card_dict['card_set']['card_list']:
        repl = card['card_text']['english'].replace('{s:parentCardName}', card['card_name']['english'])
        card['card_text']['english'] = repl
                
    f.write(json.dumps(card_dict, indent=4))
    