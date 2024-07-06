import strawberry
from strawberry.experimental import pydantic

from .models import MetaWordInfo, WordMeaning


@pydantic.type(model=MetaWordInfo, all_fields=True)
class MetaWordInfoType:
    pass


@pydantic.type(model=WordMeaning, all_fields=True)
class WordMeaningType:
    pass


@strawberry.type
class WordMeaningResult:
    meta_word_info: MetaWordInfoType
    word_meanings: list[WordMeaningType]
