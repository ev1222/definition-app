import strawberry
from strawberry.asgi import GraphQL
from strawberry.experimental import pydantic

from typing import List

from .models import MetaWordInfo, WordInfo
from .resolvers import fetch_word_info


@pydantic.type(model=MetaWordInfo, all_fields=True)
class MetaWordInfoType:
    pass

@pydantic.type(model=WordInfo, all_fields=True)
class WordInfoType:
    pass

@strawberry.type
class WordInfoResult:
    metaWordInfo: MetaWordInfoType
    wordInfo: List[WordInfoType]


@strawberry.type
class Query:
    @strawberry.field
    def get_word_info(lang: str, term: str) -> WordInfoResult:
        meta_word_info, word_infos = fetch_word_info(lang, term)
        return WordInfoResult(metaWordInfo=meta_word_info, wordInfo=word_infos)
    

schema = strawberry.Schema(query=Query)
app = GraphQL(schema)



