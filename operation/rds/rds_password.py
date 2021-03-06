# -*- encoding:utf-8 -*-

from fabric.api import *
from fabric.contrib.console import *


def change_production():
    change('production-mysql', 'DATABASE_MASTER_USER_PASSWORD_PRODUCTION')


def change_administration():
    change('administration-mysql', 'DATABASE_MASTER_USER_PASSWORD_ADMINISTRATION')


def change_production_us():
    change('production-mysql', 'DATABASE_MASTER_USER_PASSWORD_PRODUCTION_US', 'us-west-1')


def change(db_instance_identifier, env_db_password, region='ap-northeast-1'):
    if not confirm("%s のパスワードを変更します。本当に実行しますか？" % (db_instance_identifier)):
        abort('パスワードの変更を中止しました。')
    db_password = get_env(env_db_password)
    execute_modify_password(db_instance_identifier, db_password, region)


def execute_modify_password(db_instance_identifier, db_password, region):
    command = ' aws rds modify-db-instance' \
              + " --region %s " % (region) \
              + ' --db-instance-identifier %s' % (db_instance_identifier) \
              + ' --master-user-password "%s"' % (db_password)
    with hide('running'):
        local(command)


def get_env(key_name):
    command = 'echo $%s' % (key_name)
    with hide('stdout'):
        result = local(command, capture=True)
    return result
