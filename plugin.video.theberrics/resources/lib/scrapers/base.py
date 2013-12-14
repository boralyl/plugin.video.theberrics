import importlib
import re

from BeautifulSoup import BeautifulSoup
import requests


BASE_URL = 'http://theberrics.com'
GOOGLE_CACHE_URL = 'http://webcache.googleusercontent.com/search?q=cache:{0}'
SLUG_RE = re.compile(r'([a-zA-Z0-9\-]+)\.')


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

    def get_title_from_url(self, url, replace=None):
        """
        Grabs the title from the end of the URL.

        Optionally if replace is specified, that string will be removed
        from the title.  This is useful if the url contains the category
        and the title.  i.e. /category-some-title.html?foo=bar would become
        `Some Title` if we specified replace to be 'category'
        """
        title = None
        # Grab the slug portion of the url.  No need to catch an exception
        # as we will get the entire string if the '/' character isn't present
        slug_url = url.split('/')[-1]
        # Get just the slug and none of the .html or params
        match = SLUG_RE.match(slug_url)
        if match:
            slug = match.groups()[0]
            title = ' '.join([word.title() for word in slug.split('-')])
            title = re.sub('(?i)' + re.escape(replace), '', title)
            title = title.strip()
        return title

    @staticmethod
    def factory(category, plugin):
        """
        Factory method for instantiating the correct scraper class based
        on the category string
        """
        # Dynamically import the module
        module = 'resources.lib.scrapers.' + category.replace('_', '')
        module = importlib.import_module(module)

        # Get the class name and return the instance
        class_name = ''.join([word.title() for word in category.split('_')])
        class_name += 'Scraper'
        klass = getattr(module, class_name)
        return klass(plugin)
