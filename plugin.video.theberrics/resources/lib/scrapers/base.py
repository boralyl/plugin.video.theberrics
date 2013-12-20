import importlib
import re

from BeautifulSoup import BeautifulSoup
import requests


BASE_URL = 'http://theberrics.com'
GOOGLE_CACHE_URL = 'http://webcache.googleusercontent.com/search?q=cache:{0}'
SLUG_RE = re.compile(r'([a-zA-Z0-9\-]+)\.')
MAX_RESULTS = 30


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

    def log(self, msg):
        """
        A wrapper to more easily perform logging using the scraper
        """
        return self.plugin.log.debug(msg)

    def get_url(self, post):
        """
        Parses the HTML for the url for the video page
        @TODO: what if we can't find it?  Return a sane default.
        """
        a = post.find("a")
        return BASE_URL + a['href']

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
            if replace:
                title = re.sub('(?i)' + re.escape(replace), '', title)
            title = title.strip()
        return title

    def get_limit_and_offset_for_page(self, page):
        """

        """
        limit = MAX_RESULTS * page
        offset = (page - 1) * MAX_RESULTS
        return (limit, offset)

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


class ThumbnailScraper(BaseScraper):
    """
    Base class for pages with many video thumbnails.

    There are several types of video lists on theberrics.com, most of them
    follow this layout.  So all common scraping functions for thumbnails
    are in this class.
    """

    def get_label(self, post):
        """
        Parses the HTML for the label
        """
        date = post.find("div", attrs={'class': 'post-date'})
        date = date.text.encode('ascii', 'ignore')
        name = post.find("div", attrs={'class': 'post-sub-title'})
        name = name.text.encode('ascii', 'ignore')
        name = name.replace('&nbsp;', '')
        if name:
            return "{0} - {1}".format(date, name)
        else:
            return date

    def get_icon(self, post):
        """
        Parses the HTML for the image for the video
        """
        img = post.find("img")
        try:
            icon = img['data-original']
            # Some image paths start with //img/path/file.png so we need to
            # add the http: protocol.
            if not icon.startswith('http:'):
                icon = 'http:' + icon
        except KeyError:
            icon = 'DefaultVideo.png'
        return icon

    def get_item(self, post):
        """
        Creates a single playable item
        """
        label = self.get_label(post)
        icon = self.get_icon(post)
        url = self.get_url(post)
        path = self.plugin.url_for('play_video', url=url)
        item = {
            'label': label,
            'label2': label,
            'icon': icon,
            'thumbnail': icon,
            'path': path,
            'is_playable': True
        }
        return item

    def get_items(self, page=1):
        """
        Parses the HTML for all videos and creates a list of them
        """
        limit, offset = self.get_limit_and_offset_for_page(page)

        attrs = {'class': 'post-thumb standard-post-thumb'}
        kwargs = {}
        if page == 1:
            kwargs['limit'] = limit
        self.log("page: %s, limit: %s, offset: %s" % (page, limit, offset))
        posts = self.soup.findAll("div", attrs=attrs, **kwargs)
        num_posts = len(posts)
        posts = posts[offset:limit]
        return [self.get_item(post) for post in posts], num_posts


class MenuItemScraper(BaseScraper):
    """
    Base class for pages with divs that have menu-items.

    There are several types of video lists on theberrics.com, this handles
    the 2nd most common layout which is a bunch of rectangle items that have a
    menu-item class.
    """

    def get_label(self, url):
        name = url.split('/')[-1][:-5]
        return ' '.join([n.title() for n in name.split('-')])

    def get_icon(self, post):
        img = post.find("img")
        return img['src']

    def get_item(self, post):
        url = self.get_url(post)
        label = self.get_label(url)
        icon = self.get_icon(post)
        path = self.plugin.url_for('play_video', url=url)
        item = {
            'label': label,
            'label2': label,
            'icon': icon,
            'thumbnail': icon,
            'path': path,
            'is_playable': True
        }
        return item

    def get_items(self, page=1):
        self.log("page: %s" % (page,))
        limit = 30
        offset = (page - 1) * limit
        attrs = {'class': 'menu-item'}
        if page == 1:
            posts = self.soup.findAll("div", attrs=attrs, limit=MAX_RESULTS)
        else:
            posts = self.soup.findAll("div", attrs=attrs)[offset:limit]
        self.plugin.log.error(":shit")
        self.plugin.log.error(posts)
        self.log(posts)
        num_posts = len(posts)
        return ([self.get_item(post) for post in posts], num_posts)
