#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import subprocess
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)


class Cron:
    def __init__(self, freq_list, log_file):
        '''
        freq_dict in {'daily':[task,task], 'hourly':[xxxx..
        format task is ('name',func) tuple
        '''
        self._freq = freq_list.copy()
        self._fd = self.open_log(log_file)
        self.load_log(self._fd)  # put logs in self.logs dict
        # dict in {'weekly':[(seconds, taskname)],'daily':xxx}

    def run(self):
        week_seconds = 604800 # week translate to seconds
        day_seconds = 86400 # day translate to seconds
        hour_seconds = 3600  # hour translate to seconds
        time_sequence = {'hourly': hour_seconds, 'daily': day_seconds,
                         'weekly': week_seconds}
        if(len(self._freq) != 0):
            time.sleep(600)  # sleep 10min before run
            while True:
                for type, task in self._freq:
                    task_name, func = task
                    last_time = self.logs.get(task_name)
                    task_name = task_name.strip()
                    logging.debug("task {} last run time {}".format(
                        task_name, last_time))
                    logging.debug("has passed {}s from last run task {}".format(
                        time.time()-last_time, task_name))
                    logging.debug("waiting until passed time grow to {}".format(
                        time_sequence[type]))
                    if(last_time is None or time.time() -
                       last_time > time_sequence[type]):
                        # last running time more than one hour, one day or one week
                        logging.info("task {}: {}s passed since last run".format(
                            task_name, time_sequence[type]))
                        func()
                        self.write_log(type, task_name)
                time.sleep(1800)

    def write_log(self, type, task_name):
        self.logs[task_name] = time.time()
        self._fd.write(self.timestr()+'\t'+type+"\t"+task_name+'\n')
        self._fd.flush()

    def timestr(self):
        now = time.localtime(time.time())
        return time.strftime("%Y%m%d%H%M", now)

    def open_log(self, log_file):
        '''
        open log file to read and write, log_file is an
        absolute path contains log file name
        '''
        if(os.path.exists(log_file)):  # already exists
            return open(log_file, 'r+')
        elif(os.path.exists(os.path.dirname(log_file))):
            # create new file
            return open(log_file, 'w')
        else:
            raise Exception("the dir to put log file does not exists")

    def load_log(self, log_fd):
        '''
        log format: date\t type\t task name start running
        obtain last weekly, daily, hourly task running log
        bug self.logs only need the the last running time
        of all tasks
        '''
        self.logs = {}
        while True:  # has content
            line = log_fd.readline()
            if(line == ''):
                break
            datestr, type, task = line.split('\t')
            date = time.strptime(datestr, "%Y%m%d%H%M")
            seconds = time.mktime(date)
            self.logs[task.strip()] = seconds



def run_command(command):
    subprocess.check_call(command)


def btrfsbackup():
    command = ['/usr/local/bin/bakseafile.sh']
    #command = ['ls','/home/huangyu']
    run_command(command)

def test():
    print("test function")

# freq_list item type, (taskname, func)
# type can be hourly daily weekly
freq_list = [('daily', ('btrfsbackup', btrfsbackup)),
            ]
log_file = '/var/log/mycron.log'  # can't be cron.log, it is used by system's cron
cron = Cron(freq_list, log_file)
cron.run()
