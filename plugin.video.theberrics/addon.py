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
    categories = (
        ('Bangin!', 'bangin'),
        ('Battle Commander', 'battle_commander'),
        ('DIY or DIE', 'diy_or_die'),
        ('First Try Fridays', 'first_try_fridays'),
        ('General Ops', 'general_ops'),
        ('Off The Grid', 'off_the_grid'),
        ('Process', 'process'),
        ('Recruit', 'recruit'),
        ('Shoot All Skaters', 'shoot_all_skaters'),
        ('Thrashin\' Thursdays', 'thrashin_thursdays'),
        ('Trajectory', 'trajectory'),
        ('United Nations', 'united_nations'),
        ('VHS', 'vhs'),
        ('Wednesdays With Reda', 'wednesdays_with_reda'),
    )
    items = [utils.create_item_for_category(name, category, MEDIA_URL, plugin)
             for name, category in categories]
    return items


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception as e:
        msg = "Error: check logs.  %s" % (e.message,)
        plugin.notify(msg=msg, delay=8000)
