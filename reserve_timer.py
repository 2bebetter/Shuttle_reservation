# -*- coding: utf-8 -*-
# @Date    : 2021/3/25
# @Author  : wmh
from apscheduler.schedulers.blocking import BlockingScheduler

from reserve import UcasBcyy

def reserve_job_8pm():
    bcyy = UcasBcyy("24", u'20:30', u'益园-张仪村')
    bcyy.reserve_shuttle()

def reserve_job_5pm():
    bcyy = UcasBcyy("5", u'17:30', u'益园-张仪村')
    bcyy.reserve_shuttle()

def reserve_schedule():
    sched = BlockingScheduler()
    # Thu, Thu 00:00 reserve shuttle at 8:30pm
    sched.add_job(reserve_job_8pm, 'cron', day_of_week='Tue,Thu', hour='0')
    # Fri 00:00 reserve shuttle at 5:30pm
    sched.add_job(reserve_job_5pm, 'cron', day_of_week='fri', hour='0')

    sched.start()

if __name__ == '__main__':
    reserve_schedule()