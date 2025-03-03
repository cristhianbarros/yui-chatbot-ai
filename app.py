from os import environ
from flask import Flask, request, make_response
from services.MessageHandler import message_handler



VERIFY_TOKEN = environ.get('VERIFY_TOKEN')

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to yui chat "

@app.route("/webhook/")
def verify_webhook():

    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token != VERIFY_TOKEN:
        return "Authentication failed. Invalid Token."

    return make_response( challenge, 200)

@app.route("/webhook", methods=["POST"])
def handle_incoming():
    data = request.get_json()
    message = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages', [{}])[0]
    sender_info = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('contacts', [{}])[0]

    if message:
        message_handler.handle_incoming_message(message, sender_info)

    return make_response('', 200)

if __name__ == "__main__":
    app.run(debug=True)