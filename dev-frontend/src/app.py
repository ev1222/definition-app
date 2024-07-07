import streamlit as st
from python_graphql_client import GraphqlClient

from models import MetaWordInfo, WordMeaning

url = "http://localhost:8000"

query = """
query($word: String!){
  wordInfo(lang: "en-us", word: $word){
    metaWordInfo {
      word
      etymologies
      ipa
      audioFile
    }
    wordMeanings {
      lexicalCategory
      definitions
      examples
      synonyms
      subDefinitions
      subExamples
      subSynonyms
    }
  }
}
"""

client = GraphqlClient(url)

st.title("Dictionary App")
word = st.text_input(label="Define words")

st.divider()

if word:
    vars = {"word": word}
    response = client.execute(query, vars)
    result = response.get('data', {}).get('wordInfo')

    meta_word_info = MetaWordInfo(**result['metaWordInfo'])
    word_meanings = [WordMeaning(**wm) for wm in result['wordMeanings']]

    definition_box = st.container(border=True)

    definition_box.header(meta_word_info.word.title())

    for ipa, audio_file in zip(meta_word_info.ipa, meta_word_info.audioFile):
        col1, col2 = definition_box.columns([3,1])
        col2.subheader(f"/{ipa}/")
        
        if col1.button("Pronounce"):
            st.audio(audio_file, autoplay=True)

    cats = set()
    c = 1
    for word_meaning in word_meanings:
        if word_meaning.lexicalCategory not in cats:
            c = 1
            cats.add(word_meaning.lexicalCategory)
            definition_box.caption(f"<p style='margin-bottom: 2px;'><i>{word_meaning.lexicalCategory.lower()}</i>", unsafe_allow_html=True)
        
        for defn in word_meaning.definitions:
            definition_box.write(f"<p style='margin-bottom: 2px;'>{c}. {defn}", unsafe_allow_html=True)
        
        for ex in word_meaning.examples:
            definition_box.write(f"&emsp;*\"{ex}\"*")
        
        for i, sub_defn in enumerate(word_meaning.subDefinitions):
            definition_box.markdown(f"<p style='margin-bottom: 2px;'>&emsp;• {sub_defn}", unsafe_allow_html=True)
            for sub_ex in word_meaning.subExamples[i]:
                definition_box.markdown(f"&emsp;&emsp;*\"{sub_ex}\"*")
        
        c += 1


