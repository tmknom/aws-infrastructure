# -*- encoding:utf-8 -*-
#
# 各種リソースの構築スクリプト
#
#####################################################################

from fabric.api import *

from terraform.cli.cli_helper import *
from helper import *


@task
def build_ec2_production():
    '''本番環境のEC2構築'''
    tf_vars = get_ec2_tf_vars(ENVIRONMENT_PRODUCTION, ROLE_RAILS, TECH_NEWS)
    terraform_apply('ec2/production/tech_news', tf_vars)


@task
def build_ec2_testing():
    '''テスト環境のEC2構築'''
    tf_vars = get_ec2_tf_vars(ENVIRONMENT_PRODUCTION, ROLE_RAILS, TECH_NEWS)
    terraform_apply('ec2/testing/tech_news', tf_vars)


@task
def build_security_group():
    '''セキュリティグループ構築'''
    tf_vars = get_tf_vars()
    terraform_apply('security_group', tf_vars)


@task
def build_rds():
    '''RDS構築'''
    tf_vars = get_db_tf_vars()
    terraform_apply('rds', tf_vars)


@task
def change_password_rds_production():
    '''本番環境のRDSのパスワード変更'''
    local('fab change_password:%s -f rds/password_changer.py' % ('production-mysql'))


@task
def build_vpc():
    '''VPC構築'''
    terraform_apply('vpc')


@task
def build_code_deploy():
    '''CodeDeploy構築'''
    terraform_apply('code_deploy')


@task
def build_instance_profile():
    '''InstanceProfileの構築'''
    terraform_apply('instance_profile/initialization')
    terraform_apply('instance_profile/rails')


@task
def build_user_cli():
    '''CLIユーザの構築'''
    terraform_apply('iam_user/cli/administrator')


@task
def build_user_external():
    '''AWS外部用システムユーザの構築'''
    terraform_apply('iam_user/external/circle_ci')


@task
def build_s3_log():
    '''s3-log バケットの構築'''
    terraform_apply('s3/s3_log')


@task
def build_s3_terraform():
    '''terraform バケットの構築'''
    terraform_apply('s3/terraform')


@task
def build_s3_cloud_trail():
    '''cloud-trail バケットの構築'''
    terraform_apply('s3/cloud_trail')


@task
def build_cloud_trail():
    '''CloudTrailの構築'''
    terraform_apply('cloud_trail')
