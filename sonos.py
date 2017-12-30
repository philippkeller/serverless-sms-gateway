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
    s.speaker_info = dict(foo='bar') # hack to make socos.speaker_info() 
                                     # not try to make the call to internal_ip
    s.refresh = False
    return s

def replace_album(device, search_term):
    res = device.music_library.get_music_library_information('albums', search_term=search_term)
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
            replace_album(s, rest)

if __name__ == '__main__':
    # schwarz = get_sonos_device('192.168.1.118, 'phred-pui.internet-box.ch', 5193)
    weiss = get_sonos_device('192.168.1.117', 'phred-pui.internet-box.ch', 5194)
    replace_album(weiss, 'rächer')