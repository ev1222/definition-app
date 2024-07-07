import os, json
import requests
from dotenv import load_dotenv

load_dotenv()


def get_abandon_json():
    # Get the path to the current directory (definition-app/dev-frontend/src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the top-level directory (definition-app) and the JSON file
    root_dir = os.path.abspath(os.path.join(current_dir, '../../'))
    json_file_path = os.path.join(root_dir, 'abandon.json')

    # Read the JSON response from the file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    return data


class OxfordWordMeaning:

    def __init__(self):
        self.__app_id = os.getenv("OXFORD_API_ID")
        self.__app_key = os.getenv("OXFORD_API_KEY")

    def __fetch_word_data(self, lang: str, word: str) -> dict:
        url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/{lang}/{word.lower()}"
        r = requests.get(
            url, headers={"app_id": self.__app_id, "app_key": self.__app_key}
        )
        word = r.json()
        return word

    def __parse_word_data(self, lang: str, word: str):
        meta_word_info = {}
        word_meaning = {}
        word_meanings = []

        # data = self.__fetch_word_data(lang, word)
        data = get_abandon_json()
        results = data.get("results", [])
        for result in results:
            word = result.get("word")
            lexical_entries = result.get("lexicalEntries", [])

            for lexical_entry in lexical_entries:
                lexical_category = lexical_entry.get("lexicalCategory", {}).get("text")
                entries = lexical_entry.get("entries", [])

                for entry in entries:
                    etymologies = entry.get("etymologies", [])
                    pronunciations = entry.get("pronunciations", [])
                    senses = entry.get("senses", [])

                    # dialects = [
                    #     ", ".join(pronunciation.get("dialects", []))
                    #     for pronunciation in pronunciations
                    # ]
                    phonetic_notation = [
                        pronunciation.get("phoneticNotation")
                        for pronunciation in pronunciations
                    ]
                    phonetic_spelling = [
                        pronunciation.get("phoneticSpelling")
                        for pronunciation in pronunciations
                    ]
                    audio_file = [
                        pronunciation.get("audioFile")
                        for pronunciation in pronunciations
                    ]

                    for sense in senses:
                        definitions = sense.get("definitions", [])
                        # short_definitions = sense.get("shortDefinitions", [])
                        examples = sense.get("examples", [])
                        synonyms = sense.get("synonyms", [])

                        subsenses = sense.get("subsenses", [])
                        if subsenses:
                            sub_definitions = [
                                subsense.get("definitions", [])
                                for subsense in subsenses
                            ]
                            # sub_short_definitions = [
                            #     subsense.get("shortDefinitions", [])
                            #     for subsense in subsenses
                            # ]
                            sub_examples = [
                                subsense.get("examples", []) for subsense in subsenses
                            ]
                            sub_synonyms = [subsense.get('synonyms', []) for subsense in subsenses]
                        else:
                            sub_definitions = []
                            # sub_short_definitions = []
                            sub_examples = []

                        if not meta_word_info:
                            meta_word_info = {
                                "word": word,
                                "etymologies": etymologies,
                                "phonetic_notation": phonetic_notation,
                                "phonetic_spelling": phonetic_spelling,
                                "audio_file": audio_file,
                            }

                        word_meaning = {
                            "lexical_category": lexical_category,
                            "definitions": definitions,
                            "examples": examples,
                            "synonyms": synonyms,
                            "sub_definitions": sub_definitions,
                            "sub_examples": sub_examples,
                            "sub_synonyms": sub_synonyms
                        }

                        word_meanings.append(word_meaning)

        return meta_word_info, word_meanings

    def __format_meta_info(self, meta_word_info: dict) -> dict:
        """
        Helper function that formats meta_word_info from parse_word_data for use in get_word_meaning.

        ### Args:
            meta_word_info (dict): The raw meta information dictionary.

        ### Returns:
            dict: Formatted meta information dictionary.
        """
        word = meta_word_info["word"]
        etymologies = meta_word_info["etymologies"]

        # Extract only IPA from pronunciations
        ipa_indices = [
            i for i, x in enumerate(meta_word_info["phonetic_notation"]) if x == "IPA"
        ]
        ipa = [meta_word_info["phonetic_spelling"][i] for i in ipa_indices]

        # Extract audio files for IPA (respelling pronunciation has None audioFile)
        audio_file = [file for file in meta_word_info["audio_file"] if file]

        # Reconstruct meta_word_info with desired fields and shape
        formatted_meta_word_info = {
            "word": word,
            "etymologies": etymologies,
            "ipa": ipa,
            "audio_file": audio_file,
        }

        return formatted_meta_word_info

    def __format_meanings(self, word_meanings: list[dict]) -> list[dict]:
        """
        Helper function that formats word_meanings from parse_word_data for use in get_word_meaning.

        ### Args:
            word_meanings (list[dict]): The raw word meanings list of dictionaries.

        ### Returns:
            list[dict]: Formatted list of word meaning dictionaries.
        """
        formatted_meanings = []
        for wm in word_meanings:
            lexical_category = wm["lexical_category"]
            definitions = wm["definitions"]

            # Extract text from examples
            examples = [example.get("text") for example in wm["examples"] if example]

            # Extract text form synonyms
            synonyms = [synonym.get("text") for synonym in wm["synonyms"] if synonym]

            # Flatten sub_definitions
            sub_definitions = [
                sub_def for sublist in wm["sub_definitions"] for sub_def in sublist
            ]

            # Extract text from sub_examples while maintaining sublist structure
            sub_examples = [
                [example.get("text") for example in sublist]
                for sublist in wm["sub_examples"]
            ]

            # Extract text from sub_synonyms while maintaining sublist structure
            sub_synonyms = [
                [synonym.get("text") for synonym in sublist]
                for sublist in wm["sub_synonyms"]
            ]

            # Reconstruct word_meanings with desired fields and shape
            word_meaning = {
                "lexical_category": lexical_category,
                "definitions": definitions,
                "examples": examples,
                "synonyms": synonyms,
                "sub_definitions": sub_definitions,
                "sub_examples": sub_examples,
                "sub_synonyms": sub_synonyms
            }
            formatted_meanings.append(word_meaning)
        return formatted_meanings

    def get_word_meaning(self, lang: str, word: str) -> tuple[dict, list[dict]]:
        """
        Get meta information and all meanings for a given word in the specified language.

        ### Args:
            lang (str): The language of the word to define.
            word (str): The word to define.

        ### Returns:
            tuple[dict, list[dict]]: A tuple containing meta_word_info dictionary and word_meanings list of word_meaning dictionaries.
                meta_word_info = {
                    'word': str,
                    'etymologies': list[str],
                    'ipa': list[str],
                    'audio_file': list[str]
                }

                word_meaning = {
                    'lexical_category': str,
                    'definitions': list[str],
                    'sub_definitions': list[str],
                    'examples': list[str],
                    'sub_examples': list[list[str]],
                }
        """
        meta_word_info, word_meanings = self.__parse_word_data(lang, word)

        meta_word_info = self.__format_meta_info(meta_word_info)
        word_meanings = self.__format_meanings(word_meanings)

        return meta_word_info, word_meanings
