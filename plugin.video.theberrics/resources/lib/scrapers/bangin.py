from base import BaseScraper, BASE_URL


class BanginScraper(BaseScraper):
    url = 'http://theberrics.com/bangin'

    def get_label(self, post):
        """
        """
        date = post.find("div", attrs={'class': 'post-date'})
        date = date.text
        name = post.find("div", attrs={'class': 'post-sub-title'})
        name = name.text
        name = name.replace('&nbsp;', '')
        if name:
            return "{0} - {1}".format(date, name)
        else:
            return date

    def get_icon(self, post):
        """
        """
        img = post.find("img")
        try:
            icon = img['data-original']
        except KeyError:
            icon = 'DefaultVideo.png'
        return icon

    def get_url(self, post):
        """
        @TODO: what if we can't find it?  Return a sane default.
        """
        a = post.find("a")
        return BASE_URL + a['href']

    def get_item(self, post):
        """

        """
        label = self.get_label(post)
        icon = self.get_icon(post)
        url = self.get_url(post)
        path = self.plugin.url_for('play_video', url=url)
        #vid_url = self.get_video_url(url)
        item = {
            'label': label,
            'label2': label,
            'icon': icon,
            'thumbnail': icon,
            'path': path,
            'is_playable': True
        }
        return item

    def get_items(self):
        attrs = {'class': 'post-thumb standard-post-thumb'}
        posts = self.soup.findAll("div", attrs=attrs)
        return [self.get_item(post) for post in posts]
