import pandas as pd
from bs4 import BeautifulSoup
from requests import get

urls = [
    (f'https://allegro.pl/listing?string={category}&p={page}', category)
    for category in ('zabawka', 'kosmetyki', 'perfumy', 'środki czystości', 'napój')
    for page in range(1, 30)
]

# Web scrapping for NLP dataset (5 categories, each scrapping 29 x 100 allegro pages)
if __name__ == '__main__':
    results = {}
    for url, category in urls:
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        h2s = html_soup.find_all('h2', class_="_9c44d_LUA1k")
        for item in h2s:
            results[item.text] = category
    df = pd.DataFrame(results.items(), columns=['Name', 'Category'])
    df.to_csv('categories.csv')
