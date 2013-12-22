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


@plugin.route('/category/<category>/years')
def show_years_for_category(category):
    """
    Shows all years for the selected category
    """
    items = utils.get_years_for_category(category, plugin)
    return items


@plugin.route('/category/<category>/year/<year>')
def show_year(category, year):
    items, has_next = utils.get_items_for_year(category, year, plugin)
    return items


@plugin.route('/category/<category>/<page>')
def show_category(category, page='1'):
    """
    Category page, lists all videos for the provided category
    """
    page = int(page)
    items, has_next = utils.get_items_for_category(category, plugin, page)

    has_pagination = False
    if has_next:
        items.append({
            'label': 'Next >>',
            'path': plugin.url_for('show_category', category=category,
                                   page=str(page + 1))
        })
        has_pagination = True

    if page > 1:
        items.insert(0, {
            'label': '<< Previous',
            'path': plugin.url_for('show_category', category=category,
                                   page=str(page - 1))
        })
        has_pagination = True

    if has_pagination:
        # need to manually call finish so xbmc knows not to store history
        # for the next/previous items.
        return plugin.finish(items, update_listing=True)
    else:
        return items


@plugin.route('/')
def categories():
    """
    The index view, which lists all categories
    """
    categories = (
        # (label, category, has_multiple_years_pages)
        ('All Eyes On', 'all_eyes_on', True),
        ('Bangin!', 'bangin', True),
        ('Battle Commander', 'battle_commander', False),
        ('Bombaklats', 'bombaklats', True),
        ('DIY or DIE', 'diy_or_die', True),
        ('Established', 'est', True),
        ('First Try Fridays', 'first_try_fridays', True),
        ('General Ops', 'general_ops', True),
        ('Highlights', 'highlights', True),
        ('Off The Grid', 'off_the_grid', True),
        ('Process', 'process', True),
        ('Recruit', 'recruit', False),
        ('Shoot All Skaters', 'shoot_all_skaters', True),
        ('Thrashin\' Thursdays', 'thrashin_thursdays', True),
        ('Trajectory', 'trajectory', True),
        ('Trickipedia', 'trickipedia', False),
        ('United Nations', 'united_nations', False),
        ('VHS', 'vhs', True),
        ('Wednesdays With Reda', 'wednesdays_with_reda', True),
    )
    items = [utils.create_item_for_category(
                name, category, has_years, MEDIA_URL, plugin)
             for name, category, has_years in categories]
    return items


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception as e:
        msg = "Error: check logs.  %s" % (e.message,)
        plugin.notify(msg=msg, delay=8000)
