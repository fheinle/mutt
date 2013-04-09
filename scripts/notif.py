#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
"""notification on new mail"""

import pyinotify
import pynotify
from gtk.gdk import pixbuf_new_from_file

from mailbox import MaildirMessage
import os
import sys

ICON = pixbuf_new_from_file('/usr/share/icons/gnome/32x32/status/mail-unread.png')
MAILDIRS = [
    '/home/florian/.mail/florian-florianheinle.de/INBOX/new/',
]
pynotify.init('notif.py')

def notify(event):
    """Show Notifications"""
    mail = MaildirMessage(message=open(event.pathname, 'r'))
    n = pynotify.Notification(
            "Neue E-Mail",
            "Von: %s\n%s" % (mail['From'], mail['Subject'])
        )
    n.set_icon_from_pixbuf(icon)
    n.set_timeout(12000)
    n.show()

if __name__ == '__main__':
    # daemonize with double fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >> sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
    # decouple from previous environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print "Daemon Pid %d" % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    # now set up maildir watching
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, notify)
    for maildir in MAILDIRS:
        wm.add_watch(maildir, pyinotify.IN_CREATE|pyinotify.IN_MOVED_TO)
    notifier.loop()
