import genanki
from typing import List

styling="""

.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

.big {
 height: 180px;
 filter: invert(100%);
}

.small {
 height: 20px;
 filter: invert(100%);
}

.kanji {
 font-family: "Hiragino Kaku Gothic Pro W3";
 font-size:180px;
 color: white;
 background-color:#0a9ce6;
}

.hiragana {
 font-family: "Hiragino Kaku Gothic Pro W3";
 font-size: 25 px;
}

.text {
 font-family: "Ubuntu Light", "HelveticaNeueLT Std Lt";
 font-style: "italics";
}

.radicon {
 color:white;
 font-size:180px;
}

.quest{
 background: #e9e9e9; 
 color: #555;
 line-height: 40px;
}

"""

radical_backside="""
<div class="kanji">{{word}}{{image}}</div>

<div class="quest"><b>Radical</b></div>
"""

radical_frontside="""
{{FrontSide}}

<br>
<span class="text"><u><b>Meaning</b></u></span><br><br>

<font size="50px"><span class="text"><font color="#0a9ce6">{{meanings}}</font></span></font>
<br><br>
<span class="text"><u><b>Mnemonic</b></u></span><br><br>
<span class="text">{{meaning_mnemonic}}</span>
"""

kanji_backside="""
<div class="kanji">{{word}}</div>

<div class="quest"><b>Kanji</b></div>
"""

kanji_frontside="""
{{FrontSide}}

<br>
<span class="text"><u><b>Meaning</b></u></span><br><br>
<font size="50px"><span class="text"><font color="#0a9ce6">{{meanings}}</font></span></font>

<span class="text"><u><b>On'yomi</b></u></span><br><br>
<font size="50px"><span class="text"><font color="#0a9ce6">{{readings_on}}</font></span></font>

<span class="text"><u><b>Kun'yomi</b></u></span><br><br>
<font size="50px"><span class="text"><font color="#0a9ce6">{{readings_kun}}</font></span></font>

<span class="text"><b>Radicals:</b></span> <font color="#0a9ce6"><span class="hiragana"><b>{{radicals}}</b></span></font>&nbsp;<span class="text">({{radicals_names}})</span>
<span class="text"><b>simmilar looking Kanji:</b></span> <font color="#0a9ce6"><span class="hiragana"><b>{{simmilar_kanji}}</b></span></font>&nbsp;<span class="text">({{simmilar_kanji_names}})</span>

<span class="text"><u><b>Meaning Mnemonic</b></u></span><br><br>
<span class="text"><font color="#0a9ce6">{{meaning_mnemonic}}</font></span>
<br>
<span class="text"><font color="#0a9ce6">{{meaning_hint}}</font></span>

<span class="text"><u><b>Reading Mnemonic</b></u></span><br><br>
<span class="text"><font color="#0a9ce6">{{reading_mnemonic}}</font></span>
<br>
<span class="text"><font color="#0a9ce6">{{reading_hint}}</font></span>

"""

class GenkiNoteRadical(genanki.Note):
  @property
  def guid(self):
      return genanki.guid_for(self.fields[3]) # uid

class GenkiNoteKanji(genanki.Note):
  @property
  def guid(self):
      return genanki.guid_for(self.fields[12]) # uid

def gen_kanji_deck(deck, deckpath: str, model: genanki.Model, uuid:int) -> genanki.Deck:
  full_name = f'{deckpath}'
  anki_deck = genanki.Deck(uuid, full_name)
  for c in deck:
    note = GenkiNoteKanji(
          model=model,
          fields=[
              ", ".join(c['meanings']),
              c['word'], 
              ", ".join(c['readings_on']),
              ", ".join(c['readings_kun']),
              c['meaning_mnemonic'],
              c['meaning_hint'],
              c['reading_mnemonic'],
              c['reading_hint'],
              c['radicals'],
              c['radicals_names'],
              c['simmilar_kanji'],
              c['simmilar_kanji_names'],
              f'{full_name}::{", ".join(c["meanings"])}', 
          ],
          )
    anki_deck.add_note(note)
  return anki_deck

def gen_radical_deck(deck, deckpath: str, model: genanki.Model, uuid:int) -> genanki.Deck:
  full_name = f'{deckpath}'
  anki_deck = genanki.Deck(uuid, full_name)
  for c in deck:
    note = GenkiNoteRadical(
          model=model,
          fields=[
              ", ".join(c['meanings']),
              c['word'] if c['word'] is not None else "<img src=\"{c['image_filename'] if c['image_filename'] is not None else ''}\">",
              c['meaning_mnemonic'],
              f'{full_name}::{", ".join(c["meanings"])}', 
          ],
          )
    anki_deck.add_note(note)
  return anki_deck

def export_to_anki(decks: List, images: List):
  anki_model_radicals = genanki.Model(
      1561628560,
      'Genkikani Model',
      fields=[
          {'name': 'meanings'},
          {'name': 'word'},
          {'name': 'meaning_mnemonic'},
          {'name': 'uuid'},
      ],
      templates=[
          {
          'name': 'Recognition',
          'qfmt': radical_backside,
          'afmt': radical_frontside,
          },
      ],
      css=styling
      )
  anki_model_kanjis = genanki.Model(
      1561628561,
      'Genkikani Model',
      fields=[
          {'name': 'meanings'},
          {'name': 'word'},
          {'name': 'readings_on'},
          {'name': 'readings_kun'},
          {'name': 'meaning_mnemonic'},
          {'name': 'meaning_hint'},
          {'name': 'reading_mnemonic'},
          {'name': 'reading_hint'},
          {'name': 'radicals'},
          {'name': 'radicals_names'},
          {'name': 'simmilar_kanji'},
          {'name': 'simmilar_kanji_names'},
          {'name': 'uuid'},
      ],
      templates=[
          {
          'name': 'Recognition',
          'qfmt': kanji_backside,
          'afmt': kanji_frontside,
          },
      ],
      css=styling
      )
  anki_decks = []
  sound_files = []
  start_uuid = 284760580
  image_files = images
  deck_name = "Genkikani"
  for i,lection in enumerate(decks):

    # radicals
    radical_deck = gen_radical_deck(lection['radicals'], f'{deck_name}::{lection["name"]}::0 Radicals', anki_model_radicals, start_uuid + i*10)
    anki_decks.append(radical_deck)

    # kanjis
    kanji_deck = gen_kanji_deck(lection['kanjis'], f'{deck_name}::{lection["name"]}::1 Kanjis', anki_model_kanjis, start_uuid + i*10 + 1)
    anki_decks.append(kanji_deck)

  
  anki_package = genanki.Package(anki_decks)

  media_files = [f'data/wanikani/images/{image}' for image in image_files]
  anki_package.media_files = media_files

  anki_package.write_to_file('wanigenki.apkg')
