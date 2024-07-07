from pydantic import BaseModel


class MetaWordInfo(BaseModel):
    word: str
    etymologies: list[str]
    ipa: list[str]
    audioFile: list[str]


class WordMeaning(BaseModel):
    lexicalCategory: str
    definitions: list[str]
    examples: list[str]
    synonyms: list[str]
    subDefinitions: list[str]
    subExamples: list[list[str]]
    subSynonyms: list[list[str]]
