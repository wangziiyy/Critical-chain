#!/user/bin/env python
# -*- coding:utf-8 -*-


from cpm反 import Cpm
from job_0 import Job


class Psp(object):
    """类属性"""
    def __init__(self, sum_of_jobs, jobs, res_tops):
        self.sum_of_jobs = sum_of_jobs
        self.jobs = jobs
        self.res_tops = res_tops
        self.T = 0
        self.set_T()
        self.cal_share_res()
        self.baseRes = [0, 0, 0, 0]
        self.upperRes = [0, 0, 0, 0]
        self.resline_0 = []
        self.resline_1 = []
        self.resline_2 = []
        self.resline_3 = []

    # 初始化
    def initialize(self):
        self.set_job_preses()
        self.set_T()
        # self.cpm_cal()
        # self.cal_share_res()
        # 更新res_tops，更新资源上限
        self.res_tops[0] = self.upperRes[0]
        self.res_tops[1] = self.upperRes[1]
        self.res_tops[2] = self.upperRes[2]
        self.res_tops[3] = self.upperRes[3]
        # 以下这行程序生成的是一个列表（toppsp.py）
        # self.res_tops[0] = [self.upperRes[0]]*self.T
        # print('self.res_tops[0]', self.res_tops[0])
        # print('self.res_tops[1]', self.res_tops[1])
        # print('self.res_tops[2]', self.res_tops[2])
        # print('self.res_tops[3]', self.res_tops[3])
        print('res_tops:', self.res_tops)

    def initialize_for_program(self):
        self.res_tops = []
        self.T = 0
        self.set_job_preses()
        self.set_T()
        self.cal_share_res()

    # 在关键路径基础上计算资源上限
    def cpm_cal(self):
        cpm = Cpm(self)
        cpm.cpm_calculate()
        self.upperRes = [0, 0, 0, 0]
        for t in range(self.T):
            # 以下这个for将同时间段的使用资源加起来
            temp = [0, 0, 0, 0]
            for job in self.jobs:
                # 四种资源
                for i in range(4):
                    if job.cpmTime['start'] <= t <= job.cpmTime['end']:
                        temp[i] = temp[i] + job.modes[0].reses[i]
            # 更新upperRes，每种资源上界
            for j in range(4):
                if temp[j] > self.upperRes[j]:
                    self.upperRes[j] = temp[j]
        print('upperRes:', self.upperRes)
        return self.upperRes

    # 设置T
    def set_T(self):
        self.T = 0
        for job in self.jobs:
            self.T = self.T + job.get_dur()
        # cpm = Cpm(self)
        # cpm.cpm_calculate()
        # cpm.float_calculate_0()
        # cpm.float_calculate_1()
        # self.T_L=jobs[len(jobs)-1].cpmTime['lateEnd']
        return self.T

    # 设置紧前活动集合
    def set_job_preses(self):
        # preses=[]
        for job in self.jobs:
            for nb in job.sucs:
                self.jobs[nb].preses.append(job.nb)

    # 计算资源的上下界(按百分比)
    # baseRes即为每个活动所使用资源的最大使用量。upperRes即为每个活动所使用资源的和
    def cal_share_res(self):
        self.baseRes = [0, 0, 0, 0]
        self.upperRes = [0, 0, 0, 0]
        for job in self.jobs:
            tmp = [0, 0, 0, 0]
            for i in range(4):
                tmp[i] = job.modes[0].reses[i]
                if tmp[i] > self.baseRes[i]:
                    self.baseRes[i] = tmp[i]
                self.upperRes[i] = self.upperRes[i] + tmp[i]
        # print('resource0:', self.baseRes[0], self.upperRes[0])
        # print('resource1:', self.baseRes[1], self.upperRes[1])
        # print('resource2:', self.baseRes[2], self.upperRes[2])
        # print('resource3:', self.baseRes[3], self.upperRes[3])
