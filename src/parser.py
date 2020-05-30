import re
import json
import requests

CARD_SET_URL = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-Artifact-Beta/master/game/dcg/resource/card_set_01_english.txt'
ITEMS_GAME_URL = 'https://raw.githubusercontent.com/SteamDatabase/GameTracking-Artifact-Beta/master/game/dcg/pak01_dir/scripts/items/items_game.txt'

def get_card(card_dict, identifier):
    card_list = card_dict['card_set']['card_list']
    
    try: 
        int(identifier)
        return [card for card in card_list if card['card_id'] == identifier][0]
    
    except ValueError:
        return [card for card in card_list if card['card_name']['english'] == identifier][0]

def remove_attr_syntax(s): 
    m = re.findall(r'(?<=\[)([^\[\]]+)(?=\[)', s)

    for token in m:
        s = s.replace(token, '')

    return re.sub('[\[\]]', '', s)

def fetch_file_from_steamdb(url):
    return requests.get(url).text

# Parse 'game/dcg/resource/card_set_01_english.txt'
def parse_card_set_file(raw_f):
    reg = r'"Card(?:Name|Text)_(\d+)"\s*"(.*)"'
    entries = [re.match(reg, l.strip()) for l in raw_f.splitlines()]

    # If it's a card entry, extract its name, ID and text
    entries = [entry.groups() for entry in entries if entry]
    cards = [[entries[i][0], entries[i][1], entries[i+1][1]] for i in range(0, len(entries), 2)]

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

            # Add <br> to ability
            repl = parent_card['card_text']['english'].replace(ability, f'{ability}<br>')
            parent_card['card_text']['english'] = repl

            parent_card['references'].append(child_card['card_id'])

    
    for card in card_dict['card_set']['card_list']:
        # Add remaining {s:parentCardName} (possibly unreleased or unfinished cards)

        translations = {
            r'{s:parentCardName}': card['card_name']['english'],
            r'\s?&#9632;\s?': '',
            r'\s?&#9633;\s?': '',
            r'\s?&#9634;\s?': '',
            r'\s?&#9635;\s?': ' Attack ',
            r'\s?&#9636;\s?': ' Armor ',
            r'\s?&#9637;\s?': ' Health ',
            r'<BR/>\\n<BR/>\\n': '<br><br><br><br>'
        }

        for tk, tv in translations.items():
            repl = re.sub(tk, tv, card['card_text']['english'])
            card['card_text']['english'] = repl

    return card_dict

# Parse 'game/dcg/pak01_dir/scripts/items/items_game.txt'
def parse_items_game_file(raw_f, card_dict):
    entries = [re.sub(r"[\n\t\s]*", '', l) for l in raw_f.splitlines()]
    entries = [l for l in entries if 'altArtworkID0' not in l]  # Remove two lines messing the indexing
    
    for card in card_dict['card_set']['card_list']:
        idx = [entries.index(e) for e in entries if f'1{card["card_id"]}' in e]

        if len(idx) == 0:
            continue

        CARD_RARITY_IDX = idx[0] + 3
        CARD_TYPE_IDX = idx[0] + 11

        card['rarity'] = re.findall(r'card_(\w+)', entries[CARD_RARITY_IDX])[0].capitalize()
        card['card_type'] = re.findall(r'card_type\"\"(\w+)', entries[CARD_TYPE_IDX])[0]

csf = fetch_file_from_steamdb(CARD_SET_URL)
card_dict = parse_card_set_file(csf)

csf = fetch_file_from_steamdb(ITEMS_GAME_URL)
parse_items_game_file(csf, card_dict)

with open('../cards.json', 'w+') as f:
    f.write(json.dumps(card_dict, indent=4))
    