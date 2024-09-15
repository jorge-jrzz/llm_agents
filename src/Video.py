from typing import List, Dict
from pathlib import Path
import os
from moviepy.editor import *
import whisper
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Video():
    
    def extract_audio(self, video_path: str, audio_path: str) -> str:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        print(f"Audio extracted and saved at {audio_path}")
        return audio_path
        
    def transcribe_audio(self, audio_path: str) -> str:
        model = whisper.load_model("small")
        result = model.transcribe(audio_path)
        return result["text"]
    
    def __get_documents(self, transcribed_text: str, metadata: Dict) -> List:
        return [
            Document(
                page_content=transcribed_text,
                metadata=metadata
            )
        ]
    
    def generate_sumary(self, video_path: str, audio_path: str) -> str:
        audio = self.extract_audio(video_path, audio_path)
        text = self.transcribe_audio(audio)
        video = Path(video_path)
        metadata = {"title": video.name, "source": video_path}
        documents = self.__get_documents(text, metadata)
        llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_template(
            "Resume del siguiente contenido que es de un video:\n\n{context}"
        )
        chain = create_stuff_documents_chain(llm, prompt)
        summary = chain.invoke({"context": documents})
        return summary


if __name__ == "__main__":
    video = Video()
    video_path = "../video.mp4"
    audio_path = "./audio.mp3"
    summary = video.generate_sumary(video_path, audio_path)
    print(summary)