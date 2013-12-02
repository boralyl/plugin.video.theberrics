import re

import requests

from scrapers.bangin import BanginScraper
from scrapers.battlecommander import BattleCommanderScraper
from scrapers.diyordie import DiyOrDieScraper
from scrapers.generalops import GeneralOpsScraper
from scrapers.offthegrid import OffTheGridScraper
from scrapers.process import ProcessScraper
from scrapers.recruit import RecruitScraper
from scrapers.shootallskaters import ShootAllSkatersScraper
from scrapers.trajectory import TrajectoryScraper
from scrapers.vhs import VHSScraper


BERRICS_VIDEO_URL = 'http://berrics.vo.llnwd.net/o45/{0}.mp4'
VIDEO_ID_RE = re.compile('data-media-file-id="([a-zA-Z0-9\-]+)"\s')


def get_items_for_category(category, plugin):
    """
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
        # @TODO: Need caching, especially for this one, lots of items on a page
        scraper = GeneralOpsScraper(plugin)
    elif category == 'shoot_all':
        scraper = ShootAllSkatersScraper(plugin)
    return scraper.get_items()


def add_autoplay(url):
    if not url.endswith('?autoplay'):
        url = url + '?autoplay'
    return url


def get_video_url(url):
    url = add_autoplay(url)
    r = requests.get(url)
    found = VIDEO_ID_RE.findall(r.text)
    if found:
        return BERRICS_VIDEO_URL.format(found[0])
