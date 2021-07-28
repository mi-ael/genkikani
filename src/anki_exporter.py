import genanki
from typing import List

styling="""


@font-face {
  font-family: "Hiragino Kaku Gothic Pro W3";
  src: url("_hirakakyprow3.otf");
}


radical {
  color: #0a9ce6;
}

kanji {
  color: #b8046c;
}

vocabulary {
  color: #a900fd;
}

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

.radical {
 font-family: "Hiragino Kaku Gothic Pro W3";
 font-size:180px;
 color: white;
 background-color:#0a9ce6;
}

.kanji {
 font-family: "Hiragino Kaku Gothic Pro W3";
 font-size:180px;
 color: white;
 background-color:#b8046c;
}

.vocab {
 font-family: "Hiragino Kaku Gothic Pro W3";
 font-size:180px;
 color: white;
 background-color:#a900fd;
}

.hiragana {
 font-family: "Hiragino Kaku Gothic Pro W3";
 font-size: 25 px;
}

.text {
 font-family: "Roboto", "HelveticaNeueLT Std Lt";
 font-style: "italics";
}

.radicon {
 color:white;
 font-size:180px;
}

.quest-radical{
 background: #e9e9e9; 
 color: #555;
 line-height: 40px;
}

.quest-kanji{
 background: #e9e9e9; 
 color: #555;
 line-height: 40px;
}

.quest-vocab{
 background: #e9e9e9; 
 color: #555;
 line-height: 40px;
}

"""

radical_backside="""
<div class="radical">{{word}}</div>

<div class="quest-radical"><b>Radical</b></div>
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

<div class="quest-kanji"><b>Kanji</b></div>
"""

kanji_frontside="""
{{FrontSide}}

<br>
<span class="text"><u><b>Meaning</b></u></span><br>
<font size="50px"><span class="text"><font color="#b8046c">{{meanings}}</font></span></font>
<br>
<br>
<span class="text"><u><b>On'yomi</b></u></span><br>
<font size="50px"><span class="text"><font color="#b8046c">{{readings_on}}</font></span></font>
<br>
<br>
<span class="text"><u><b>Kun'yomi</b></u></span><br>
<font size="50px"><span class="text"><font color="#b8046c">{{readings_kun}}</font></span></font>
<br>
<br>
<span class="text"><b>Radicals:</b></span> <font color="#b8046c"><span class="hiragana"><b>{{radicals}}</b></span></font>&nbsp;<span class="text">({{radicals_names}})</span>
<br>
{{#simmilar_kanji}}
<br>
<span class="text"><b>simmilar looking Kanji:</b></span> <font color="#b8046c"><span class="hiragana"><b>{{simmilar_kanji}}</b></span></font>&nbsp;<span class="text">({{simmilar_kanji_names}})</span>
<br>
{{/simmilar_kanji}}
<br>
<span class="text"><u><b>Meaning Mnemonic</b></u></span><br>
<span class="text">{{meaning_mnemonic}}</span>
<br>
<br>
<span class="text">{{meaning_hint}}</span>
<br>
<br>
<span class="text"><u><b>Reading Mnemonic</b></u></span><br>
<span class="text">{{reading_mnemonic}}</span>
<br>
<br>
<span class="text">{{reading_hint}}</span>

"""


vocab_backside="""
<div class="vocab">{{word}}</div>

<div class="quest-vocab"><b>Vocabulary</b></div>
"""
# TODO: sound does not exist case
vocab_frontside="""
{{FrontSide}}

{{#full_kanji}}
<br>
<span class="text"><u><b>Full Kanji Version</b></u></span><br>
<span class="text">{{full_kanji}}</span>
<br>
{{/full_kanji}}

<br>
<span class="text"><u><b>Meaning</b></u></span><br>
<font size="50px"><span class="text"><font color="#e9e9e9">{{meanings}}</font></span></font>
<br>
<br>
<span class="text"><u><b>On'yomi</b></u></span><br>
<font size="50px"><span class="text"><font color="#e9e9e9">{{readings}}</font></span></font>
<br>
{{#type}}
<br>
<span class="text"><u><b>Type</b></u></span><br>
<span class="text">{{type}}</span>
<br>
{{/type}}
<br>
<span class="text"><b>Kanjis:</b></span> <font color="#e9e9e9"><span class="hiragana"><b>{{kanjis}}</b></span></font>&nbsp;<span class="text">({{kanjis_names}})</span>
<br>
{{#meaning_mnemonic}}
<br>
<span class="text"><u><b>Meaning Mnemonic</b></u></span><br>
<span class="text">{{meaning_mnemonic}}</span>
<br>
{{/meaning_mnemonic}}
{{#reading_mnemonic}}
<br>
<span class="text"><u><b>Reading Mnemonic</b></u></span><br>
<span class="text">{{reading_mnemonic}}</span>
<br>
{{/reading_mnemonic}}
{{#note}}
<br>
<span class="text"><u><b>Note</b></u></span><br>
<span class="text">{{note}}</span>
<br>
{{/note}}
<br>
{{#sentences}}
<br>
<span class="text"><u><b>Sentences</b></u></span><br>
<span class="text">{{sentences}}</span>
<br>
{{/sentences}}
<br>

{{#sound}}
{{sound}}
{{/sound}}
"""

class GenkiNoteRadical(genanki.Note):
  @property
  def guid(self):
      return genanki.guid_for(self.fields[3]) # uid

class GenkiNoteKanji(genanki.Note):
  @property
  def guid(self):
      return genanki.guid_for(self.fields[12]) # uid

class GenkiNoteVocab(genanki.Note):
  @property
  def guid(self):
      return genanki.guid_for(self.fields[12]) # uid

def gen_vocab_deck(deck, deckpath: str, model: genanki.Model, uuid:int, sounds:List[str]) -> genanki.Deck:
  full_name = f'{deckpath}'
  anki_deck = genanki.Deck(uuid, full_name)
  for c in deck:
    note = GenkiNoteVocab(
          model=model,
          fields=[
              ", ".join(c['meanings']),
              c['word'], 
              ", ".join(c['readings']),
              c['meaning_mnemonic'],
              c['reading_mnemonic'],
              c['kanjis'],
              c['kanjis_names'],
              c['type'],
              c['sentences'],
              c['note'] if 'note' in c else '',
              c['full_kanji'] if 'full_kanji' in c else '',
              f"[sound:{c['sound']}]" if c['sound'] != '' else '',
              f'{full_name}::{", ".join(c["meanings"])}', 
          ],
          )
    if c['sound'] != '':
      sounds.append(c['sound'])
    anki_deck.add_note(note)
  return anki_deck


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
              c['word'] if c['word'] is not None else "",
              #c['image_filename'] if c['image_filename'] is not None else '',
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
          #{'name': 'image'},
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
          {'name': 'radicals'},# todo: fix color of wanikani radicals
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
  anki_model_vocabulary = genanki.Model(
      1561628562,
      'Genkikani Model',
      fields=[
          {'name': 'meanings'},
          {'name': 'word'},
          {'name': 'readings'},
          {'name': 'meaning_mnemonic'},
          {'name': 'reading_mnemonic'},
          {'name': 'kanjis'},
          {'name': 'kanjis_names'},
          {'name': 'type'},
          {'name': 'sentences'},
          {'name': 'note'},
          {'name': 'full_kanji'},
          {'name': 'sound'},
          {'name': 'uuid'},
      ],
      templates=[
          {
          'name': 'Recognition',
          'qfmt': vocab_backside,
          'afmt': vocab_frontside,
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

    # vocabulary important
    vocab_deck_important = gen_vocab_deck(lection['vocabulary_important'], f'{deck_name}::{lection["name"]}::2 Vocabulary', anki_model_vocabulary, start_uuid + i*10 + 2, sound_files)
    anki_decks.append(vocab_deck_important)

    # vocabulary wanikani
    vocab_deck_unimportant = gen_vocab_deck(lection['vocabulary_wanikani'], f'{deck_name}::{lection["name"]}::3 Additional Vocabulary', anki_model_vocabulary, start_uuid + i*10 + 3, sound_files)
    anki_decks.append(vocab_deck_unimportant)

    # vocabulary unimportant
    vocab_deck_unimportant = gen_vocab_deck(lection['vocabulary_unimportant'], f'{deck_name}::{lection["name"]}::4 Unimportant Vocabulary', anki_model_vocabulary, start_uuid + i*10 + 4, sound_files)
    anki_decks.append(vocab_deck_unimportant)
  
  anki_package = genanki.Package(anki_decks)

  media_files = [f'data/wanikani/images/{image}' for image in image_files]
  media_files.extend([f'data/wanikani/sound/{sound}' for sound in sound_files])

  # font
  media_files.append("data/fonts/_hirakakyprow3.otf")

  anki_package.media_files = media_files

  anki_package.write_to_file('wanigenki.apkg')
