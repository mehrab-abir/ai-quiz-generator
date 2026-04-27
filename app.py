import streamlit as st
from apiCalling import note_generator, quiz_generator, audio_transcription
from PIL import Image
import time

st.header("Note Summary and Quiz Generator")
st.subheader("Upload images and have AI make quizzes for you")
st.divider()

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

with st.sidebar:
    images = st.file_uploader("Upload upto 3 images of your content: ",
                              type=["jpg","jpeg","png"],
                              accept_multiple_files=True)
    
    pil_images = []
    for img in images:
        pil_img = Image.open(img)
        pil_images.append(pil_img)

    if images:
        if(len(images) > 3):
            st.error("Maximum 3 images allowed")
        else:
            st.markdown(":blue[uploaded images:]")
            cols = st.columns(len(images))
            for i,img in enumerate(images):
                with cols[i]:
                    st.image(img)
    
    difficulty = st.selectbox("Choose difficulty level of the quiz:",
                              ("Easy","Medium","Hard"),
                              index=None)

    btn = st.button("Generate Quiz",type="primary")
    
if btn:
    if not images:
        st.error("You must upload at least 1 image")
    if difficulty is None:
        st.error("Select a difficulty level")
        
    if images and difficulty:
        if(len(images)>3):
            st.error("Maximum 3 images allowed")
        else:
            with st.container(border=True):
                st.subheader("Summarized Note:")

                with st.spinner("Summarizing note..."):
                    summarized_note = note_generator(pil_images)
                    st.write_stream(stream_text(summarized_note))
            with st.container(border=True):
                st.subheader("Audio Transcription:")
                with st.spinner("Generating audio: "):
                    
                    #clearning markdown symbols
                    summarized_note = summarized_note.replace("#",'')
                    summarized_note = summarized_note.replace("*",'')
                    summarized_note = summarized_note.replace("$",'')
                    
                    audioTranscribe = audio_transcription(summarized_note)
                    st.audio(audioTranscribe)
            
            with st.container(border=True):
                st.subheader(f"Quiz (Difficulty: {difficulty})")
                with st.spinner("Generating quiz..."):
                    generated_quiz = quiz_generator(pil_images,difficulty)
                    st.write_stream(stream_text(generated_quiz))
            
    
    
    