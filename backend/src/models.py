from pydantic import BaseModel


class MetaWordInfo(BaseModel):
    word: str
    etymologies: list[str]
    phonetic_notation: list[str]
    phonetic_spelling: list[str]
    audio_file: list[str]


class WordInfo(BaseModel):
    lexical_category: str
    definitions: list[str]
    sub_definitions: list[str]
    examples: list[str]
    sub_examples: list[str]