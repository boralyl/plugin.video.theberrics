from bangin import BanginScraper


class TrickipediaScraper(BanginScraper):
    url = 'http://theberrics.com/trickipedia'

    def get_label(self, post):
        trick = post.find("div", attrs={'class': 'trick'})
        trick = trick.text
        skater = post.find("div", attrs={'class': 'name'})
        skater = skater.text
        return "{0} - {1}".format(trick, skater)

    def get_icon(self, post):
        """
        Parses the HTML for the image for the video
        """
        img = post.find("img")
        try:
            icon = img['data-original']
            self.plugin.log(icon)
            icon = icon.replace('w=60', 'w=400')
            icon = icon.replace('h=60', 'h=400')
        except KeyError:
            icon = 'DefaultVideo.png'
        return icon

    def get_items(self):
        """
        Parses the HTML for all videos and creates a list of them
        """
        attrs = {'class': 'trick-div clearfix'}
        posts = self.soup.findAll("div", attrs=attrs)
        return [self.get_item(post) for post in posts]
