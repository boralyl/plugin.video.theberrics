from xbmcswift2 import Plugin

from resources.lib import utils


PLUGIN_ID = 'plugin.video.theberrics'
MEDIA_URL = 'special://home/addons/{0}/resources/media/'.format(PLUGIN_ID)

plugin = Plugin()


@plugin.route('/play/<url>')
def play_video(url):
    vid_url = utils.get_video_url(url)
    plugin.log.info('Playing url: %s' % vid_url)
    plugin.set_resolved_url(vid_url)


@plugin.route('/category/<category>')
def show_category(category):
    items = utils.get_items_for_category(category, plugin)
    return plugin.finish(items)


@plugin.route('/')
def categories():
    icon_path = MEDIA_URL + 'bangin.jpg'
    items = [
        {
	        'label': 'Bangin!',
	        'icon': MEDIA_URL + 'bangin.jpg',
	        'thumbnail': MEDIA_URL + 'bangin.jpg',
            'path': plugin.url_for('show_category', category='bangin')
	    },
        {
	        'label': 'Battle Commander',
	        'icon': MEDIA_URL + 'battle_commander.jpg',
	        'thumbnail': MEDIA_URL + 'battle_commander.jpg',
            'path': plugin.url_for('show_category', category='battle_commander')
	    },
        {
    	    'label': 'DIY or DIE',
    	    'icon': MEDIA_URL + 'diy_or_die.jpg',
    	    'thumbnail': MEDIA_URL + 'diy_or_die.jpg',
            'path': plugin.url_for('show_category', category='diy_or_die')
    	},
        {
    	    'label': 'Off The Grid',
    	    'icon': MEDIA_URL + 'off_the_grid.png',
    	    'thumbnail': MEDIA_URL + 'off_the_grid.png',
            'path': plugin.url_for('show_category', category='off_the_grid')
    	},
        {
    	    'label': 'Recruit',
    	    'icon': MEDIA_URL + 'recruit.jpg',
    	    'thumbnail': MEDIA_URL + 'recruit.jpg',
            'path': plugin.url_for('show_category', category='recruit')
    	},
    ]
    return plugin.finish(items)


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception:
        plugin.notify(msg='network_error')