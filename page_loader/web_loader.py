import requests


def get_web_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content
