from pydantic import BaseModel


class MetaWordInfo(BaseModel):
    word: str
    etymologies: list[str]
    ipa: list[str]
    audio_file: list[str]


class WordMeaning(BaseModel):
    lexical_category: str
    definitions: list[str]
    examples: list[str]
    synonyms: list[str]
    sub_definitions: list[str]
    sub_examples: list[list[str]]
    sub_synonyms: list[list[str]]
