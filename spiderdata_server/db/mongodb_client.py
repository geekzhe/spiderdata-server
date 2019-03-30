import re
from bson import Regex

from pymongo import MongoClient
from spiderdata_server.etc import settings as CONF
from spiderdata_server.server import helper

"""
1. 语言排行榜前１０　就业岗位柱状图
2. 岗位工作地点柱状图
    postion_
3. 基于工作年限的岗位平均工资　
db.zhilian_python_BJ.aggregate({$group:{_id:{工作年限:'$workExperience',薪资范围:'$salary'},数量:{$sum:1}}})



> db.zhilian_python_BJ.aggregate({$group:{_id:'$workExperience'})

4. 岗位学历　岗位数量分布
> db.zhilian_python_BJ.aggregate({$group:{_id:{'eduLevel'},"count":{$sum:1}})


5. 基于学历的岗位平局薪资
db.zhilian_python_BJ.aggregate({$group:{_id:{工作年限:'$eduLevel',薪资范围:'$salary'},数量:{$sum:1}}})

6. 
"""
class MongoBase(object):
    """数据库操作基本类，包含与业务无关的数据库操作方法"""
    def __init__(self):
        self.host = CONF.Mongo_HOST
        self.user = CONF.Mongo_USERNAME
        self.port = CONF.Mongo_PORT
        self.passwd = CONF.Mongo_PASSWORD
        self.dbname = CONF.Mongo_DATABASE_NAME
        self.conn = self.connect()

    def connect(self):
        # conn =MongoClient(self.host,self.port)
        # TODO: 需要优化
        conn= MongoClient('127.0.0.1',27017)
        db = conn['zhilian']
        return db





    #  TODO 工作年限和岗位数量
    # > db.zhilian_java_BJ.aggregate({$group:{_id:'$workExperience',num:{$sum:1}}})
    def mongo_select_working_year_Jobs_count(self):
        lauage_name = {'python':'zhilian_python_BJ','java':'zhilian_java_BJ'}
        job_count = {}

        for k,v in lauage_name.items():
            count_list=[]   
            cursor = self.connect()[v].aggregate([{"$group":{"_id":"$workExperience","num":{"$sum":1}}}])
            for x in cursor:
                count_list.append(x)
            job_count[k] = count_list
        
        return job_count 


        
    #  TODO 岗位学历　岗位数量分布
    # > db.zhilian_java_BJ.aggregate({$group:{_id:'$eduLevel',num:{$sum:1}}})
    def mongo_select_education_level_Jobs_count(self):
        lauage_name = {'python':'zhilian_python_BJ','java':'zhilian_java_BJ'}
        job_count = {}

        for k,v in lauage_name.items():
            count_list=[]   
            cursor = self.connect()[v].aggregate([{"$group":{"_id":"$eduLevel","num":{"$sum":1}}}])
            for x in cursor:
                count_list.append(x)
            job_count[k] = count_list
        
        return job_count 




# TODO 1. 语言排行榜前10就业岗位数量柱状图
    def mongo_select_Top10(self):
        lauage_name = {'python':'zhilian_python_BJ','java':'zhilian_java_BJ'}
        job_count = {}

        for k,v in lauage_name.items():
            cursor = self.connect()[v].count()
            job_count[k] = cursor

        return job_count 



# TODO: 3. 基于工作年限的岗位平均工资　
# 3. 基于工作年限的岗位平均工资　
# db.zhilian_python_BJ.aggregate({$group:{_id:{工作年限:'$workExperience',薪资范围:'$salary'},数量:{$sum:1}}})
    def mongo_select_working_years_Jobs_avgsalary(self):
        lauage_name = {'python':'zhilian_python_BJ','java':'zhilian_java_BJ'}
        work_avgsalary= {}

        for k,v in lauage_name.items():
            count_list=[]   
            cursor = self.connect()[v].aggregate([{"$group":{"_id":{"work_years":"$workExperience","salary":"$salary"},"count":{"$sum":1}}}])
            # cursor = self.connect()[v].aggregate([{"$group":{"_id":"$workExperience","count":{"$sum":1}}}])
            # print(cursor)
            for x in cursor:
                count_list.append(x)
            work_avgsalary[k] = count_list
        
        return work_avgsalary



#  TODO 5. 基于学历的岗位平局薪资
# db.zhilian_python_BJ.aggregate({$group:{_id:{工作年限:'$eduLevel',薪资范围:'$salary'},数量:{$sum:1}}})
    def mongo_select_education_level_Jobs_avgsalary(self):
        lauage_name = {'python':'zhilian_python_BJ','java':'zhilian_java_BJ'}
        edu_avgsalary= {}

        for k,v in lauage_name.items():
            count_list=[]   
            cursor = self.connect()[v].aggregate([{"$group":{"_id":{"education":"$eduLevel","salary":"$salary"},"count":{"$sum":1}}}])
            # cursor = self.connect()[v].aggregate([{"$group":{"_id":"$workExperience","count":{"$sum":1}}}])
            # print(cursor)
            for x in cursor:
                count_list.append(x)
            edu_avgsalary[k] = count_list
        
        return edu_avgsalary    
    

#  TODO 基于用户选择的岗位推荐
# db.zhilian_python_BJ.find({responsibility:{$regex:/python+.+css+/,$options:'i'}}).count()

    def choose_user_job_recommend(self,conditon):
        lauage_name = {'python':'zhilian_python_BJ','java':'zhilian_java_BJ'}
        user_chose_recommed_jobs= {}
        paremt = re.compile(conditon)
        regex  =Regex.from_native(paremt)
        regex.flags = re.UNICODE
        
        for k,v in lauage_name.items():
            cursor =self.connect()[v].find({"responsibility":{"$regex":regex,"$options":"i"}})
            for x in cursor:
                count_list=[]   
            # cursor = self.connect()[v].find({'responsibility':{'$regex':'/'conditon'+/','$options':'i'}})
                count_list.append(x)
            user_chose_recommed_jobs[k] = count_list
        print(user_chose_recommed_jobs)
        
        return user_chose_recommed_jobs
    




class MongodbClient(MongoBase):
    """与业务有关的数据库操作方法类"""
    def __init__(self):
        # TODO: 从配置文件读取数据库连接信息
        # host = CONF.Mongo_HOST
        # user = CONF.Mongo_USERNAME
        # passwd = CONF.Mongo_PASSWORD
        # dbname = CONF.Mongo_DATABASE_NAME
        super().__init__()
    
    # TODO 前十名语言工作岗位数量
    def select_Top10(self):
        zhilian_lauage_Top10 = self.mongo_select_Top10()
        return zhilian_lauage_Top10
        
    

    # TODO 工作年限和岗位数量
    def working_year_Jobs_count(self):
        zhilian_working_yearAndJobs_count= self.mongo_select_working_year_Jobs_count()

        return zhilian_working_yearAndJobs_count



   
    # TODO: 这里写与业务有关的数据库操作方法

    # TODO 学历和岗位数量
    # > db.zhilian_java_BJ.aggregate({$group:{_id:'$eduLevel',num:{$sum:1}}})
    def  eduLevel_level_Job_ount(self):
        zhilian_endcation_level_job_count = self.mongo_select_education_level_Jobs_count()
        
        return zhilian_endcation_level_job_count
        
        


    #  TODO Base education's post wage 基于学历的岗位工资
    def education_avgsalary(self):
        zhilian_endcation_level_job_avgsalary = self.mongo_select_education_level_Jobs_avgsalary()
        return zhilian_endcation_level_job_avgsalary
        


    #  TODO  基于用户选择的的岗位推荐
    def job_recommd(self,condition):
        condition_user = self.choose_user_job_recommend(condition)
        # print('manage－－－－－－－－－－－－－－－－－－－－－',condition_user)
        return condition_user




    


# moncli = MongodbClient()
# print(moncli.mongo_select_working_years_Jobs_avgsalary())