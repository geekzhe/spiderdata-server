from flask import g, Flask, jsonify, make_response, request
from flask_cors import CORS

from spiderdata_server.server import helper
from spiderdata_server.server.data.manager import zhilian_postion


post_manager = zhilian_postion()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# －－－－－－－－－－首页展示
#   server --> client
#  python  javaScript c ..智联招聘的每个数量返回数字
@app.route('/v1/jobs_count', methods=['GET'])
def jobsAndLauage_Top10_count():
    lauage_post= post_manager.lauage_position_top10()
    resp={'body':{'jobs':lauage_post}}

    return make_response(jsonify(resp),200)


# TODO 前十语言招聘数量排行
@app.route('/v1/work_year_job_count', methods=['GET'])
def work_year_job_count():
    work_yesrs_job_counts= post_manager.working_year_Jobs_count()
    resp={'body':{'jobs':work_yesrs_job_counts}}

    return make_response(jsonify(resp),200)

# TODO 岗位学历和岗位数量图
@app.route('/v1/education_level_job_count', methods=['GET'])
def education_level_job_count():
    eduLevel_job_counts= post_manager.eduLevel_JobCount()
    resp={'body':{'jobs':eduLevel_job_counts}}

    return make_response(jsonify(resp),200)



# TODO 工作年限和岗位平均工资
@app.route('/v1/work_year_job_avgsalary', methods=['GET'])
def work_year_job_avgsalary():
    work_years_job_avgsalarys= post_manager.working_year_avageSalary()
    resp={'body':{'jobs':work_years_job_avgsalarys}}

    return make_response(jsonify(resp),200)


# TODO 学历的平均工资
@app.route('/v1/edulevel_job_avgsalary', methods=['GET'])
def edulevel_job_avgsalary():
    edulevel_job_avgsalarys= post_manager.education_avgsalary()
    resp={'body':{'jobs':edulevel_job_avgsalarys}}

    return make_response(jsonify(resp),200)




# TODO 　获取前台的数据－岗位推荐
@app.route('/v1/job_recommend', methods=['POST'])
def  job_recommend():
    skills = request.json.get('skill')
    # skills = ['python', 'css']
    condition = "+.+".join(skills)
    job_recommend_user= post_manager.job_recommend(condition)
    resp={'body':{'jobs':job_recommend_user}}

    return make_response(jsonify(job_recommend_user),200)

