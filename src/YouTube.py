from typing import List, Optional
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class YouTube():
    def __init__(self):
        pass

    def __get_video_info(self, url: str, language: List[str], translation: Optional[str] = None) -> List:
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=True, # de pytuve
            language=language, # Lenguaje del video
            translation=translation, # Traducción del contenido de video
            transcript_format=TranscriptFormat.CHUNKS, # [TEXT = 'text', LINES = 'lines', CHUNKS = 'chunks']
            chunk_size_seconds=180,
        )

        return loader.load()

    def generate_summary(self, url: str, language: List[str] = ["es", "en"], translation: Optional[str] = None) -> str:
        documents = self.__get_video_info(url, language, translation)
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_template(
            "Resume del siguiente contenido que es de un video de YouTube:\n\n{context}"
        )
        chain = create_stuff_documents_chain(llm, prompt)
        summary = chain.invoke({"context": documents})
        return summary
    

if __name__ == "__main__":
    yt = YouTube()
    url = "https://youtu.be/1wvL99nmIUU?si=eGXf5w-iI3qJsrvo"
    summary = yt.generate_summary(url)
    print(summary)