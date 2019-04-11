"""
职位分析模块业务代码
"""
import re

from spiderdata_server.db.mongodb_client import MongodbClient
from spiderdata_server.server import helper

DB = MongodbClient()


class zhilian_postion(object):
    def __init__(self):
        pass

    # TODO 前十语言数量排行榜
    def lauage_position_top10(self):
        lauage_count = DB.select_Top10()
        return lauage_count

    # TODO 工作年限和岗位数量
    def working_year_Jobs_count(self):
        zhilian_working_year_Jobs_count = DB.working_year_Jobs_count()
        return zhilian_working_year_Jobs_count

    # TODO 工作年限和和平均工资
    def working_year_avageSalary(self):
        zhilian_work_year_job_salary = \
            DB.mongo_select_working_years_Jobs_avgsalary()
        salaries_by_language = {}
        for language, item in zhilian_work_year_job_salary.items():
            salaries = {}
            for i in item:
                # i 格式
                # {
                #   'count': 1,
                #   '_id': {'work_years': '不限', 'salary': '10K-20K'}
                # }
                work_years = i['_id']['work_years']
                salary = i['_id']['salary']
                count = int(i['count'])
                # 去除无法统计的数据
                if work_years in ['不限', '无经验'] or salary in ['薪资面议']:
                    continue
                salary = re.search(r'(.+)K-(.+)K', salary).groups()
                salary_min = float(salary[0]) * 1000
                salary_max = float(salary[1]) * 1000

                if work_years in salaries:
                    salaries[work_years]['min'] += salary_min * count
                    salaries[work_years]['max'] += salary_max * count
                    salaries[work_years]['count'] += count
                else:
                    salaries[work_years] = {
                        'min': salary_min * count,
                        'max': salary_max * count,
                        'count': count
                    }

            for year, salary_info in salaries.items():
                salaries[year]['min_avg'] = (salary_info['min'] //
                                             salary_info['count'])
                salaries[year]['max_avg'] = (salary_info['max'] //
                                             salary_info['count'])
            salaries_by_language[language] = salaries

        return salaries_by_language

    # TODO: 这里写与业务有关的数据库操作方法

    # TODO 学历和岗位数量
    def eduLevel_JobCount(self):
        zhilian_eduLevel_job_count = DB.eduLevel_level_Job_ount()
        return zhilian_eduLevel_job_count

    #  TODO Base education's post wage 基于学历的岗位工资
    def education_avgsalary(self):
        zhilian_edulevle_job_avgsalary = DB.education_avgsalary()

        salaries_by_language = {}
        for language, item in zhilian_edulevle_job_avgsalary.items():
            salaries = {}
            for i in item:
                # i 格式
                # {
                #   'count': 3,
                #   '_id': {'salary': '12K-22K', 'education': '本科'}
                # }
                education = i['_id']['education']
                salary = i['_id']['salary']
                count = int(i['count'])
                # 去除无法统计的数据
                if education in ['不限'] or salary in ['薪资面议']:
                    continue
                salary = re.search(r'(.+)K-(.+)K', salary).groups()
                salary_min = float(salary[0]) * 1000
                salary_max = float(salary[1]) * 1000

                if education in salaries:
                    salaries[education]['min'] += salary_min * count
                    salaries[education]['max'] += salary_max * count
                    salaries[education]['count'] += count
                else:
                    salaries[education] = {
                        'min': salary_min * count,
                        'max': salary_max * count,
                        'count': count
                    }

            for edu, salary_info in salaries.items():
                salaries[edu]['min_avg'] = (salary_info['min'] //
                                            salary_info['count'])
                salaries[edu]['max_avg'] = (salary_info['max'] //
                                            salary_info['count'])
            salaries_by_language[language] = salaries

        return salaries_by_language

    #  TODO  基于用户选择的的岗位推荐
    def job_recommend(self, conndition):
        perfect_job = DB.job_recommd(conndition)
        job_info = {
            'job_name': perfect_job['python'][0][' jobName'],
            'job_url': perfect_job['python'][0]['jobURL']
        }

        return job_info


class CSDN(object):
    def __init__(self):
        pass

    def search_post(self, search_key, limit=10):
        """基于指定的关键字查找相关内容"""
        # 调数据库接口，基于关键字查询相关内容
        posts = DB.get_posts(search_key, limit)

        return posts

    def add_search_history(self, search_key, user):
        DB.add_search_history(search_key, user)

    def get_search_history(self, search_key, except_user, limit=10):
        """获取指定关键字最近的查询记录"""
        # 只查询最近 10 天内的搜索记录
        after_time = helper.get_time(helper.get_time_sec() - (10 * 24 * 60 *
                                                              60))
        # 获取最近搜索指定关键字的用户列表
        posts = [k['user'] for k in DB.get_search_history(search_key,
                                                          after_time,
                                                          except_user, limit)]

        return posts
