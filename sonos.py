import soco
import os

def get_sonos_device(internal_ip, external_hostname, port):
    import socket
    external_ip = socket.gethostbyname(external_hostname)

    # needs internal ip address for "is_master_of_group" check
    s = soco.SoCo(internal_ip)

    # replace port
    url = 'http://{}:{}'.format(external_ip, port)
    s.music_library.contentDirectory.base_url = url
    s.avTransport.base_url = url
    s.zoneGroupTopology.base_url = url
    s.alarmClock.base_url = url
    s.renderingControl.base_url = url
    s.speaker_info = dict(foo='bar') # hack to make socos.speaker_info() 
                                     # not try to make the call to internal_ip
    s.refresh = False
    return s

def replace_alarm(device, time):
    """
    remove all alarms and set new one-time-occurring alarm at time (str with 'HH::MM')
    """
    from soco import alarms
    import datetime

    t = datetime.datetime.strptime(time, "%H:%M").time()
    for a in list(alarms.get_alarms(zone=device)):
        a.remove()
    a = alarms.Alarm(device, t, None, 'ONCE')
    a.save()


def replace_queue(device, search_term):
    res = []
    for t in ['albums', 'playlists', 'artists', 'tracks']:
        res = device.music_library.get_music_library_information(t, search_term=search_term)
        if len(res) > 0:
            break
    device.clear_queue()
    for r in res:
        device.add_to_queue(r)
    device.play_from_queue(0)

# to trigger this you need to send an sms with the form
# 
# device action search terms
# with:
# - device: matches against SONOS_DEVICES last part of string
# - action: one of:
#   - r/re/replace: replaces current queue
#   - a/add: adds to current queue
def dispatcher(cmd):
    cmd = cmd.lower()
    device, action, rest = cmd.split(' ', 2)

    lines = os.environ['SONOS_DEVICES'].split(",")
    external_hostname = os.environ['SONOS_DYNDNS']
    s = None
    for line in lines:
        external_port, internal_ip, search_terms = line.split(':')
        search_terms = search_terms.lower().split(' ')
        if device in search_terms:
            s = get_sonos_device(internal_ip, external_hostname, external_port)

    if s:
        if action in ['r', 're', 'replace']:
            replace_queue(s, rest)
        elif action in ['al', 'alarm']:
            replace_alarm(s, rest)

if __name__ == '__main__':
    schwarz = get_sonos_device('192.168.1.118', 'phred-pui.internet-box.ch', 5193)
    # weiss = get_sonos_device('192.168.1.117', 'phred-pui.internet-box.ch', 5194)
    # replace_album(weiss, 'rächer')
    print(schwarz.volume)