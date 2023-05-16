#!/user/bin/env python
# -*- coding:utf-8 -*-

"""活动类：包含模式，紧前活动集合，紧后活动集合，每个活动的关键路径时间"""


class Job(object):
    """类属性"""
    def __init__(self, nb, sucs, modes):
        self.nb = nb
        self.sucs = sucs
        self.modes = modes
        self.preses = []
        self.runMode = 0
        self.start = 0
        self.end = 0
        self.cpmTime = {'start': 0, 'end': 0, 'ifOk': False, 'float': 0, 'lateStart': 0, 'lateEnd': 0}
        '''
        Constructor
        '''
    def set_modes(self, modes):
        self.modes = modes

    # 紧后集合
    def set_sucs(self, sucs):
        self.sucs = sucs
        return sucs

    # 工期
    def get_dur(self):
        return self.modes[0].dur
