#!/usr/bin/env python
# -*-coding: utf-8 -*-

# -----------------------------------------------------------------
# including the controller of seafile and xunlei services
# for orangepi
# -----------------------------------------------------------------

from subprocess import Popen, PIPE, check_call
import os
import time
# seafile parameters
kcpss_dir = '/root/kcpss/'
kcp_client = kcpss_dir+os.sep+'kcpclient'
ss_client = 'ssserver'
ss_config = kcpss_dir + os.sep + 'shadowsocks.json'
ss_port = 8388
kcp_statu_process_name = 'kcpclient'
ss_statu_process_name = 'ssserver'


class KCPSS:
    def __init__(self, kcp_client, ss_client,
            ss_config, kcp_statu_process_name,
            ss_statu_process_name,
            ss_port):
        self.kcp_client = kcp_client
        self.ss_client = ss_client
        self.ss_config = ss_config
        self.ss_port = ss_port
        self.kcp_statu_process_name = kcp_statu_process_name
        self.ss_statu_process_name = ss_statu_process_name
        self.get_ip()

    @property
    def status(self):
        if(self.statu(self.kcp_statu_process_name) is False or
                self.statu(self.ss_statu_process_name) is False):
            return False
        else:
            return True

    def statu(self, name):
        '''return True if seafile running,vise versa'''
        process = Popen(['pidof', name], stdout=PIPE)
        output, error = process.communicate()
        if(output == ''):  # no such process,seafile not running
            return False
        else:
            return True

    def get_ip(self):
        process = Popen(['ip','route','list'], stdout=PIPE)
        output, error = process.communicate()
        output = output.decode()  # convert bytes to str
        if(len(output) < 10):
            raise Exception("error getting host ip address")
        else:
            lines = output.split("\n")
            for line in lines:
                items = line.split(" ")
                if(items[0] == 'default'):
                    self.ip = items[2]

    def run(self):
        kcp_command = [self.kcp_client, '-r', self.ip, '-l',
                ":"+self.ss_port, '-mode', 'fast2', '-crypt', 'xor']
        ss_command = [self.ss_client, '-c', self.ss_config]
        if(self.statu(self.kcp_statu_process_name) is True):
            check_call(['killall', self.kcp_statu_process_name])
        if(self.statu(self.ss_statu_process_name) is True):
            check_call(['killall', self.ss_statu_process_name])

        check_call(kcp_command)
        check_call(ss_command)


if __name__ == '__main__':
    CKcpss = KCPSS(kcp_client, ss_client, ss_config,
            kcp_statu_process_name, ss_statu_process_name, ss_port)

    while True:
        if(CKcpss.status is False):
            CKcpss.run()
            time.sleep(60)
