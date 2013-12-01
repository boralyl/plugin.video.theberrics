from base import BaseScraper, BASE_URL


class BattleCommanderScraper(BaseScraper):
    url = 'http://theberrics.com/battle-commander'

    def get_label(self, url):
        name = url.split('/')[-1][:-5]
        return ' '.join([n.title() for n in name.split('-')])

    def get_url(self, post):
        a = post.find("a")
        return BASE_URL + a['href']

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

    def get_items(self):
        attrs = {'class': 'menu-item'}
        posts = self.soup.findAll("div", attrs=attrs)
        return [self.get_item(post) for post in posts]
