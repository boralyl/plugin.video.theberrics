from base import ThumbnailScraper


class GeneralOpsScraper(ThumbnailScraper):
    url = 'http://theberrics.com/gen-ops'

    def get_label(self, post):
        date = post.find("div", attrs={'class': 'post-date'})
        date = date.text.encode('ascii', 'ignore')
        title = post.find("div", attrs={'class': 'post-title'})
        title = title.text.encode('ascii', 'ignore')
        subtitle = post.find("div", attrs={'class': 'post-sub-title'})
        subtitle = subtitle.text.encode('ascii', 'ignore')
        subtitle = subtitle.replace('&nbsp;', '')

        if date and title and subtitle:
            return "{0} - {1} {2}".format(date, title, subtitle)
        elif date and title:
            return "{0} - {1}".format(date, title)
        else:
            return date
