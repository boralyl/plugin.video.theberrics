from BeautifulSoup import BeautifulSoup
import requests


BASE_URL = 'http://theberrics.com'


class BaseScraper(object):

    def __init__(self, plugin):
        self.plugin = plugin
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text)
