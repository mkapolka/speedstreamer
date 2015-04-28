import sys
from subprocess import call

import requests
import simplejson as json

PER_PAGE = 30


def print_channels(channels, offset=0, per_page=None):
    for index, channel in enumerate(channels[offset:offset+per_page or len(channels)]):
        print("[%s] %s playing %s (%s)" %
            (offset + index,
             channel['display_name'],
             channel['meta_game'],
             channel['title']
            ))

def main():
    r = requests.get('http://api.speedrunslive.com/frontend/streams')
    data = json.loads(r.text)

    channels = data['_source']['channels']

    sorted_by_viewers = sorted(channels, key=lambda x: x['current_viewers'], reverse=True)
    channel = None

    offset = 0
    while not channel:
        print_channels(sorted_by_viewers, offset, PER_PAGE)
        print "[p]revious, [n]ext, [q]uit"
        ri = raw_input()
        if ri == 'n':
            offset += PER_PAGE
        elif ri == 'p':
            offset -= PER_PAGE
        elif ri == 'q':
            return
        else:
            try:
                index = int(ri)
                channel = sorted_by_viewers[index]
            except ValueError:
                print "Please select a valid number."

    quality = None
    while not quality:
        choice = raw_input("Quality? [a]udio [l]ow [m]edium [h]igh or [s]ource?")
        quality = {
            'a': 'audio',
            'l': 'low',
            'm': 'medium',
            'h': 'high',
            's': 'source'
        }.get(choice)


    call(["livestreamer", "http://twitch.tv/%s" % channel['name'], quality])

if __name__ == "__main__":
    main()
