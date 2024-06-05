from fabric import task
from invoke import Responder
 
 
@task()
def deploy(c):
    supervisor_conf_path = '~/'
    supervisor_program_name = 'myblog2'
 
    project_root_path = '~/sites/myblogV2/'
 
    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = '/home/admin/.local/bin/supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)
 
    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        c.run(cmd)
 
    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        c.run('pipenv run python manage.py migrate')
        c.run('pipenv run python manage.py collectstatic --noinput')
 
    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = '/home/admin/.local/bin/supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)
