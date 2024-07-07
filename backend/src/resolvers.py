from typing import Tuple, List

from .models import MetaWordInfo, WordMeaning
from .OxfordWordMeaning import OxfordWordMeaning


def fetch_word_info(lang: str, word: str) -> Tuple[MetaWordInfo, List[WordMeaning]]:
    meaning = OxfordWordMeaning()

    meta_word_info, word_meanings = meaning.get_word_meaning(lang, word)

    return MetaWordInfo(**meta_word_info), [WordMeaning(**wm) for wm in word_meanings]
