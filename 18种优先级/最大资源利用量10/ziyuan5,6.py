import pandas as pd
import ast


class Activity:
    def __init__(self, name, start_time, end_time, resources):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.resources = resources
        
class ResourcePool:
    def __init__(self):
        # 获取资源数量
        resource1 = psp1.res_tops[0]
        resource2 = psp1.res_tops[1]
        resource3 = psp1.res_tops[2]
        resource4 = psp1.res_tops[3]
        final_dict = {
            "resource1": resource1,
            "resource2": resource2,
            "resource3": resource3,
            "resource4": resource4,
            "activity_name": "init_resource"
        }
        self.resource_list = [final_dict]
        print(self.resource_list)
    def add_resource(self, resource_type, resource_count, activity_name):
        #遍历资源池，如果已经存在该活动的该类型资源，则增加该类型资源的数量
        for resource in self.resource_list:
            if resource.get("activity_name") == activity_name and resource.get(resource_type):
                resource[resource_type] += resource_count
                return
        #如果不存在该活动的该类型资源，则添加该类型资源
        self.resource_list.append({resource_type: resource_count, "activity_name": activity_name})
    def get_activity_resource(self, resource_type, resource_count):
        #获取所有可用的该类型资源
        jobs = psp1.jobs
        activity_list = []
        for job_dict in job_dicts:
            job = jobs[job_dict['job_nb']]
            activity = {
                "name": f"activity{job.nb}",
                "sum_reses": job_dict['sum_reses']
            }
            activity_list.append(activity)
        activity_list_sorted = sorted(activity_list, key=lambda x: x['sum_reses'], reverse = True)
# 将排序后的活动名称存入列表中
        priority_list = ['init_resource'] + [activity['name'] for activity in activity_list_sorted]
        print('优先级：',priority_list)
        available_resource = []
        for resource in self.resource_list:
            if resource.get(resource_type):
                available_resource.append(resource)
        #如果没有可用的该类型资源，则返回None critical chain
        if not available_resource:
            return None
        sorted_resource = sorted(available_resource, key=lambda x: priority_list.index(x['activity_name']))
        print('可用资源',sorted_resource)  # 打印排序后的列表
        #遍历所有可用的该类型资源，如果该资源数量足够，则减少该资源数量并返回该资源信息
        for resource in sorted_resource:
            if resource.get(resource_type) >= resource_count:
                resource[resource_type] -= resource_count
                return {"resource_type": resource_type, "resource_count": resource_count, "activity_name": resource.get("activity_name")}
            #如果该资源数量不够，则减少该资源数量并继续遍历下一个资源
            else:
                resource_count -= resource[resource_type]
                resource[resource_type] = 0
        #如果所有可用的该类型资源都不够，则返回None
        return None
    
    
def convert_reses(x):
    try:
        return tuple(ast.literal_eval(x))
    except (ValueError, SyntaxError):
        return x
# 读取 excel 文件并指定 converters 参数
df = pd.read_excel('output.xlsx', converters={'reses': convert_reses})
# 转换为字典
data = df.to_dict(orient='records')
# 创建 activity 列表
activities = []
activity_list = []
# 遍历字典并创建 activity
for item in data:
    name = f"activity{item['job_nb']}"
    start_time = item['start']
    end_time = item['end']
    resources = {
        f"resource{i+1}": item['reses'][i] for i in range(4) if item['reses'][i] != 0
    }
    activity = {
        "name": name,
        "start_time": start_time,
        "end_time": end_time,
        "resources": resources
    }
    activities.append(activity)
    activity_list.append(activity)
# 将所有活动按照开始时间排序
activity_list.sort(key=lambda x: (x["start_time"]))


# 定义资源池
resource_pool = ResourcePool()
# 遍历每个时刻
for i in range(activity_list[-1]["end_time"] + 2):
    # 输出资源池的情况
    print("Time:", i)
    print("Resource pool:", resource_pool.resource_list)
    
    # 遍历所有活动
    for activity in activity_list:
        if activity["start_time"] == i:
            selected_resource = None
            for resource_type, resource_count in activity["resources"].items():
                resource = resource_pool.get_activity_resource(resource_type, resource_count)
                if resource is None:
                    break
                if selected_resource is None:
                    selected_resource = resource
                else:
                    selected_resource[resource_type] = resource_count
                    selected_resource["activity_name"] += ", " + resource["activity_name"]
            if selected_resource is None:
                print("Activity", activity["name"], "cannot start due to insufficient resources")
            else:
                print("Activity", activity["name"], "starts")
            print("Resource pool:", resource_pool.resource_list)
        # 如果当前时刻是活动的结束时刻，释放所占用的资源
        elif activity["end_time"] == i:
            for resource_type, resource_count in activity["resources"].items():
                resource_pool.add_resource(resource_type, resource_count, activity["name"])
            print("Activity", activity["name"], "ends")
            print("Resource pool:", resource_pool.resource_list)
            