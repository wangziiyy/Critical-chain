#!/user/bin/env python
# -*- coding:utf-8 -*-

"""让job和资源使用量联系起来"""


class Mode(object):
    def __init__(self, job_nb, dur, reses):
        self.job_nb = job_nb
        self.dur = dur
        self.reses = reses
