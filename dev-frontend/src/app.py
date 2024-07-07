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
      subDefinitions
      subExamples
    }
  }
}
"""

client = GraphqlClient(url)

st.title("Dictionary App")
word = st.text_input(label="Define words")

if word:
    vars = {"word": word}
    response = client.execute(query, vars)
    result = response.get('data', {}).get('wordInfo')

    meta_word_info = MetaWordInfo(**result['metaWordInfo'])
    word_meanings = [WordMeaning(**wm) for wm in result['wordMeanings']]

    st.header(meta_word_info.word.title())

    for ipa, audio_file in zip(meta_word_info.ipa, meta_word_info.audioFile):
        col1, col2 = st.columns([4,1])
        col2.subheader(ipa)
        
        if col1.button("Pronounce"):
            st.audio(audio_file, autoplay=True)

    cats = set()
    c = 1
    for word_meaning in word_meanings:
        if word_meaning.lexicalCategory not in cats:
            c = 1
            cats.add(word_meaning.lexicalCategory)
            st.markdown(f"##### *{word_meaning.lexicalCategory}*")
        for defn in word_meaning.definitions:
            st.write(f"{c}. {defn}")
        for ex in word_meaning.examples:
            st.markdown(f"*{ex}*")
        for i, sub_defn in enumerate(word_meaning.subDefinitions):
            st.write(f"- {sub_defn}")
            for sub_ex in word_meaning.subExamples[i]:
                st.markdown(f"*{sub_ex}*")
        c += 1


