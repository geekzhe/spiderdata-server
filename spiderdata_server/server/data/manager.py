
  
"""
职位分析模块业务代码
"""
from spiderdata_server.db.mongodb_client import MongodbClient
from spiderdata_server.server import helper

DB = MongodbClient()


class zhilian_postion(object):
    def __init__(self):
        pass

    # TODO 前十语言数量排行榜
    def lauage_position_top10(self):
        lauage_count = DB.select_Top10()
        # lauage_post=[]
        return lauage_count
    
     # TODO 工作年限和岗位数量
    def working_year_Jobs_count(self):
        zhilian_working_year_Jobs_count= DB.working_year_Jobs_count()
        return zhilian_working_year_Jobs_count

    # TODO 工作年限和和平均工资
    def working_year_avageSalary(self):
        zhilian_work_year_job_salary = DB.mongo_select_working_years_Jobs_avgsalary()
        return zhilian_work_year_job_salary



    # TODO: 这里写与业务有关的数据库操作方法

    # TODO 学历和岗位数量
    def  eduLevel_JobCount(self):
        zhilian_eduLevel_job_count = DB.eduLevel_level_Job_ount()
        return zhilian_eduLevel_job_count
    
    #  TODO Base education's post wage 基于学历的岗位工资
    def education_avgsalary(self):
        zhilian_edulevle_job_avgsalary = DB.education_avgsalary()
        return zhilian_edulevle_job_avgsalary
    
    
    #  TODO  基于用户选择的的岗位推荐
    def job_recommend(self,conndition):
        perfect_job = DB.job_recommd(conndition)
        job_info = {
            'job_name':perfect_job['python'][0][' jobName'],
            'job_url':perfect_job['python'][0]['jobURL']
        }
        print('-------------------',job_info)
        
        return job_info

