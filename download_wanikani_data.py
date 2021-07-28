from wanikani_api.client import Client, models
import json
from ruamel.yaml import YAML
import os
import requests
import sys

def select_audio(audios, audio_type):
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

def get_entries_from_data(data):
    return [item for page in data.pages for item in page._raw['data']]


yaml=YAML()

assert len(sys.argv) == 2 # needs wanikani api key
v2_api_key = sys.argv[1]
client = Client(v2_api_key)

folder_path = 'data/wanikani/sound'
os.makedirs(folder_path, exist_ok=True)
os.makedirs('data/wanikani/images', exist_ok=True)


vocabulary = client.subjects(types="vocabulary", fetch_all=True)
kanjis = client.subjects(types="kanji", fetch_all=True)
radicals = client.subjects(types="radical", fetch_all=True)

flat_vocab = get_entries_from_data(vocabulary)
#in_dict = vocabulary.current_page._raw
vocab_dict = {}
for e in flat_vocab:
    _id = e['id']
    data = e['data']
    word = data['characters']
    meanings = [m['meaning'] for m in data['meanings']]
    readings = [m['reading'] for m in data['readings']]
    components = data['component_subject_ids']
    meaning_mnemonic = data['meaning_mnemonic']
    reading_mnemonic = data['reading_mnemonic']
    audio_url_female = select_audio(data['pronunciation_audios'], 'female')
    audio_filename_female = get_filename(audio_url_female) if audio_url_female is not None else None
    if audio_filename_female is not None:
        audio = requests.get(audio_url_female)
        with open(f'data/wanikani/sound/{audio_filename_female}', 'wb') as o:
            o.write(audio.content)
    audio_url_male = select_audio(data['pronunciation_audios'], 'male')
    audio_filename_male = get_filename(audio_url_male) if audio_url_male is not None else None
    if audio_filename_male is not None:
        audio = requests.get(audio_url_male)
        with open(f'data/wanikani/sound/{audio_filename_male}', 'wb') as o:
            o.write(audio.content)
    vocab_dict[_id] = {
        'word': word,
        'meanings': meanings,
        'readings': readings,
        'components': components,
        'meaning_mnemonic': meaning_mnemonic,
        'reading_mnemonic': reading_mnemonic,
        'sound_male': audio_filename_male,
        'sound_female': audio_filename_female
    }

with open('data/wanikani/vocabulary.yaml', 'w+') as o:
    yaml.dump(vocab_dict, o)

flat_vocab = get_entries_from_data(kanjis)

#in_dict = kanjis.current_page._raw
kanji_dict = {}
for e in flat_vocab:
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

flat_vocab = get_entries_from_data(radicals)
#in_dict = radicals.current_page._raw
radical_dict = {}
for e in flat_vocab:
    _id = e['id']
    data = e['data']
    word = data['characters']
    meanings = [m['meaning'] for m in data['meanings']]
    meaning_mnemonic = data['meaning_mnemonic']
    image_filename = None
    if word is None:
        image_url = [e['url'] for e in data['character_images'] if e['content_type'] == 'image/png' and e['metadata']['dimensions'] == '1024x1024'][0]
        image_filename = get_filename(image_url) if image_url is not None else None
        image = requests.get(image_url)
        with open(f'data/wanikani/images/{image_filename}', 'wb') as o:
            o.write(image.content)
    radical_dict[_id] = {
        'word': word,
        'meanings': meanings,
        'meaning_mnemonic': meaning_mnemonic,
        'image_filename': image_filename,
    }

with open('data/wanikani/radicals.yaml', 'w+') as o:
    yaml.dump(radical_dict, o)
