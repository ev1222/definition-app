import strawberry
from strawberry.asgi import GraphQL

from .resolvers import fetch_word_info
from .API_types import WordMeaningResult


@strawberry.type
class Query:
    @strawberry.field
    def get_word_info(lang: str, term: str) -> WordMeaningResult:
        meta_word_info, word_meanings = fetch_word_info(lang, term)
        return WordMeaningResult(meta_word_info=meta_word_info, word_meanings=word_meanings)
    

schema = strawberry.Schema(query=Query)
app = GraphQL(schema)



