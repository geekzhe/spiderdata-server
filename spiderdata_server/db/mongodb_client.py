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
db.zhilian_python_BJ.aggregate(
    {$group:{_id:{工作年限:'$workExperience',薪资范围:'$salary'},数量:{$sum:1}}})



> db.zhilian_python_BJ.aggregate({$group:{_id:'$workExperience'})

4. 岗位学历　岗位数量分布
> db.zhilian_python_BJ.aggregate({$group:{_id:{'eduLevel'},"count":{$sum:1}})


5. 基于学历的岗位平局薪资
db.zhilian_python_BJ.aggregate(
    {$group:{_id:{工作年限:'$eduLevel',薪资范围:'$salary'},数量:{$sum:1}}})

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
        conn = MongoClient('127.0.0.1', 27017)
        db = conn['zhilian']
        return db

    #  TODO 工作年限和岗位数量
    # > db.zhilian_java_BJ.aggregate(
    #   {$group:{_id:'$workExperience',num:{$sum:1}}})
    def mongo_select_working_year_Jobs_count(self):
        lauage_name = {'python': 'zhilian_python_BJ',
                       'java': 'zhilian_java_BJ'}
        job_count = {}

        for k, v in lauage_name.items():
            count_list = []
            cursor = self.connect()[v].aggregate(
                [{"$group": {"_id": "$workExperience", "num": {"$sum": 1}}}])
            for x in cursor:
                count_list.append(x)
            job_count[k] = count_list

        return job_count

        #  TODO 岗位学历　岗位数量分布

    # > db.zhilian_java_BJ.aggregate({$group:{_id:'$eduLevel',num:{$sum:1}}})
    def mongo_select_education_level_Jobs_count(self):
        lauage_name = {'python': 'zhilian_python_BJ',
                       'java': 'zhilian_java_BJ'}
        job_count = {}

        for k, v in lauage_name.items():
            count_list = []
            cursor = self.connect()[v].aggregate(
                [{"$group": {"_id": "$eduLevel", "num": {"$sum": 1}}}])
            for x in cursor:
                count_list.append(x)
            job_count[k] = count_list

        return job_count

    # TODO 1. 语言排行榜前10就业岗位数量柱状图
    def mongo_select_Top10(self):
        lauage_name = {'python': 'zhilian_python_BJ',
                       'java': 'zhilian_java_BJ'}
        job_count = {}

        for k, v in lauage_name.items():
            cursor = self.connect()[v].count()
            job_count[k] = cursor

        return job_count

    # TODO: 3. 基于工作年限的岗位平均工资　
    # 3. 基于工作年限的岗位平均工资　
    # db.zhilian_python_BJ.aggregate(
    #   {$group:{_id:{工作年限:'$workExperience',薪资范围:'$salary'},
    #            数量:{$sum:1}}})
    def mongo_select_working_years_Jobs_avgsalary(self):
        lauage_name = {'python': 'zhilian_python_BJ',
                       'java': 'zhilian_java_BJ'}
        work_avgsalary = {}

        for k, v in lauage_name.items():
            count_list = []
            cursor = self.connect()[v].aggregate([{"$group": {
                "_id": {"work_years": "$workExperience", "salary": "$salary"},
                "count": {"$sum": 1}}}])
            for x in cursor:
                count_list.append(x)
            work_avgsalary[k] = count_list

        return work_avgsalary

    #  TODO 5. 基于学历的岗位平局薪资
    # db.zhilian_python_BJ.aggregate(
    #   {$group:{_id:{工作年限:'$eduLevel',薪资范围:'$salary'},数量:{$sum:1}}})
    def mongo_select_education_level_Jobs_avgsalary(self):
        lauage_name = {'python': 'zhilian_python_BJ',
                       'java': 'zhilian_java_BJ'}
        edu_avgsalary = {}

        for k, v in lauage_name.items():
            count_list = []
            cursor = self.connect()[v].aggregate([{"$group": {
                "_id": {"education": "$eduLevel", "salary": "$salary"},
                "count": {"$sum": 1}}}])
            for x in cursor:
                count_list.append(x)
            edu_avgsalary[k] = count_list

        return edu_avgsalary

    #  TODO 基于用户选择的岗位推荐
    # db.zhilian_python_BJ.find(
    #   {responsibility:{$regex:/python+.+css+/,$options:'i'}}).count()

    def choose_user_job_recommend(self, conditon):
        lauage_name = {'python': 'zhilian_python_BJ',
                       'java': 'zhilian_java_BJ'}
        user_chose_recommed_jobs = {}
        paremt = re.compile(conditon)
        regex = Regex.from_native(paremt)
        regex.flags = re.UNICODE

        for k, v in lauage_name.items():
            cursor = self.connect()[v].find(
                {"responsibility": {"$regex": regex, "$options": "i"}})
            count_list = []
            for x in cursor:
                count_list.append(x)
            user_chose_recommed_jobs[k] = count_list
        print(user_chose_recommed_jobs)

        return user_chose_recommed_jobs

    def _convert_regex(self, regex):
        cr = Regex.from_native(re.compile(regex))
        cr.flags = re.UNICODE
        return cr

    def search_post(self, regex, field, limit=10):
        # db.csdn.find({title:{$regex:'python', $options: '$i'}})
        cursor = self.connect()['csdn']
        posts = []
        for r in cursor.find(
                {"title": {"$regex": self._convert_regex(regex),
                           "$options": '$i'}}, field).limit(limit):
            posts.append(r)

        return posts

    def update_search_history(self, filters, update):
        # 为了加快查找速度，需要在数据库中创建以下复合索引
        # db.search_history.createIndex({search_key:1,user:1})
        cursor = self.connect()['search_history']
        cursor.update_one(filters, update, upsert=True)

    def find_search_history(self, filters, field, limit=10):
        # db.search_history.find({user:'tom',time:{$gt:"2019-04-03 08:40:30"}})
        cursor = self.connect()['search_history']
        search_history = []
        for r in cursor.find(filters, field).limit(limit):
            search_history.append(r)

        return search_history


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
        zhilian_working_yearAndJobs_count = \
            self.mongo_select_working_year_Jobs_count()

        return zhilian_working_yearAndJobs_count

    # TODO: 这里写与业务有关的数据库操作方法

    # TODO 学历和岗位数量
    # > db.zhilian_java_BJ.aggregate({$group:{_id:'$eduLevel',num:{$sum:1}}})
    def eduLevel_level_Job_ount(self):
        zhilian_endcation_level_job_count = \
            self.mongo_select_education_level_Jobs_count()

        return zhilian_endcation_level_job_count

    #  TODO Base education's post wage 基于学历的岗位工资
    def education_avgsalary(self):
        zhilian_endcation_level_job_avgsalary = \
            self.mongo_select_education_level_Jobs_avgsalary()
        return zhilian_endcation_level_job_avgsalary

    #  TODO  基于用户选择的的岗位推荐
    def job_recommd(self, condition):
        condition_user = self.choose_user_job_recommend(condition)
        return condition_user

    def get_posts(self, search_key, limit=10):
        regex = search_key
        field = {'_id': 0, 'title': 1, 'url': 1}
        posts = self.search_post(regex, field, limit)

        return posts

    def add_search_history(self, search_key, user):
        search_time = helper.get_time()

        # search_history 表中要保证 同一用户 搜索 同一关键词 的记录只有一条
        # 因此需要使用 update(upsert=True) 方法而不是 insert 方法添加搜索记录
        # 指定用户搜索指定关键词的记录已存在时，更新搜索时间；不存在时，添加新记录
        filters = {
            # 关键词忽略大小写，将关键词全部转为小写进行记录
            'search_key': search_key.lower(),
            'user': user
        }
        update = {
            '$set': {'time': search_time}
        }
        self.update_search_history(filters, update)

    def get_search_history(self, search_key, after_time, except_user,
                           limit=10):
        filters = {
            # 记录时已将关键词全部转为小写字母，查找时全部转为小写进行查找
            "search_key": search_key.lower(),
            "time": {"$gt": after_time},
            "user": {"$ne": except_user}
        }
        field = {"_id": 0, "user": 1}
        search_history = self.find_search_history(filters, field, limit)

        return search_history
