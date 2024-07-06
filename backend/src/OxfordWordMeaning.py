import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OxfordWordMeaning:

    def __init__(self):
        self.__app_id = os.getenv('OXFORD_API_ID')
        self.__app_key = os.getenv('OXFORD_API_KEY')

    def get_data(self, lang: str, term: str) -> dict:
        url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/{lang}/{term.lower()}"
        r = requests.get(url, headers = {"app_id" : self.__app_id, "app_key" : self.__app_key})
        term = r.json()
        return term
    
    def parse_data(self, lang: str, term: str, data: dict):
        word_infos = []

        meta_word_info = {}
        word_info = {}

        data = data
        results = data.get('results', [])
        for result in results:
            word = result.get('word')
            lexical_entries = result.get('lexicalEntries', [])

            for lexical_entry in lexical_entries:
                lexical_category = lexical_entry.get('lexicalCategory', {}).get('text')
                entries = lexical_entry.get('entries', [])

                for entry in entries:
                    etymologies = entry.get('etymologies', [])
                    pronunciations = entry.get('pronunciations', [])
                    senses = entry.get('senses', [])

                    dialects = [', '.join(pronunciation.get('dialects', [])) for pronunciation in pronunciations]
                    phonetic_notation = [pronunciation.get('phoneticNotation') for pronunciation in pronunciations]
                    phonetic_spelling = [pronunciation.get('phoneticSpelling') for pronunciation in pronunciations]
                    audio_file = [pronunciation.get('audioFile') for pronunciation in pronunciations if pronunciation.get('audioFile')]
                    
                    for sense in senses:
                        definitions = sense.get('definitions', [])
                        short_definitions = sense.get('shortDefinitions', [])
                        examples = [example.get('text', '') for example in sense.get('examples', []) if example]

                        subsenses = sense.get('subsenses', [])
                        if subsenses:
                            sub_definitions = [definition for subsense in subsenses for definition in subsense.get('definitions', [])]
                            sub_short_definitions = [subsense.get('shortDefinitions', []) for subsense in subsenses]
                            sub_examples = [example.get('text', '') for subsense in subsenses for example in subsense.get('examples', []) if example]
                        else:
                            sub_definitions = []
                            sub_examples = []
                        
                        if not meta_word_info:
                            meta_word_info = {
                                'word': word,
                                'etymologies': etymologies,
                                'phonetic_notation': phonetic_notation,
                                'phonetic_spelling': phonetic_spelling,
                                'audio_file': audio_file
                            }

                        word_info = {
                            'lexical_category': lexical_category,
                            'definitions': definitions,
                            'sub_definitions': sub_definitions,
                            'examples': examples,
                            'sub_examples': sub_examples,
                        }

                        word_infos.append(word_info)
                
        return meta_word_info, word_infos