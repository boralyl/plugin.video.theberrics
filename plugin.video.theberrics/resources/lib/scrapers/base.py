from BeautifulSoup import BeautifulSoup
import requests


BASE_URL = 'http://theberrics.com'
GOOGLE_CACHE_URL = 'http://webcache.googleusercontent.com/search?q=cache:{0}'


class BaseScraper(object):

    def __init__(self, plugin):
        self.plugin = plugin
        try:
            self.response = requests.get(self.url, timeout=5)
        except requests.Timeout:
            # If we timeout, try to load the page from google cache.
            url = GOOGLE_CACHE_URL.format(self.url)
            self.response = requests.get(url)
            if self.response.status_code != 200:
                raise Exception("Connection timed out to %s.  The website may "
                                "be down." % self.url)

        self.soup = BeautifulSoup(self.response.text)
