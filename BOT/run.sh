if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

source ./.venv/bin/activate

python -m pip install -r requirements.txt
python -m spacy download en

python chatbot.py &

echo "Chatbot is running on http://127.0.0.1:5000/chatbot endpoint, use 'text' param to get response"

if [ -z "$SLACK_API_TOKEN" ]; then
  echo "\$SLACK_API_TOKEN is not set, bot won't work"
  exit 1
fi

python slackbot.py &

echo "Slackbot is running, send private message to start conversation"
