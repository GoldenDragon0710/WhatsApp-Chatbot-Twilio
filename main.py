from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import openai
import json
import requests
import speech_recognition as sr

app = Flask(__name__)

# SECRET KEY CAN BE ANYTHING
app.config['SECRET_KEY'] = 'top-secret!'

# OPEN-AI API KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_text(question):
    print("question----", question)
    response = openai.Completion.create(
        prompt=str(question),
        model="text-davinci-003",
        max_tokens=1024,
        temperature=0.2,
    )

    answer = response.choices[0].text
    return answer

# endpoint for incoming WhatsApp messages
@app.route("/wamsg", methods=['POST'])
def wamsg():
    # parse incoming WhatsApp message
    incoming_msg = request.form.get('Body').lower()

    res = MessagingResponse()
    reply = res.message()
    # responded = ""

    # if incoming_msg:
    answer = ask_text(incoming_msg)
    reply.body(answer)
        # responded = "text"

    # if responded == "":
    #     reply.body("Message Cannot Be Empty!")
        # print("error")

    # send transcribed text as WhatsApp message
    return str(res)
    
if __name__ == '__main__':
    app.run(debug=True)