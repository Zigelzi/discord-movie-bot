import requests
from bs4 import BeautifulSoup

def get_movie_name(source_url):
    r = requests.get(source_url)
    bs = BeautifulSoup(r.text, features='html.parser')
    movie_name = ''
    metas = bs.find_all('meta')
    for meta in metas:
        if 'property' in meta.attrs:
            if meta.attrs['property'] == 'og:title':
                movie_name = meta.attrs['content']
    return movie_name
