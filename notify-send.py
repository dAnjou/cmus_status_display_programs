#!/usr/bin/env python

from pynotify import Notification, init as pynotify_init
import sys
import subprocess
import shlex

def pynotify(title, body, icon='notification-audio-play'):
    n = Notification(title, body, icon)
    n.set_hint_string("x-canonical-append", "true")
    n.set_hint_int32("transient", 1)
    n.show()

def main():
    output = subprocess.check_output(shlex.split('cmus-remote -Q'))
    print output
    status = {}
    for line in output.split('\n'):
        elements = line.split(' ')
        if elements[0] in ['tag', 'set']:
            status[elements[1]] = ' '.join(elements[2:])
        else:
            status[elements[0]] = ' '.join(elements[1:])
    print status['status']
    if status['status'] not in ['paused', 'stopped']:
        print status['artist'], status['title']
        pynotify(status['artist'], status['title'])

if __name__ == "__main__":
    if not pynotify_init("cmus-notifier"):
        sys.exit(1)
    main()
