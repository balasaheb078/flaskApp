from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
import google.generativelanguage as genai

import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pygame
from time import sleep
import os

# Initialize the Flask app
app = Flask(__name__)

# Directly setting the API key
api_key = "AIzaSyALPf5IE31NMOoWNINUBfZygDnR9WsSj2M"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# List to store chat history
chat_history = []

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')

        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            sleep(1)

        pygame.mixer.music.unload()
        os.remove('temp.mp3')

    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['question']

    chat_history.append(f"User: {user_input}")

    context = "\n".join(chat_history)
    response = model.generate_content(f"{context}\nAI: {user_input}")
    
    output_text = response.text
    output_text = output_text.replace('*', '').replace('_', '')

    chat_history.append(f"AI: {output_text}")

    speak(output_text)
    return jsonify({'response': output_text, 'chat_history': chat_history})
    

if __name__ == '__main__':
    app.run(debug=True)
