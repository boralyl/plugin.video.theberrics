import re

import requests

from scrapers.base import GOOGLE_CACHE_URL
from scrapers.bangin import BanginScraper
from scrapers.battlecommander import BattleCommanderScraper
from scrapers.diyordie import DiyOrDieScraper
from scrapers.firsttryfridays import FirstTryFridaysScraper
from scrapers.generalops import GeneralOpsScraper
from scrapers.offthegrid import OffTheGridScraper
from scrapers.process import ProcessScraper
from scrapers.recruit import RecruitScraper
from scrapers.shootallskaters import ShootAllSkatersScraper
from scrapers.thrashinthursdays import ThrashinThursdaysScraper
from scrapers.trajectory import TrajectoryScraper
from scrapers.vhs import VHSScraper
from scrapers.wednesdayswithreda import WednesdaysWithRedaScraper

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
    if category == 'bangin':
        scraper = BanginScraper(plugin)
    elif category == 'battle_commander':
        scraper = BattleCommanderScraper(plugin)
    elif category == 'diy_or_die':
        scraper = DiyOrDieScraper(plugin)
    elif category == 'recruit':
        scraper = RecruitScraper(plugin)
    elif category == 'off_the_grid':
        scraper = OffTheGridScraper(plugin)
    elif category == 'process':
        scraper = ProcessScraper(plugin)
    elif category == 'trajectory':
        scraper = TrajectoryScraper(plugin)
    elif category == 'vhs':
        scraper = VHSScraper(plugin)
    elif category == 'general_ops':
        # @TODO: 300 some videos on this page.  Should a limit be used?
        scraper = GeneralOpsScraper(plugin)
    elif category == 'shoot_all':
        scraper = ShootAllSkatersScraper(plugin)
    elif category == 'first_try_f':
        scraper = FirstTryFridaysScraper(plugin)
    elif category == 'thrashin_t':
        scraper = ThrashinThursdaysScraper(plugin)
    elif category == 'wednesdays_reda':
        scraper = WednesdaysWithRedaScraper(plugin)

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
