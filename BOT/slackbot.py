import logging
import os

import requests
from slack import RTMClient


@RTMClient.run_on(event="message")
def say_hello(**payload):
    try:
        data = payload['data']
        logging.info(data)
        if 'subtype' not in data:
            web_client = payload['web_client']
            channel_id = data['channel']
            thread_ts = data['ts']

            try:
                text = data['text'].strip().replace('.', '')
                response = requests.get(
                    url='http://127.0.0.1:5000/chatbot',
                    params={'text': text}
                )
                text = response.text
            except Exception as e:
                logging.warning(e)
                text = "I have no idea"
            web_client.chat_postMessage(
                channel=channel_id,
                text=text,
                thread_ts=thread_ts,
                username="fred",
                icon_emoji=":panda_face"
            )
    except Exception as e:
        logging.warning(e)


if __name__ == "__main__":
    slack_token = os.environ["SLACK_API_TOKEN"]
    rtm_client = RTMClient(token=slack_token)
    rtm_client.start()
