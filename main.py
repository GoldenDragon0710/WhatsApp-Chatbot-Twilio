from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import openai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = 'top-secret!'

Google_API_KEY = os.getenv("GOOGLE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_text(question):
    response = openai.Completion.create(
        prompt=question,
        model="text-davinci-003",
        max_tokens=1024,
        temperature=0.2,
    )

    answer = response.choices[0].text
    return answer


@app.route("/wamsg", methods=['POST'])
def wamsg():
    incoming_msg = request.values.get("Body", "").strip().lower()
    answer = ask_text(incoming_msg)
    res = MessagingResponse()
    reply = res.message()
    reply.body(answer)
    return str(res)


if __name__ == '__main__':
    app.run(debug=True)
