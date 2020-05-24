Chatbot napisany w pythonie z użyciem biblioteki "chatterbot".

W folderze results znajdują się przykładowe konwersację z botem.
W folderze chatterbot znajduję się kod bota oraz odpowiednie pliki/skrypty potrzebne do odpalenia.

Bot jest podłaczony do slacka, dlatego wymaga token do bota SLACK_API_TOKEN ustawiony w zmiennej środowiskowej.
Bot również korzysta z restowego api, aby pobrać pogodę, natomiast reszta konwersacji jest wytrenowana ręcznie + na kilku dostępnych korpusach.
Bot obsługuje tylko język angielski.
Konwersacje odbwają się na slacku, alternatywnie zapytania można też wysyłać na endpoint "/chatbot" z argumentem "text".

Dostępne konwersacje (S - samodzielnie stworzone, K{X} - korpus X:
- powitanie (K{greetings})
- pożegnanie (S)
- zapytanie o godzinę (S)
- zapytanie o pogodę (na dzisiaj bądź jutro) (S)
- rozmowa o wiedźminie (S [+ K{movies} jako dodatek, ale nie korzystane w konwersacji]) 
- rozmowa o jedzeniu (S [+ K{food} jako dodatek, ale nie korzystane w konwersacji])
- zapytanie o dowcip (K{humor})
- profil robota (K{botprofile})
- rozmowa o komputerach (K{computers})
