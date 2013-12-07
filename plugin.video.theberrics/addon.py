# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html

from xbmcswift2 import Plugin

from resources.lib import utils


PLUGIN_ID = 'plugin.video.theberrics'
MEDIA_URL = 'special://home/addons/{0}/resources/media/'.format(PLUGIN_ID)

plugin = Plugin()


@plugin.route('/play/<url>')
def play_video(url):
    """
    Plays the passed in video
    """
    vid_url = utils.get_video_url(url)
    plugin.log.info('Playing url: %s' % vid_url)
    plugin.set_resolved_url(vid_url)


@plugin.route('/category/<category>')
def show_category(category):
    """
    Category page, lists all videos for the provided category
    """
    items = utils.get_items_for_category(category, plugin)
    return plugin.finish(items)


@plugin.route('/')
def categories():
    """
    The index view, which lists all categories
    """
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
            'label': 'First Try Fridays',
            'icon': MEDIA_URL + 'first_try_fridays.jpg',
            'thumbnail': MEDIA_URL + 'first_try_fridays.jpg',
            'path': plugin.url_for('show_category', category='first_try_f')
        },
        {
    	    'label': 'General Ops',
    	    'icon': MEDIA_URL + 'general_ops.jpg',
    	    'thumbnail': MEDIA_URL + 'general_ops.jpg',
            'path': plugin.url_for('show_category', category='general_ops')
    	},
        {
    	    'label': 'Off The Grid',
    	    'icon': MEDIA_URL + 'off_the_grid.png',
    	    'thumbnail': MEDIA_URL + 'off_the_grid.png',
            'path': plugin.url_for('show_category', category='off_the_grid')
    	},
        {
    	    'label': 'Process',
    	    'icon': MEDIA_URL + 'process.png',
    	    'thumbnail': MEDIA_URL + 'process.png',
            'path': plugin.url_for('show_category', category='process')
    	},
        {
    	    'label': 'Recruit',
    	    'icon': MEDIA_URL + 'recruit.jpg',
    	    'thumbnail': MEDIA_URL + 'recruit.jpg',
            'path': plugin.url_for('show_category', category='recruit')
    	},
        {
    	    'label': 'Shoot All Skaters',
    	    'icon': MEDIA_URL + 'shoot_all_skaters.png',
    	    'thumbnail': MEDIA_URL + 'shoot_all_skaters.png',
            'path': plugin.url_for('show_category', category='shoot_all')
    	},
        {
            'label': 'Thrashin\' Thursdays',
            'icon': MEDIA_URL + 'thrashin_thursdays.png',
            'thumbnail': MEDIA_URL + 'thrashin_thursdays.png',
            'path': plugin.url_for('show_category', category='thrashin_t')
        },
        {
    	    'label': 'Trajectory',
    	    'icon': MEDIA_URL + 'trajectory.jpg',
    	    'thumbnail': MEDIA_URL + 'trajectory.jpg',
            'path': plugin.url_for('show_category', category='trajectory')
    	},
        {
    	    'label': 'VHS',
    	    'icon': MEDIA_URL + 'vhs.jpg',
    	    'thumbnail': MEDIA_URL + 'vhs.jpg',
            'path': plugin.url_for('show_category', category='vhs')
    	},
        {
            'label': 'Wednesdays With Reda',
            'icon': MEDIA_URL + 'wednesdays_with_reda.png',
            'thumbnail': MEDIA_URL + 'wednesdays_with_reda.png',
            'path': plugin.url_for('show_category', category='wednesdays_reda')
        },
    ]
    return plugin.finish(items)


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception as e:
        msg = "Error: check logs.  %s" % (e.message,)
        plugin.notify(msg=msg, delay=8000)
