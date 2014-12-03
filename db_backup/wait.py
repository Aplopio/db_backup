from __future__ import print_function
import time


def wait_for(condition, while_wating=None, interval=2, args=[]):
    time_taken = 0
    while condition(*args):
        time.sleep(interval)
        time_taken += interval
        if time_taken % 60 == 0:
            print()
            print('Has waited for', time_taken/60, 'm')
        else:
            print('.', sep='', end='')
        if while_wating:
            args = while_wating(*args)
