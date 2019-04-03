from flask import g, Flask, jsonify, make_response, request
from flask_cors import CORS

from spiderdata_server.server import helper
from spiderdata_server.server.data.manager import zhilian_postion
from spiderdata_server.server.data.manager import CSDN
from spiderdata_server.server.user import manager as user_manager

post_manager = zhilian_postion()
csdn_manager = CSDN()

app = Flask(__name__)
CORS(app, supports_credentials=True)


# －－－－－－－－－－首页展示
#   server --> client
#  python  javaScript c ..智联招聘的每个数量返回数字
@app.route('/v1/jobs_count', methods=['GET'])
def jobsAndLauage_Top10_count():
    lauage_post = post_manager.lauage_position_top10()
    resp = {'body': {'jobs': lauage_post}}

    return make_response(jsonify(resp), 200)


# TODO 前十语言招聘数量排行
@app.route('/v1/work_year_job_count', methods=['GET'])
def work_year_job_count():
    work_yesrs_job_counts = post_manager.working_year_Jobs_count()
    resp = {'body': {'jobs': work_yesrs_job_counts}}

    return make_response(jsonify(resp), 200)


# TODO 岗位学历和岗位数量图
@app.route('/v1/education_level_job_count', methods=['GET'])
def education_level_job_count():
    eduLevel_job_counts = post_manager.eduLevel_JobCount()
    resp = {'body': {'jobs': eduLevel_job_counts}}

    return make_response(jsonify(resp), 200)


# TODO 工作年限和岗位平均工资
@app.route('/v1/work_year_job_avgsalary', methods=['GET'])
def work_year_job_avgsalary():
    work_years_job_avgsalarys = post_manager.working_year_avageSalary()
    resp = {'body': {'jobs': work_years_job_avgsalarys}}

    return make_response(jsonify(resp), 200)


# TODO 学历的平均工资
@app.route('/v1/edulevel_job_avgsalary', methods=['GET'])
def edulevel_job_avgsalary():
    edulevel_job_avgsalarys = post_manager.education_avgsalary()
    resp = {'body': {'jobs': edulevel_job_avgsalarys}}

    return make_response(jsonify(resp), 200)


# TODO 　获取前台的数据－岗位推荐
@app.route('/v1/job_recommend', methods=['POST'])
def job_recommend():
    skills = request.json.get('skill')
    # skills = ['python', 'css']
    condition = "+.+".join(skills)
    job_recommend_user = post_manager.job_recommend(condition)
    resp = {'body': {'jobs': job_recommend_user}}

    return make_response(jsonify(job_recommend_user), 200)


@app.route('/v1/search_post', methods=['GET'])
def search_post():
    token = request.json.get('token')
    search_key = request.json.get('search_key')
    limit = request.json.get('limit', 10)

    # 调用方法，在数据库中检索关键字，默认返回最近 10 条数据
    search_result = csdn_manager.search_post(search_key, limit=limit)

    user_list = []
    if token:
        # 根据 token 获取用户名，将用户名存到数据库中关键词搜索历史中
        user = user_manager.get_user_by_token(token)
        csdn_manager.add_search_history(search_key, user.username)

        # 获取最近的 20 个搜索过该关键词的用户名列表
        user_list = csdn_manager.get_search_history(search_key,
                                                    user.username, 20)

    resp = helper.make_response_dict(40001,
                                     'success',
                                     {'result': search_result,
                                      'user_list': user_list})
    return make_response(jsonify(resp), 201)
