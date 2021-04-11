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

"""

radical_backside="""
<div class="kanji">{{word}}</div>

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










html_kanji_kana = """
<font size="6px" color="#C0C0C0"><span class="kanji">{{kanjis}}</span></font>
<br>
<font size="15px"><span class="kana">{{japanese_kana}}</span></font>
<br>
"""

html_sound="""
{{sound}}
<br>
"""

html_frontside="""
{{FrontSide}}
"""

html_meaning="""
<font size="4px" color="#C0C0C0">Meaning: </font>
<br>
"""

html_english="""
<font size="15px"><span class="text">{{english}}</span></font>
<br>
"""

html_kanji_meaning="""
<br>
{{#kanji_meaning}}
<font size="4px" color="#C0C0C0">Kanji Meaning: </font>
<br>
<font size="6px"><span class="text">{{kanjis}}</span></font>
<br>
<font size="6px"><span class="text">{{kanji_meaning}}</span></font>
<br>
{{/kanji_meaning}}
"""

css="""
.card {
font-family: arial;
font-size: 20px;
text-align: center;
}
"""


class GenkiNote(genanki.Note):
  pass
    # @property
    # def guid(self):
    #     return genanki.guid_for(self.fields[0]) # uid
            

def gen_radical_deck(deck, deckpath: str, model: genanki.Model, uuid:int) -> genanki.Deck:
    full_name = f'{deckpath}::radicals'
    anki_deck = genanki.Deck(uuid, full_name)
    for c in deck:
        note = GenkiNote(
            model=model,
            fields=[
                c['word'], 
                ", ".join(c['meanings']),
                c['meaning_mnemonic'], 
            ],
            )
        anki_deck.add_note(note)
    return anki_deck

def export_to_anki(decks: List):
    anki_model = genanki.Model(
        1561628562,
        'Simple Model',
        fields=[
            {'name': 'word'},
            {'name': 'meanings'},
            {'name': 'meaning_mnemonic'},
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
    anki_decks = []
    sound_files = []
    start_uuid = 284860580
    for i,lection in enumerate(decks):
        radical_deck = gen_radical_deck(lection['radicals'], f'{lection["name"]}::Radicals', anki_model, start_uuid + i*10)
        anki_decks.append(radical_deck)
    
    anki_package = genanki.Package(anki_decks)

    anki_package.media_files = sound_files

    anki_package.write_to_file('wanigenki.apkg')
