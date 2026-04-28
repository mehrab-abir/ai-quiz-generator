from google import genai
from gtts import gTTS
from dotenv import load_dotenv
import os, io

load_dotenv();

apiKey = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=apiKey)

def note_generator(images):
    prompt = "summarize this note in no more than 100 words, add necessary markdown to format the text";
    
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[images,prompt]
    )
    
    return response.text

def quiz_generator(images, difficultyLevel,numQuiz):
    prompt = f"make {numQuiz} quiz questions in english language from the content of these images maintaining difficulty level {difficultyLevel}, among three options Easy, Medium, Hard. Also, provide answers of those questions at the end.";
    
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[images,prompt]
    )
    
    return response.text

def audio_transcription(text):
    speech = gTTS(text, lang='en',slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer;
