from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import openai
import requests
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# SECRET KEY CAN BE ANYTHING
app.config['SECRET_KEY'] = 'top-secret!'

Google_API_KEY = os.getenv("GOOGLE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_text(question):
    print("question----", question)
    response = openai.Completion.create(
        prompt=question,
        model="text-davinci-003",
        max_tokens=1024,
        temperature=0.2,
    )

    answer = response.choices[0].text
    return answer

def transcribe_audio(audio_file):
    # Set Google Speech-to-Text API endpoint URL and API key
    endpoint_url = "https://speech.googleapis.com/v1/speech:recognize?key=" + Google_API_KEY
    print("endpoint_url----", endpoint_url)
    
    # Set request data and headers
    request_data = {
        "audio": {
            "content": audio_file
        },
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "en-US"
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send request to the Google Speech-to-Text API endpoint
    response = requests.post(url=endpoint_url, json=request_data, headers=headers)
    
    # Extract transcription from response
    transcription = response.json()["results"][0]["alternatives"][0]["transcript"]
    
    return transcription

# endpoint for incoming WhatsApp messages
@app.route("/wamsg", methods=['POST'])
def wamsg():
    # Get the incoming message from WhatsApp
    incoming_msg = request.values.get("Body", "").strip().lower()

    answer = ""
    # If incoming message is an audio file
    if request.values.get("NumMedia", "") == "1" and request.values.get("MediaContentType0", "").startswith("audio/"):
        # Get the URL of the audio file
        url = request.values.get("MediaUrl0", "")

        # Download the audio file
        downloaded_file = requests.get(url).content
        
        # Transcribe the audio file using Google Speech-to-Text API
        transcription = transcribe_audio(downloaded_file)
        
        answer = ask_text(transcription)
    else:
        # If incoming message is not an audio file
        answer = ask_text(incoming_msg)

    res = MessagingResponse()
    reply = res.message()

    # send transcribed text as WhatsApp message
    reply.body(answer)
    return str(res)
    
if __name__ == '__main__':
    app.run(debug=True)