import re

import requests

from scrapers.base import BaseScraper, GOOGLE_CACHE_URL

# for script.common.plugin.cache
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("theberrics", 24)


BERRICS_VIDEO_URL = 'http://berrics.vo.llnwd.net/o45/{0}.mp4'
VIDEO_ID_RE = re.compile('data-media-file-id="([a-zA-Z0-9\-]+)"\s')


def get_items_for_category(category, plugin):
    """
    Collects all video items for the provided category
    """
    scraper = BaseScraper.factory(category, plugin)

    # Return cached result or calls function.  Cache expires every 24 hours
    return cache.cacheFunction(scraper.get_items)


def add_autoplay(url):
    """
    Adds autoplay to the url if it isn't present
    """
    if not url.endswith('?autoplay'):
        url = url + '?autoplay'
    return url


def get_video_url(url):
    """
    Fetches the actual mp4 video file url
    """
    url = add_autoplay(url)
    try:
        r = requests.get(url, timeout=5)
    except requests.Timeout:
        # If we timeout, try to load the page from google cache.
        cache_url = GOOGLE_CACHE_URL.format(url)
        r = requests.get(cache_url)
        if r.status_code != 200:
            raise Exception("Connection timed out trying to load video page "
                            "%s" % url)
    found = VIDEO_ID_RE.findall(r.text)
    if found:
        return BERRICS_VIDEO_URL.format(found[0])


def create_item_for_category(name, category, media_url, plugin):
    """
    Creates an item for the category list page
    """
    item = {
        'label': name,
        'icon': "{0}{1}.png".format(media_url, category),
        'thumbnail': "{0}{1}.png".format(media_url, category),
        'path': plugin.url_for('show_category', category=category)
    }
    return item
