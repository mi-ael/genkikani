from ruamel.yaml import YAML
from typing import List
from pathlib import Path
from src.anki_exporter import export_to_anki



yaml=YAML()
kanjis = yaml.load(Path('data/wanikani/kanjis.yaml'))
radicals = yaml.load(Path('data/wanikani/radicals.yaml'))

def unique(l):
    # requires python 3.7 for order
    return list(dict.fromkeys(l))

def kanji_to_id(kanji:str)->int:
    first = next(k for k,v in kanjis.items() if v['word'] == kanji)
    assert first is not None
    return first

def get_radicals_for_kanji(kanji:int) -> List[int]:
  kanji_data = kanjis[kanji]
  return kanji_data['components']

def mark_important(kanas:str) -> str:
  return f'<span stile="background-color: rgba(255, 0, 0, 0.3);">{kanas}</span>'

def main():
  genki_dir = Path('data/genki/')
  already_included_radicals = []
  lections = []
  for f in sorted(genki_dir.iterdir()):
    lection_data = yaml.load(f)
    lection_kanjis = [k['kanji'] for k in lection_data]
    lection_kanji_ids = [kanji_to_id(k) for k in lection_kanjis]
    required_radicals = unique([radical for kanji in lection_kanji_ids for radical in get_radicals_for_kanji(kanji)])
    required_radicals = [x for x in required_radicals if x not in already_included_radicals]
    already_included_radicals.extend(required_radicals)

    genkikani_radicals = []
    for rad_id in required_radicals:
      rad_data = radicals[rad_id]
      genkikani_radicals.append(rad_data)

    genkikani_kanjis = []
    for kanji_id, genki_data in zip(lection_kanji_ids, lection_data):
      kanji_data = kanjis[kanji_id]
      important_onyomi = [reading['reading'] for reading in genki_data['onyomi'] if reading['important'] == True]
      important_kunyomi = [reading['reading'] for reading in genki_data['kunyomi'] if reading['important'] == True]
      kanji_data['readings_on'] = [reading if reading not in important_onyomi else mark_important(reading) for reading in kanji_data['readings_on']]
      kanji_data['readings_kun'] = [reading if reading not in important_kunyomi else mark_important(reading) for reading in kanji_data['readings_on']]
      genkikani_kanjis.append(kanji_data)
    lections.append({
      'name': f,
      'radicals': genkikani_radicals,
      'kanjis': genkikani_kanjis,
    })

  # generate actual Decks
  export_to_anki(lections)


      




if __name__ == "__main__":
  main()
