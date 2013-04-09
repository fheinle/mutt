#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
""" get/set passwords from gnome keyring """

import keyring
import getpass


def get_password(item):
    return keyring.get_password('gmail', item)
 
def set_password(item, password):
    keyring.set_password('gmail', item, password)

if __name__ == '__main__':
    from sys import argv, exit
    try:
        action, item = argv[1], argv[2]
    except IndexError:
        exit('Syntax: [add|get] item')
    if action == 'add':
        password = getpass.getpass()
        set_password(item, password)
    elif action == 'get':
        print get_password(item)
    else:
        exit('Syntax: [add|get] item')
