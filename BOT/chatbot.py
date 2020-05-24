import logging

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from flask import Flask, request

from utils.adapters import ADAPTERS
from utils.conversations import CONVERSATIONS, CORPUSES

app = Flask(__name__)

bot = ChatBot(
    name="fred",
    logic_adapters=ADAPTERS
)


def train_on_corpuses():
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(*CORPUSES)


def train_on_prepared_conversations():
    trainer = ListTrainer(bot)
    for topics in CONVERSATIONS.values():
        for conversation in topics.values():
            trainer.train(
                conversation=conversation
            )


@app.route("/")
def main():
    return "Hello, use /chatbot endpoint for chatting with bot"


@app.route("/chatbot")
def get_bot_response():
    userText = request.args.get('text')
    try:
        response = bot.get_response(userText)
    except Exception as e:
        logging.warning(e)
        response = "I have no idea"
    return str(response)


if __name__ == "__main__":
    train_on_corpuses()
    train_on_prepared_conversations()
    app.run()
