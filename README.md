# WhatsApp Chatbot using Twilio API

This is a simple WhatsApp chatbot built with the Twilio API in Python. The chatbot can respond to incoming messages on WhatsApp and provide predefined responses based on user inputs.

## Prerequisites

Before running this chatbot, make sure you have the following prerequisites installed:

- Python 3.10.11

```
pip install -r requirements.txt
```

## Configuration

- Go to `Messaging > Try it out > Send a WhatsApp message`
- Set configure the Sandbox URL.

Customization
To customize the chatbot's responses, modify the ask_text() function in the app.py file. You can add conditional statements and define the desired responses based on user inputs.

```
def ask_text(question):
    response = openai.Completion.create(
        prompt=question,
        model="text-davinci-003",
        max_tokens=1024,
        temperature=0.2,
    )

    answer = response.choices[0].text
    return answer
```

## Conclusion

With this simple WhatsApp chatbot, you can easily respond to incoming messages on WhatsApp using the Twilio API in Python. Customize the responses to suit your specific use case and provide a seamless conversational experience to your users.
