#!/usr/bin/env python
#-*-coding: utf-8 -*-

#-----------------------------------------------------------------
# including the controller of seafile and xunlei services
# for orangepi
#-----------------------------------------------------------------

from subprocess import Popen,PIPE
import os
import time
# seafile parameters
seafile_dir = '/media/u-sda1/yuzi/seafile-server-latest'
seafile_script = 'seafile.sh'
seahub_script = 'seahub.sh'
seafile_statu_process_name = 'seafile-controller'
seafile_user = 'orangepi' #seafile must be run by the owner of seafile-data dir

# xunlei parameters
xunlei_dir = '/home/orangepi/xunlei'
xunlei_bin = 'portal'
xunlei_statu_process_name =  'ETMDaemon'

class Seafile:
    def __init__(self,seafile_dir,seafile_script,seahub_script,\
            statu_process_name,run_as_user=None):
        self.dir = seafile_dir
        self.seafile = self.dir + os.sep + seafile_script
        self.seahub = self.dir + os.sep + seahub_script
        self.statu_process_name = statu_process_name
        self.user = run_as_user

    @property
    def status(self):
        '''return True if seafile running,vise versa'''
        process = Popen(['pidof',self.statu_process_name],stdout=PIPE)
        output,error = process.communicate()
        if(output == ''): #no such process,seafile not running
            return False
        else:
            return True

    def run(self,command):
        seafile_command = self.seafile + ' ' + command
        seahub_command = self.seahub + ' ' + command
        if(self.user != None):
            seafile_command = 'su '+self.user+' -c '+"\""+seafile_command+"\""
            seahub_command = 'su '+self.user+' -c '+"\""+seahub_command+"\""
	print(">>>seafile:"+seafile_command)
	print(">>>seahub:"+seahub_command)
        os.system(seafile_command)
        os.system(seahub_command)


    def start(self):
        self.run('start')

    def stop(self):
        self.run('stop')

    def restart(self):
        self.run('restart')

class Xunlei:
    def __init__(self,xunlei_dir,xunlei_bin,statu_process_name):
        self.bin = xunlei_dir + os.sep + xunlei_bin
        self.statu_process_name = statu_process_name

    @property
    def status(self):
        '''return True if xunlei is runing, vise versa'''
        process = Popen(['pidof',self.statu_process_name],stdout=PIPE)
        output,error = process.communicate()

        if(output == ''):
            return False
        else:
            return True

    def start(self):
        os.system(self.bin)

    def stop(self):
        os.system(self.bin + ' -s')

    def restart(self):
        if(self.status==True):
            self.stop()
            self.start()
        else:
            print('xunlei is not running')

if __name__ == '__main__':
    print('ha')
    CSeafile = Seafile(seafile_dir,seafile_script,seahub_script,\
            seafile_statu_process_name)

    while True:
        if(CSeafile.status == False):
            CSeafile.start()
            time.sleep(5)
