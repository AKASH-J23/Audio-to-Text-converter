import streamlit as st
from pydub import AudioSegment,silence
import speech_recognition as sr
import os

recog=sr.Recognizer()
Result=""
st.markdown("<h1 style='text-align: center;'> Audio to text Converter </h1>",unsafe_allow_html=True)
st.markdown("---",unsafe_allow_html=True)
audio=st.file_uploader("Enter Your Audio File",type=["wav","mp3"])
if audio:
    st.audio(audio)
    audio_segment=AudioSegment.from_file(audio)
    chunks=silence.split_on_silence(audio_segment,min_silence_len=100,silence_thresh=audio_segment.dBFS-14,keep_silence=100)
    for index,chunk in enumerate(chunks):
        chunk.export(str(index)+".wav",format="wav")
        with sr.AudioFile(str(index)+".wav") as source:
            recorded=recog.record(source)
            try:
                text=recog.recognize_google(recorded)
                Result=Result+''+text
            except:
                Result=Result+" Unaudible"
    with st.form("Result"):
        res=st.text_area("Text",value=Result)
        btn=st.form_submit_button("Download")
        if btn:
            env_var=os.environ
            usr_loc=env_var.get("USERPROFILE")
            loc=usr_loc+"\Downloads\TextFile.txt"
            with open(loc,'w') as file:
                file.write(res)