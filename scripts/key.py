#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
""" get gnome keyring passwords """

import sys
import gnomekeyring as gkey
import getpass

def set_password(username, server, password):
    attrs = {
        'user':username,
        'server':server,
        'protocol':'imap'
    }
    gkey.item_create_sync(
        gkey.get_default_keyring_sync(),
        gkey.ITEM_NETWORK_PASSWORD,
        'Mail-Password %s' % server,
        attrs,
        password,
        True
    )

def get_password(username, server):
    attrs = {
        'user':username,
        'server':server,
        'protocol':'imap'
    }
    items = gkey.find_items_sync(
        gkey.ITEM_NETWORK_PASSWORD,
        attrs
    )
    return items[0].secret

if __name__ == '__main__':
    try:
        action, username, server = sys.argv[1], sys.argv[2], sys.argv[3]
    except IndexError:
        sys.exit('Syntax: [set|get] item')
    if action == 'set':
        password = getpass.getpass()
        set_password(username, server, password)
    elif action == 'get':
        print get_password(username, server)
    else:
        sys.exit('Syntax: [set|get] item')
