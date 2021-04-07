from wanikani_api.client import Client, models
import json
from ruamel.yaml import YAML
import os
import requests
import sys

audio_type = 'male' # or female

def select_audio(audios):
    if len(audios) == 0:
        return None
    if len(audios) == 1:
        return audios[0]['url']
    audios_2 = list(filter(lambda x: x['content_type'] == 'audio/ogg', audios))
    if len(audios_2) == 1:
        return audios_2[0]['url']
    audios_3 = list(filter(lambda x: x['metadata']['gender'] == audio_type, audios_2))
    if len(audios_3) == 0:
        return audios_2[0]['url']
    return audios_3[0]['url']

def get_filename(url):
    fragment_removed = url.split("#")[0]  # keep to left of first #
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return os.path.basename(scheme_removed)



yaml=YAML()

assert len(sys.argv) == 2 # needs wanikani api key
v2_api_key = sys.argv[1]
client = Client(v2_api_key)

folder_path = 'data/wanikani/sound'
os.makedirs(folder_path, exist_ok=True)

vocabulary = client.subjects(types="vocabulary", fetch_all=True)
kanjis = client.subjects(types="kanji", fetch_all=True)
radicals = client.subjects(types="radical", fetch_all=True)

in_dict = vocabulary.current_page._raw
vocab_dict = {}
for e in in_dict['data']:
    _id = e['id']
    data = e['data']
    word = data['characters']
    meanings = [m['meaning'] for m in data['meanings']]
    readings = [m['reading'] for m in data['readings']]
    components = data['component_subject_ids']
    meaning_mnemonic = data['meaning_mnemonic']
    reading_mnemonic = data['reading_mnemonic']
    audio_url = select_audio(data['pronunciation_audios'])
    audio_filename = get_filename(audio_url) if audio_url is not None else None
    if audio_filename is not None:
        audio = requests.get(audio_url)
        with open(f'data/wanikani/sound/{audio_filename}', 'wb') as o:
            o.write(audio.content)
    vocab_dict[_id] = {
        'word': word,
        'meanings': meanings,
        'readings': readings,
        'components': components,
        'meaning_mnemonic': meaning_mnemonic,
        'reading_mnemonic': reading_mnemonic,
        'sound': audio_filename
    }

with open('data/wanikani/vocabulary.yaml', 'w+') as o:
    yaml.dump(vocab_dict, o)

in_dict = kanjis.current_page._raw
kanji_dict = {}
for e in in_dict['data']:
    _id = e['id']
    data = e['data']
    word = data['characters']
    meanings = [m['meaning'] for m in data['meanings']]
    readings_on = [m['reading'] for m in data['readings'] if m['type'] == 'onyomi']
    readings_kun = [m['reading'] for m in data['readings'] if m['type'] == 'kunyomi']
    components = data['component_subject_ids']
    simmilar = data['visually_similar_subject_ids']    
    meaning_mnemonic = data['meaning_mnemonic']
    meaning_hint = data['meaning_hint']
    reading_mnemonic = data['reading_mnemonic']
    reading_hint = data['reading_hint']
    kanji_dict[_id] = {
        'word': word,
        'meanings': meanings,
        'readings_on': readings_on,
        'readings_kun': readings_kun,
        'components': components,
        'simmilar': simmilar,
        'meaning_mnemonic': meaning_mnemonic,
        'meaning_hint': meaning_hint,
        'reading_mnemonic': reading_mnemonic,
        'reading_hint': reading_hint,
    }

with open('data/wanikani/kanjis.yaml', 'w+') as o:
    yaml.dump(kanji_dict, o)

in_dict = radicals.current_page._raw
radical_dict = {}
for e in in_dict['data']:
    _id = e['id']
    data = e['data']
    word = data['characters']
    meanings = [m['meaning'] for m in data['meanings']]
    radical_dict[_id] = {
        'word': word,
        'meanings': meanings,
    }

with open('data/wanikani/radicals.yaml', 'w+') as o:
    yaml.dump(radical_dict, o)
