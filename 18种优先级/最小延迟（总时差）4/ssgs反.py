#!/user/bin/env python
# -*- coding:utf-8 -*-


import random
# import ind
import sys
from job_0 import Job
from mode_0 import Mode
from psp_0 import Psp
from readdata03444 import import_from_psplib
from cpm反 import Cpm
from actrules反 import ActRules
#import openpyxl
#from openpyxl import load_workbook
#from nfp import NFP


class SSGS(object):
    def __init__(self, prj):
        self.prj = prj
        self.T = self.prj.T
        self.jobs = self.prj.jobs
        self.resline_0 = self.prj.resline_0
        self.resline_1 = self.prj.resline_1
        self.resline_2 = self.prj.resline_2
        self.resline_3 = self.prj.resline_3
        # self.resline_0 = [self.prj.res_tops[0]] * (self.T + 1)
        # self.resline_1 = [self.prj.res_tops[1]] * (self.T + 1)
        # self.resline_2 = [self.prj.res_tops[2]] * (self.T + 1)
        # self.resline_3 = [self.prj.res_tops[3]] * (self.T + 1)

    # 设置资源上限
    def reset_resline(self):
        self.T = self.prj.T
        # 这里*(self.T+1)是指所生成的列表有这么多个元素
        self.resline_0 = [self.prj.res_tops[0]] * (self.T+1)
        self.resline_1 = [self.prj.res_tops[1]] * (self.T+1)
        self.resline_2 = [self.prj.res_tops[2]] * (self.T+1)
        self.resline_3 = [self.prj.res_tops[3]] * (self.T+1)
        # print('self.prj.res_tops:', self.prj.res_tops)
        # print('self.TT:', self.T)
        # print('res0:', self.resline_0)
        # print('res1:', self.resline_1)
        # print('res1:', self.resline_2)
        # print('res1:', self.resline_3)
        return self.resline_0, self.resline_1, self.resline_2, self.resline_3
        #return self.resline_2 ,self.resline_1
    





    def schedule_one(self, job, t_in):
        # 所选择的job的工期
        dur = job.modes[0].dur
        # job初始状态均为可行
        feasible = True
        # 考虑时间延迟和资源约束
        t = t_in
        # 这里range()限定资源水平线的长度
        for t in range(t_in, self.prj.T-dur):
            # 这里range()限定在工期dur内的资源限制，在某一时间段内，时刻tt的资源限低于某一job的资源使用量，返回False
            for tt in range(t, t+dur):
                if self.resline_0[tt] < job.modes[0].reses[0]:
                    feasible = False
                if self.resline_1[tt] < job.modes[0].reses[1]:
                    feasible = False
                if self.resline_2[tt] < job.modes[0].reses[2]:
                    feasible = False
                if self.resline_3[tt] < job.modes[0].reses[3]:
                    feasible = False
            if feasible:
                # 记住这个t，即为下一个job的start，因为是单模式，当为feasible = False时，不用换模式
                break
            if not feasible:
                return False
            sys.exit(0)
        job.start = t
        if dur != 0:
            job.end = t + job.modes[0].dur - 1
        else:
            job.end = job.start
        # 更新调度后的资源水平，减掉用去的资源（在job的工期内）
        for tt in range(job.start, job.end + 1):
            self.resline_0[tt] = self.resline_0[tt] - job.modes[0].reses[0]
            self.resline_1[tt] = self.resline_1[tt] - job.modes[0].reses[1]
            self.resline_2[tt] = self.resline_2[tt] - job.modes[0].reses[2]
            self.resline_3[tt] = self.resline_3[tt] - job.modes[0].reses[3]
            #print('res0:',self.resline_0[tt],job.modes[0].reses[0],tt)
            #print('res1:',self.resline_1[tt],job.modes[0].reses[1],tt)
            #print('res2:',self.resline_2[tt],job.modes[0].reses[2],tt)
            #print('res3:',self.resline_3[tt],job.modes[0].reses[3],tt)
        # print('res0:', self.resline_0)
        # print('res1:', self.resline_1)
        # print('res1:', self.resline_2)
        # print('res1:', self.resline_3)
        return True

    def select_one(self, jobs, act_rule):
        a = ActRules(self.prj)

        # 最开始选择的是虚活动0，活动模式也是0
        global selected
        if act_rule == 4:
            selected = a.EST(jobs)
        elif act_rule == 1:
            selected = a.EFT(jobs)
        elif act_rule == 2:
            selected = a.LST(jobs)
        elif act_rule == 3:
            selected = a.LFT(jobs)
        elif act_rule == 0:
            selected = a.MSLK(jobs)
        elif act_rule == 5:
            selected = a.MFF(jobs)
        elif act_rule == 6:
            selected = a.MSF(jobs)
        elif act_rule == 7:
            selected = a.MIS(jobs)
        elif act_rule == 8:
            selected = a.SRD(jobs)
        elif act_rule == 9:
            selected = a.GRD(jobs)
        elif act_rule == 10:
            selected = a.GRU(jobs)
        elif act_rule == 11:
            selected = a.GRPW(jobs)
        elif act_rule == 12:
            selected = a.LFS(jobs)
        elif act_rule == 13:
            selected = a.WRUP(jobs)
        elif act_rule == 14:
            selected = a.MTS(jobs)
        elif act_rule == 15:
            selected = a.TRS(jobs)
        elif act_rule == 16:
            selected = a.SPT(jobs)
        elif act_rule == 17:
            selected = a.LPT(jobs)
        elif act_rule == 18:
            selected = a.WACRU(jobs)


        else:
            # 随机选择一个job
            job_nb = random.randint(0, len(jobs) - 1)
            selected = jobs[job_nb]
        return selected

    def ssgs(self, act_rule):
        # 初始化资源轴
        self.reset_resline()
        #uncompleteds = self.jobs[31:]
        sum_of_jobs = len(self.prj.jobs)
        completeds = [self.jobs[31]]
        candidate_jobs = []
        candidate_jobs = sorted(candidate_jobs, key=lambda x: x.nb, reverse=True)
        # 打印第一个虚活动的紧后活动
        #print(self.jobs[31].preses)
        df = pd.DataFrame(columns=['job_nb', 'start', 'end','reses'])
        for nb in self.jobs[31].preses:
            # 打印出紧后活动的序号，和它的紧前活动
            #print(' job_nb:', nb, ' preses:', self.jobs[nb].sucs)
            # 如果前置任务只有一个初始任务则加入候选集合
            if len(self.jobs[nb].sucs) == 1:
                candidate_jobs.append(self.jobs[nb])
                candidate_jobs = sorted(candidate_jobs, key=lambda x: x.nb, reverse=True)
                # 打印出这个活动序号
                #print('加入候选集和的活动：', self.jobs[nb].nb)
        while len(completeds) != sum_of_jobs:
            # 打印出candidate_jobs
            candidate_jobs_nb = []
            for job in candidate_jobs:
                candidate_jobs_nb.append(job.nb)
                candidate_jobs = sorted(candidate_jobs, key=lambda x: x.nb, reverse=True)
            #print('候选集合活动:', candidate_jobs_nb)
            # 以下代码选择优先级最高的任务进行调度（在candidate_jobs里面选择一个活动）
            selected = self.select_one(candidate_jobs, act_rule)
            # 确定最高开始时间：前置任务最早完成时间的最大值
            pres_end = 0
            # 第一次候选集合为1，2，3，所以selected必为其中一个，他们的紧前活动都是第一个虚活动
            for nb in selected.sucs:
                # 这里的end哪里来的？（默认为0）
                if self.jobs[nb].end > pres_end:
                    pres_end = self.jobs[nb].end
            # 说明是结束任务，需要特殊对待
            if selected.nb == sum_of_jobs - 32:
                selected.start = pres_end
                selected.end = pres_end
                # 需要加入，不然后面打印没有虚活动信息
                candidate_jobs.remove(selected)
                completeds.append(selected)
                #print(' 最终虚活动：', selected.nb, ' start:', selected.start, ' end:', selected.end)
                start = jobs[0].end - selected.end
                end = jobs[0].end - selected.start
                print('job_nb:', selected.nb,'start:', start , 'end：', end,'reses:',selected.modes[0].reses)
                df.loc[len(df)] = [selected.nb, start, end, selected.modes[0].reses]

                break

            tag = self.schedule_one(selected, pres_end)
            #print('tag:', tag)
            while not tag:
                pres_end = pres_end + 1
                # 这里pres_end即为job的开始时间
                #print('pres_end:', pres_end)
                tag = self.schedule_one(selected, pres_end)
                #print('tag:', tag)
            # 从候选任务中删除
            candidate_jobs.remove(selected)
            # 增加到调度完成集合中
            completeds.append(selected)
            start = dur - selected.end
            end = dur - selected.start
            print('job_nb:', selected.nb,'start:', start , 'end：', end,'reses:',selected.modes[0].reses)
            df.loc[len(df)] = [selected.nb, start, end, selected.modes[0].reses]

            # 从该任务的后续任务中，选择新的候选任务(注意最后一个虚活动有没有进入candidate_jobs)
            for nb_preses in selected.preses:
                can = True
                for nb_sucs in self.jobs[nb_preses].sucs:
                    # 有一个任务没有调度完成
                    if self.jobs[nb_sucs] not in completeds:
                        can = False
                if can:
                    # 说明其前置任务全部调度完成了
                    candidate_jobs.append(self.jobs[nb_preses])
                    candidate_jobs = sorted(candidate_jobs, key=lambda x: x.nb, reverse=True)
        df.to_excel('output.xlsx', index=False)
        return True


if __name__ == '__main__':
    psp1 = import_from_psplib(r'D:\data\data.sm')
    # 单独把jobs提出，便于后面使用
    jobs = psp1.jobs
    # psp1.initialize()
    # 添加入紧前关系
    psp1.set_job_preses()
    # 生成cpmTime——最早开始，最早完成，最晚开始，最晚结束，不会影响job.start和job.end
    # 创建cpm实例
    cpm = Cpm(psp1)
    cpm.cpm_calculate()
    cpm.float_calculate_0()
    #cpm.float_calculate_1()# 产生self.T
    T = psp1.set_T()
    #print('self.T:', T)
    # ********************************************************************************************************
    # 调用优先级规则，生成工期
    sg = SSGS(psp1)
    # 19个优先级规则下的工期
    dur_set = []
    for i in range(1):
        s = sg.ssgs(i)
        #print('s:', s)
        # 共有32个活动，最后一个活动的最后完成日期即为工期
        dur = jobs[0].end
        dur_set.append(dur)
    print('工期集合：', dur_set)
 #   print('data(1)工期完成！')
