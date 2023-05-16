# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:34:23 2023

@author: 王美美
"""

#!/user/bin/env python
# -*- coding:utf-8 -*-

"""活动的优先级规则：（0）min 最早开始时间(EST)，(1)min 最早完成时间(EFT)，(2)min 最晚开始时间(LST)，
(3)min 最晚完成时间(LFT)
基于关键路线的优先级规则是在任务集合中选择任务，因此函数对象均为candidate_jobs"""

# from job import Job
# from psp import Psp
from readdata03444 import *
from cpm反 import Cpm


class ActRules(object):
    def __init__(self, prj):
        # cpm通过self将prj的res_tops\job_list传递给它
        self.prj = prj
        self.jobs = self.prj.jobs
        self.res_tops = self.prj.res_tops

    # （0）min 开始时间
    def EST(self, candidate_jobs):
        global selected
        t = 1000
        for job in candidate_jobs:
            if job.cpmTime['start'] < t:
                t = job.cpmTime['start']
                selected = job
        return selected

    # （1）min 结束时间
    def EFT(self, candidate_jobs):
        t = 1000
        for job in candidate_jobs:
            if job.cpmTime['end'] < t:
                t = job.cpmTime['end']
                selected = job
        return selected

    # （2）min 最晚开始时间
    def LST(self, candidate_jobs):
        t = 10000
        for job in candidate_jobs:
            if job.cpmTime['lateStart'] < t:
                t = job.cpmTime['lateStart']
                selected = job
        return selected

    # （3）min 最晚完成时间
    def LFT(self, candidate_jobs):
        t = 1000
        for job in candidate_jobs:
            if job.cpmTime['lateEnd'] < t:
                t = job.cpmTime['lateEnd']
                selected = job
        return selected

    # （4） min 最小延迟（总时差）
    def MSLK(self, candidate_jobs):
        t = 1000
        for job in candidate_jobs:
            if job.cpmTime['lateStart'] - job.cpmTime['start'] < t:
                t = job.cpmTime['lateStart'] - job.cpmTime['start']
                selected = job
        return selected

    # (5)min 最小自由时差（FF = 活动j的紧后活动min{ES} - EFj）
    def MFF(self, candidate_jobs):
        # global selected
        ff = []
        for job in candidate_jobs:
            # 处理虚活动（结束）
            if len(job.preses) == 0:
                ff.append({'job': job, 'ff_val': 1000})
                # print('job_nb:', job.nb, 'ff_val:', 1000)
            else:
                # 找出紧后活动中最小的EST
                est = 1000
                for nb in job.preses:
                    if self.jobs[nb].cpmTime['start'] < est:
                        est = self.jobs[nb].cpmTime['start']
                # 做差，加入ff列表中
                ff_val = est - job.cpmTime['end']
                ff.append({'job': job, 'ff_val': ff_val})
                # 输出结果（没有最后一个虚活动的）,判断结果
                # print('job_nb:', job.nb, 'est:', est)
                # print('job_nb:', job.nb, 'end:', job.cpmTime['end'])
                # print('job_nb:', job.nb, 'ff_val:', ff_val)
        # 在集合中选择差值小的活动
        ff_val = 10000
        for p in ff:
            if p['ff_val'] < ff_val:
                ff_val = p['ff_val']
                selected = p['job']
        return selected

    # (6)min 最小安全时差（SF = LSj - j的紧前活动的最大最晚结束时间LF）
    def MSF(self, candidate_jobs):
        # global selected
        msf = []
        for job in candidate_jobs:
            # 处理第一个虚活动
            if len(job.sucs) == 0:
                msf.append({'job': job, 'msf_val': 1000})
                # print('job_nb:', job.nb, 'msf_val:', 1000)
            else:
                lft = 0
                # 找紧前活动得最大最晚结束时间
                for nb in job.sucs:
                    if self.jobs[nb].cpmTime['lateEnd'] > lft:
                        lft = self.jobs[nb].cpmTime['lateEnd']
                # 做差，并且将值加入msf
                msf_val = job.cpmTime['lateStart'] - lft
                msf.append({'job': job, 'msf_val': msf_val})
                # 输出结果（没有第一个虚活动的），判断结果
                # print('job_nb:', job.nb, 'lateStart:', job.cpmTime['lateStart'])
                # print('job_nb:', job.nb, 'lft:', lft)
                # print('job_nb:', job.nb, 'msf_val:', msf_val)
        # 在集合中选择差值小的
        msf_val = 10000
        for p in msf:
            if p['msf_val'] < msf_val:
                msf_val = p['msf_val']
                selected = p['job']
        return selected

    # （7）max 最多紧后任务
    def MIS(self, candidate_jobs):
        lenth = 0
        selected = candidate_jobs[0]
        for job in candidate_jobs:
            if len(job.preses) > lenth:
                lenth = len(job.preses)
                selected = job
        return selected

    # （8）min 最小资源总需求量(candidate_jobs里面是否有第一个需活动
    def SRD(self, candidate_jobs):
        srd = []
        for job in candidate_jobs:
            sum_reses = sum(re for re in job.modes[0].reses)
            srd.append({'job': job, 'sum_reses': sum_reses})
            # 输出每个活动的总资源需求量，判断结果
            # print('job_nb:', job.nb, 'sum_reses;', sum_reses)
        # candidate_jobs中每个活动的最大资源已经找到，再在里面选资源最多的那个活动
        val = 1000
        for p in srd:
            if p['sum_reses'] < val:
                val = p['sum_reses']
                selected = p['job']
        return selected

    # （9）max 最大资源总需求量(工期*资源需求总量)
    def GRD(self, candidate_jobs):
        grd = []
        # 先找出三种模式的资源量，以字典放在grd空列表里面
        for job in candidate_jobs:
            sum_reses = sum(re for re in job.modes[0].reses)
            dur_reses = sum_reses*job.modes[0].dur
            grd.append({'job': job, 'dur_reses': dur_reses})
            # 打印出结果
            # print('job_nb:', job.nb, 'dur_reses:', dur_reses)
        # candidate_jobs中每个活动的最大资源已经找到，再在里面选资源最多的那个活动
        val = -1
        for p in grd:
            if p['dur_reses'] > val:
                val = p['dur_reses']
                selected = p['job']
        return selected

    # （10）max 最大资源利用量（资源需求总量）
    def GRU(self, candidate_jobs):
        global selected
        gru = []
        for job in candidate_jobs:
            sum_reses = sum(re for re in job.modes[0].reses)
            gru.append({'job': job, 'sum_reses': sum_reses})
            # 打印结果
            # print('job_nb:', job.nb, 'sum_reses:', sum_reses)
        # -1将最后一个虚活动包括进来
        val = -1
        for p in gru:
            # 这里单独用小于号，就保证了在选择时选择序号小的那个job
            if p['sum_reses'] > val:
                val = p['sum_reses']
                selected = p['job']
        return selected

    # (11）max 最高排列位置权重：当前工期+直接紧后活动工期总和
    def GRPW(self, candidate_jobs):
        grpw = []
        for job in candidate_jobs:
            # 处理最后一个虚活动
            if len(job.preses) == 0:
                grpw.append({'job': job, 'dur_sum': 0})
                # print('job_nb:', job.nb, 'dur_sum:', 0)
            else:
                sum_dur_sum = 0
                for nb in job.preses:
                    # 紧后活动工期总和
                    sucs_dur_sum = self.jobs[nb].modes[0].dur + sum_dur_sum
                # 当前job的工期与其紧后活动工期求和
                dur_sum = job.modes[0].dur + sucs_dur_sum
                grpw.append({'job': job, 'dur_sum': dur_sum})
                # 打印，输出结果
                # print('job_nb:', job.nb, 'dur_sum:', dur_sum)
        # 选择工期和最大的活动
        # 取-1是想吧最后一个虚活动考虑在内
        val = -1
        for p in grpw:
            if p['dur_sum'] > val:
                val = p['dur_sum']
                selected = p['job']
        return selected

    # （12）min 后续工作平均机动时间(最晚开始时间-最早开始时间）/工作j的所有后序工作的集合
    def LFS(self, candidate_jobs):
        # 将活动序号与后序工作平均机动时间存储到lfs{}字典
        lfs = []
        lenth = {}
        for job in candidate_jobs:
            if len(job.preses) == 0:
                # 这个优先级规则找最小的，可以将最后一个活动设为1000，选不到最后一个活动
                lfs.append({'job': job, 'lfs': 1000})
                # print('job_nb:', job.nb, 'lfs:', 1000)
            # 找出job所有的后序工作集合的长度
            else:
                set_0 = 0
                for job_0 in job.preses:
                    set_0 = len(self.jobs[job_0].preses) + set_0
                set_1 = set_0+len(job.preses)
                # print('job_nb', job.nb, 'set_lenth', set_1)
                lenth[job.nb] = 1/set_1
                # print('job_nb', job.nb, 'lenth', lenth[job.nb])
                # 所有活动的【最晚开始时间】，【最早开始时间】在cpm.float_calculate()中产生
                TF = job.cpmTime['lateStart'] - job.cpmTime['start']
                avg = TF * lenth[job.nb]
                # 将一个个结果以字典的形式加入列表
                lfs.append({'job': job, 'lfs': avg})
                # 打印出结果，直观判断结果是否正确
                # print('job_nb:', job.nb, 'lfs:', avg)
        # 初始值设为10000，将最后一个虚活动包含
        s = 10000
        for p in lfs:
            # 这里单独用小于号，就保证了在选择时选择序号小的那个job
            if p['lfs'] < s:
                s = p['lfs']
                selected = p['job']
        return selected

    # （13）max 加权资源利用率和紧前关系(0.7*job的紧后工作集合数+0.3（求和[job对k资源的需求量/k资源可用量]）可更新资源)
    # 怎么找各种资源在该阶段的可用量是关键
    def WRUP(self, candidate_jobs):
        wrup = []
        global selected
        for job in candidate_jobs:
            set_number = 0.7*len(job.preses)
            reses_0 = 0
            # 四种可更新资源
            for i in range(len(self.prj.res_tops)):
                # job.modes[0].reses是活动的需求量，self.prj.res_tops是资源总量
                reses_0 = job.modes[0].reses[i]*(1/(self.prj.res_tops[i])) + reses_0
            reses_f = 0.3*reses_0
            wrup_val = set_number + reses_f
            wrup.append({'job': job, 'wrup_val': wrup_val})
            # 打印活动序号、wrup_val值进行判断
            print('job_nb', job.nb, 'wrup_val:', wrup_val)
        # 在活动集合中选择目标值最大的活动
        val = -1
        for p in wrup:
            if p['wrup_val'] > val:
                val = p['wrup_val']
                selected = p['job']
        return selected

    # （14）max 最多后序任务（包括直接紧后任务和间接后序任务）
    def MTS(self, candidate_jobs):
        mts = []
        for job in candidate_jobs:
            if len(job.preses) == 0:
                mts.append({'job': job, 'set_lenth': 0})
                # print('job_nb:', job.nb, 'set_lenth:', 0)
            # 后序任务数初始值为job的紧后任务数
            set_lenth = len(job.preses)
            # job的紧后任务的紧后任务为job的后序任务，求后序任务的和
            for job_0 in job.preses:
                set_lenth = len(self.jobs[job_0].preses) + set_lenth
                # 将任务和后续任务的和以字典的形式加入上述列表中
                mts.append({'job': job, 'set_lenth': set_lenth})
            # 打印出任务序号、后序任务的和
                print('job_nb:', job.nb, 'set_lenth:', set_lenth)
        val = -1
        for p in mts:
            if p['set_lenth'] > val:
                val = p['set_lenth']
                selected = p['job']
        return selected

    # (15) min 最小总资源稀缺度TRS（job对k资源的需求量÷k资源总量，再求和）
    def TRS(self, candidate_jobs):
        trs = []
        for job in candidate_jobs:
            reses_d = 0
            for i in range(len(self.prj.res_tops)):
                reses_d = job.modes[0].reses[i]*(1/(self.prj.res_tops[i])) + reses_d
            trs.append({'job': job, 'reses_d': reses_d})
            # 打印输出结果，检查结果
            # print('job_nb:', job.nb, 'reses_d:', reses_d)
        val = 1000
        for p in trs:
            # 这里取小于号，就是按顺序去的任务，默认选择序号最小的开始
            if p['reses_d'] < val:
                val = p['reses_d']
                selected = p['job']
        return selected

    # (16) min 最短工期
    def SPT(self, candidate_jobs):
        dur = 1000
        for job in candidate_jobs:
            if job.modes[0].dur < dur:
                dur = job.modes[0].dur
                selected = job
        return selected

    # (17) max 最长工期
    def LPT(self, candidate_jobs):
        global selected
        dur = -1
        for job in candidate_jobs:
            if job.modes[0].dur > dur:
                dur = job.modes[0].dur
                selected = job
        return selected

    # (18) max 修正的WRUP（—加权资源利用率和紧前关系）方法(WACRU)，这里α取值为1，w 取值依然为0.7
    def WACRU(self, candidate_jobs):
        wacru = []
        for job in candidate_jobs:
            # 处理一下最后一个虚活动的情况，将它加入wacru，且它的值为0（因为是选择优先级值最大的，把最后一个活动的优先级值设为0）
            if len(job.preses) == 0:
                wacru_0 = 0
                wacru.append({'job': job, 'wacru_val': wacru_0})
                # print('job_nb:', job.nb, 'wacru_val:', wacru_0)
            else:
                gi_0 = 0
                for job_0 in job.preses:
                    # 1/(1+jobs[job_0].cpmTime['float'])即为F（*），val即为Gi
                    # jobs[job_0]这里的job应该是所有的jobs，而不是所说的candidate_jobs
                    float_val = self.jobs[job_0].cpmTime['float']
                    gi_0 = 1/(1+float_val) + gi_0
                # 打印该活动的任务序号、Gi值
                gi = 0.7 * gi_0
                # print('job_nb:', job.nb, 'Gi:', gi)
                reses_d = 0
                for i in range(len(self.prj.res_tops)):
                    reses_d = job.modes[0].reses[i] * (1 / (self.prj.res_tops[i])) + reses_d
                resource_use = 0.3 * reses_d
                wacru_val = gi + resource_use
                wacru.append({'job': job, 'wacru_val': wacru_val})
                # 打印活动序号、wacru_val进行结果判断
                # print('job_nb:', job.nb, 'wacru_val:', wacru_val)
        # 在活动集合中选择目标值最大的活动
        val = -1
        for p in wacru:
            if p['wacru_val'] > val:
                val = p['wacru_val']
                selected = p['job']
        return selected    
    
