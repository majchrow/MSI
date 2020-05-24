from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from chatterbot.response_selection import get_random_response


class WeatherAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        if 'weather' in statement.text.lower():
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        import requests
        try:
            req = requests.get(
                url="https://www.metaweather.com/api/location/523920/"
            )
            if 'tomorrow' in statement.text.lower():
                text = "The weather tomorrow will be {:.2f} Celsius".format(
                    req.json()['consolidated_weather'][1]['the_temp'])
            else:
                text = "The weather today is {:.2f} Celsius".format(req.json()['consolidated_weather'][0]['the_temp'])
            response = Statement(text=text)
            response.confidence = 1
        except Exception as e:
            response = Statement(text="I don't know")
            response.confidence = 0
        return response


class TimeAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        if all(word in statement.text.lower() for word in ('time', 'what')):
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        from datetime import datetime
        now = datetime.now()

        response = Statement(text='The current time is ' + now.strftime('%I:%M %p'))
        response.confidence = 1
        return response


ADAPTERS = [
    {
        "import_path": "chatterbot.logic.BestMatch",
        "response_selection_method": get_random_response
    },
    {
        "import_path": "utils.adapters.WeatherAdapter"
    },
    {
        "import_path": "utils.adapters.TimeAdapter"
    }
]
