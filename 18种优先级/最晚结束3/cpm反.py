#!/user/bin/env python
# -*- coding:utf-8 -*-


class Cpm(object):
    """初始化属性"""
    def __init__(self, prj):
        # 主目录
        self.prj = prj
        self.job_list = prj.jobs
        self.T = prj.T
        self.res_tops = prj.res_tops
        self.sum_of_jobs = prj.sum_of_jobs
    """计算关键路径，单模式，只有一个工期"""
    def cpm_calculate(self):
        uncompleteds = self.prj.jobs[:]
        sum_of_jobs = len(self.prj.jobs)
        completeds = []
        while len(completeds) != sum_of_jobs:
            # 以下代码确定本次循环可以调度的任务，都加入到候选集和
            candidate_jobs = []
            for job in uncompleteds:
                sucs = job.sucs
                if len(sucs) == 0:
                    candidate_jobs.append(job)
                else:
                    # 先将job的初始状态设为True,用以判断能不能进入candidate_jobs
                    if_sucs_ok = True
                    for job_nb in sucs:
                        # 当job的cpmTime['ifOk']为False时，if_preses_ok也为False
                        if not self.prj.jobs[job_nb].cpmTime['ifOk']:
                            if_sucs_ok = False
                    if if_sucs_ok:
                        candidate_jobs.append(job)
            # 在候选集合中，将可以调度的任务全部调度完成
            for job in candidate_jobs:
                # 获取开始时间
                sucs = job.sucs
                # 若没有紧前工作(紧前活动集合长度为0)，则直接调度(处理第一个虚活动)
                if len(sucs) == 0:
                    job.cpmTime['start'] = 0
                    if job.get_dur() != 0:
                        job.cpmTime['end'] = job.cpmTime['start']+job.modes[0].dur - 1
                    else:
                        job.cpmTime['end'] = job.cpmTime['start']
                    job.cpmTime['ifOk'] = True
                    completeds.append(job)
                    uncompleteds.remove(job)
                    # 终止本次循环（while），开始下一次
                    continue
                # 找到前置任务的最后完成时间(前置任务最大的结束时间)
                start = 0
                for job_nb in sucs:
                    if self.prj.jobs[job_nb].cpmTime['end'] > start:
                        start = self.prj.jobs[job_nb].cpmTime['end']
                # 工期不为0时，开始时间
                if job.get_dur() != 0:
                    job.cpmTime['start'] = start+1
                # 工期为0时，开始时间
                else:
                    job.cpmTime['start'] = start
                # 工期不为0时，结束时间
                if job.get_dur() != 0:
                    job.cpmTime['end'] = job.cpmTime['start']+job.get_dur() - 1
                # 工期为0时，开始时间
                else:
                    job.cpmTime['end'] = job.cpmTime['start']
                job.cpmTime['ifOk'] = True
                completeds.append(job)
                uncompleteds.remove(job)
                # 最终的虚活动
                if len(completeds) == sum_of_jobs:
                    return job.cpmTime['end']

    # 计算关键路径时间（self.T=最后一个活动的最晚完成时间），最晚开始时间，最晚完成时间，总时差
    def float_calculate_0(self):
        # self.T = 给定的最后期限，这里当作没给，取的是上述结束时间
        uncompleteds = self.job_list[:]
        sum_of_jobs = len(self.job_list)
        # completeds = []
        for job in uncompleteds:
            # 将所有活动的初始cpmTime['if_ok']均设为False
            job.cpmTime['ifOk'] = False
        completeds = []
        while len(completeds) != sum_of_jobs:
            candidate_jobs = []
            # 以下代码将那些所有后续任务已经完成的job加入候选集合中
            for job in uncompleteds:
                preses = job.preses
                # 处理最终虚活动
                if len(preses) == 0:
                    candidate_jobs.append(job)
                else:
                    # 将job的初始if_sucs_ok设为True，判断能否进入candidate_jobs
                    if_preses_ok = True
                    for job_nb in preses:
                        # 当job的cpmTime['ifOk']为False时，if_sucs_ok也为False
                        if not self.job_list[job_nb].cpmTime['ifOk']:
                            if_preses_ok = False
                    if if_preses_ok:
                        candidate_jobs.append(job)
            # 以下代码将可以调度的任务全部调度完成
            for job in candidate_jobs:
                # 获取最晚开始时间
                preses = job.preses
                # 处理最终虚活动，若没有紧后工作，则直接调度
                if len(preses) == 0:
                    # self.T取自上述cpm_calculate
                    self.T = job.cpmTime['end']
                    job.cpmTime['lateStart'] = self.T
                    job.cpmTime['lateEnd'] = self.T
                    job.cpmTime['ifOk'] = True
                    completeds.append(job)
                    uncompleteds.remove(job)
                    continue
                # 找到后置任务的最早完成时间
                lateEnd = 10000
                for job_nb in preses:
                    if self.job_list[job_nb].cpmTime['lateStart'] < lateEnd:
                        lateEnd = self.job_list[job_nb].cpmTime['lateStart']-1
                        # 处理工期等于0的情况
                        if self.job_list[job_nb].get_dur() == 0:
                            lateEnd = self.job_list[job_nb].cpmTime['lateStart']
                # 由于在计算最晚开始时间和最晚完成时间时，是倒序推导，那么倒推到第一个job时就有可能会有lateEnd小于0的情况
                if lateEnd < 0:
                    lateEnd = 0
                job.cpmTime['lateEnd'] = lateEnd
                # 当工期不为0时：
                if job.get_dur() != 0:
                    job.cpmTime['lateStart'] = job.cpmTime['lateEnd']-job.get_dur() + 1
                # 当工期为0时：
                else:
                    job.cpmTime['lateStart'] = job.cpmTime['lateEnd']
                # 总时差，TF = LST - EST
                job.cpmTime['float'] = job.cpmTime['lateStart']-job.cpmTime['start']
                job.cpmTime['ifOk'] = True
                completeds.append(job)
                uncompleteds.remove(job)

    """在关键路径计算的基础上，计算任务浮动时间(这里是吧self.T取的最长结束时间，所有活动的工期之和)"""
    def float_calculate_1(self):
        # 这里self.T是所有工期之和
        self.T = 0
        for job in self.job_list:
            self.T = self.T + job.get_dur()
        uncompleteds = self.job_list[:]
        sum_of_jobs = len(self.job_list)
        # completeds = []
        for job in uncompleteds:
            # 将所有活动的初始cpmTime['if_ok']均设为False
            job.cpmTime['ifOk'] = False
        completeds = []
        while len(completeds) != sum_of_jobs:
            candidate_jobs = []
            # 以下代码将那些所有后续任务已经完成的job加入候选集合中
            for job in uncompleteds:
                sucs = job.sucs
                # 处理最终虚活动
                if len(sucs) == 0:
                    candidate_jobs.append(job)
                else:
                    # 将job的初始if_sucs_ok设为True，判断能否进入candidate_jobs
                    if_sucs_ok = True
                    for job_nb in sucs:
                        # 当job的cpmTime['ifOk']为False时，if_sucs_ok也为False
                        if not self.job_list[job_nb].cpmTime['ifOk']:
                            if_sucs_ok = False
                    if if_sucs_ok:
                        candidate_jobs.append(job)
            # 以下代码将可以调度的任务全部调度完成
            for job in candidate_jobs:
                # 获取最晚开始时间
                sucs = job.sucs
                # 处理最终虚活动，若没有紧后工作，则直接调度
                if len(sucs) == 0:
                    # self.T为最后一个活动的最晚结束时间
                    job.cpmTime['lateStart'] = self.T - job.get_dur()
                    job.cpmTime['lateEnd'] = self.T
                    job.cpmTime['ifOk'] = True
                    completeds.append(job)
                    uncompleteds.remove(job)
                    continue
                # 找到后置任务的最早完成时间
                lateEnd = 10000
                for job_nb in sucs:
                    if self.job_list[job_nb].cpmTime['lateStart'] < lateEnd:
                        lateEnd = self.job_list[job_nb].cpmTime['lateStart']-1
                        # 处理工期等于0的情况
                        if self.job_list[job_nb].get_dur() == 0:
                            lateEnd = self.job_list[job_nb].cpmTime['lateStart']
                # 由于在计算最晚开始时间和最晚完成时间时，是倒序推导，那么倒推到第一个job时就有可能会有lateEnd小于0的情况
                if lateEnd < 0:
                    lateEnd = 0
                job.cpmTime['lateEnd'] = lateEnd
                # 当工期不为0时：
                if job.get_dur() != 0:
                    job.cpmTime['lateStart'] = job.cpmTime['lateEnd']-job.get_dur() + 1
                # 当工期为0时：
                else:
                    job.cpmTime['lateStart'] = job.cpmTime['lateEnd']
                # 总时差，TF = LST - EST
                job.cpmTime['float'] = job.cpmTime['lateStart']-job.cpmTime['start']
                job.cpmTime['ifOk'] = True
                completeds.append(job)
                uncompleteds.remove(job)


if __name__ == '__main__':
    print('ok!')
