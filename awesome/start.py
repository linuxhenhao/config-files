#!/usr/bin/env python3
import subprocess
import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG)
# program in format ('binary_name', 'args', 'pgrep -f's match str')
# if match str is '', using the 'binary_name' instead
PROGRAMS = [('xcompmgr', '', ''),
            ('volumeicon', '', ''),
            # ('/usr/bin/ss-local', '-c /etc/shadowsocks.json', ''),
            ('lxqt-policykit-agent', '', ''),
            ('kupfer', '--no-splash', ''),
            ('fcitx', '', ''),
            ('x-session-manager', '', ''),
            ]


class ProcessRunner(threading.Thread):
    def __init__(self, nameAndArgsTuple):
        super(ProcessRunner, self).__init__()
        self._programAndArgs = nameAndArgsTuple
        print(self._programAndArgs)

    def run(self):
        subprocess.check_output(self._programAndArgs)


def start():
    remain = True
    while remain:
        remain = False  # set remain to False before run programs
        for name, args, pattern in PROGRAMS:
            try:
                if(pattern == ''):
                    subprocess.check_output(('pgrep', '-f', name))
                else:
                    subprocess.check_output(('pgrep', '-f', pattern))
                # -f option for pgrep to grep both commands and args
                logging.debug('{} is running'.format(name))
            except:  # exception will be raised if no pid of name was found
                # run this program
                remain = True
                # if any of the programs need to be run, set remain to True
                logging.debug('{} is not running'.format(name))
                argList = args.split(' ')
                argList.insert(0, name)
                print(argList)
                p = ProcessRunner(argList)
                p.daemon = True
                p.start()
        time.sleep(1)


start()
