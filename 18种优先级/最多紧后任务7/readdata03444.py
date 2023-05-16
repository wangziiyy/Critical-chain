#!/user/bin/env python
# -*- coding:utf-8 -*-


# import numpy as np
from job_0 import Job
from mode_0 import Mode
#from cpm_0 import Cpm
from psp_0 import Psp


# 读取磁盘文件
def import_from_psplib(file):
    # 将紧前，工期，资源初始状态设为False，进而判断读取哪一部分数据
    precedence = False
    durations = False
    resources = False
    # 文件对象
    f_obj = open(r'D:\data\data.sm')
    # 读取psplib文件，一行一行的读取，并且用split（）将其分解,用enumerate（）来枚举
    for nb, line in enumerate(f_obj):
        # 将每一行分解，产生一个string列表
        strings = line.rstrip().split()
        if len(strings) > 1:
            if strings[0] == "jobs":
                jobs = []
                res_tops = [0, 0, 0, 0]
                sum_of_jobs = int(strings[4])
                prj = Psp(sum_of_jobs, jobs, res_tops)
            # 当precedence为True时，生成紧前信息
            if precedence:
                # 活动序号
                job_nb = int(strings[0])-1
                # 紧后活动集合
                sucs = []
                modes = []
                for ss in strings[3:]:
                    sucs.append(int(ss)-1)
                # 经过Job产生一个个job，再将job放到jobs中去
                job = Job(job_nb, sucs, modes)
                jobs.append(job)
                # 更新状态，表示读取完成
                if job_nb == prj.sum_of_jobs-1:
                    precedence = False
                continue
            # 当durations为True时，生成工期和所使用资源信息
            elif durations:
                job_nb = int(strings[0])-1
                # 工期
                dur = int(strings[2])
                # 资源（四种可更新资源）
                reses = list()
                for re in strings[3:]:
                    reses.append(int(re))
                # 经过Mode产生mode，再将mode放到modes中去，只为了将reses生成
                modes = jobs[job_nb].modes
                mode = Mode(job_nb, dur, reses)
                modes.append(mode)
                if job_nb == prj.sum_of_jobs - 1:
                    durations = False
            # 当resources为True时，生成资源可用量信息
            elif resources:
                for number, k in enumerate(strings):
                    prj.res_tops[number] = int(k)
                f_obj.close()
                return prj
            elif strings[1] == "#modes":
                precedence = True
            elif strings[1] == "mode":
                durations = True
            elif strings[0] == 'R' and strings[1] == '1':
                resources = True
    return prj


if __name__ == '__main__':
    psp1 = import_from_psplib(r'D:\data\data.sm')
    jobs = psp1.jobs
    print('资源情况:', psp1.res_tops)
    # 输出活动序号，工期，资源使用量
    for job in jobs:
        for mode in job.modes:
            print('job_nb:', job.nb, ' dur: ', mode.dur, ' reses:', mode.reses)
    print('\n')
    # 资源紧前关系
    psp1.set_job_preses()
    print('以下测试紧前关系的情况：')
    for job in jobs:
        print('job_nb:', job.nb, ' preses:', job.preses)
        print('len:',len(job.preses))
    print('\n')
    print('以下测试紧后关系情况')
    for job in jobs:
        print('job_nb:', job.nb, ' sucs:', job.sucs)
    print('\n')
    cpm = Cpm(psp1)
    cpm.cpm_calculate()
    print('一下输出各个活动的最早开始时间，最早结束时间:')
    for job in jobs:
        print('job_nb:', job.nb, ' start:', job.cpmTime['start'], ' end:', job.cpmTime['end'])
    print('\n')
    # self.T = 最后一个活动的最晚完成时间
    cpm.float_calculate_0()
    print('工期上限：')
    print('项目最迟工期：', cpm.T)
    for job in jobs:
        print('job_nb:', job.nb, ' start:', job.cpmTime['start'], ' lateStart:', job.cpmTime['lateStart'],
              ' float:', job.cpmTime['float'], 'lateEnd:', job.cpmTime['lateEnd'])
    print('\n')
    # self.T为所有活动工期之和
    cpm.float_calculate_1()
    print('输出最迟时间计算结果（工期上限）')
    print('项目最迟工期：', cpm.T)
    for job in jobs:
        print('job_nb:', job.nb, ' start:', job.cpmTime['start'], ' lateStart:', job.cpmTime['lateStart'],
              ' float:', job.cpmTime['float'], 'lateEnd:', job.cpmTime['lateEnd'])
    print('\n')    