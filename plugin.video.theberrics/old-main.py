import requests
import urllib
from xbmcswift2 import xbmc, xbmcgui, xbmcplugin

print sys.argv

PLUGIN_ID = 'plugin.video.theberrics'
MEDIA_URL = 'special://home/addons/{0}/resources/media/'.format(PLUGIN_ID)


def add_category(title, image):
    """
    Handles the bolierplate of creating a folder list item
    """
    folder = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)
    label = {
        'Title': title,
        'count': 1
    }
    folder.setInfo(type="Video", infoLabels=label)

    data = {'c': title}
    data = urllib.urlencode(data)
    url = "{plugin}?{data}".format(plugin=sys.argv[0], data=data)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url,
                                listitem=folder, isFolder=True, totalItems=1)


def make_menu():
    image = MEDIA_URL + 'bangin.jpg'
    add_category('Bangin!', image)
    image = MEDIA_URL + 'battle_commander.jpg'
    add_category('Battle Commander', image)
    image = MEDIA_URL + 'diy_or_die.jpg'
    add_category('DIY or DIE', image)
    """
    banging_url = 'http://theberrics.com/bangin'
    params = {
        'play': 1,
        'video': 'http://berrics.vo.llnwd.net/o45/5297fdef-2ff4-4929-a104-5a05c6659e49.mp4',
        'image': 'http://img.theberrics.com/cc/b8508d0f7f0c034dc5e28579090ff7c5-64c974371ee332ab125ddf7c1cc04442.jpg',
        'title': 'Thanksgiving Recovery'
    }
    item = xbmcgui.ListItem(params['title'], params['video'],
                            'DefaultVideo.png', params['image'])
    item.setInfo(type='Video', infoLabels={'Title': params['title']})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=params['video'],
                                listitem=item, isFolder=False)
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def play(params):
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo(type=mediaType, infoLabels={ "Title": title })
    xbmc.Player().play(item=link, listitem=li)



print sys.argv
make_menu()


