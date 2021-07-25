import json
from typing import Dict, List
import urllib.request
import jaconv
from ruamel.yaml import YAML
import os

yaml=YAML()


def request(action, **params):
    # requires python 3.7 for order
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def extract_readings(reading) -> List[Dict[str, str]]:
    s = reading.split('；')
    readings = []
    for reading in s:
        important = False
        if '#aa0000' in reading:
            important = True
        clean_reading = "".join(filter(lambda c: not c.isascii(), reading))
        hiragana = jaconv.kata2hira(clean_reading)
        readings.append({
            'reading': hiragana,
            'important': important
        })
    return readings


if __name__ == "__main__":
    for i in range(3, 13):
        card_ids = invoke('findNotes', query=f'deck:Genki_I::L{i}_Kanji')
        cards = invoke('notesInfo', notes=card_ids)
        kanjis = []
        vocabs = []
        for c in cards:
            kanji_note = {}
            fields = c['fields']
            kanji = fields['Kanji']['value']
            meaning = fields['Bedeutung']['value']
            onyomi = extract_readings(fields['Onyomi']['value'])
            kunyomi = extract_readings(fields['Kunyomi']['value'])
            kanjis.append({
                'kanji': kanji,
                'meaning': meaning,
                'onyomi': onyomi,
                'kunyomi': kunyomi,
            })

        folder_path = 'data/genki'
        os.makedirs(folder_path, exist_ok=True)

        
        with open(f'{folder_path}/kanjis_{str(i).zfill(2)}.yaml', 'w+') as o:
            yaml.dump(kanjis, o)



