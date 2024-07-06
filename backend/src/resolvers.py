from typing import Tuple, List

from .models import MetaWordInfo, WordInfo
from .OxfordWordMeaning import OxfordWordMeaning

def fetch_word_info(lang: str, term: str) -> Tuple[MetaWordInfo, List[WordInfo]]:
    meaning = OxfordWordMeaning()
    data = meaning.get_data(lang, term)

    meta_word_info, word_infos = meaning.parse_data(lang, term, data)
    print(meta_word_info)
    print(word_infos)
    word_infos = [WordInfo(**wi) for wi in word_infos]

    return MetaWordInfo(**meta_word_info), word_infos
    