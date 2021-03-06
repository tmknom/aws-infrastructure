# -*- encoding:utf-8 -*-
#
# 各種リソースの構築スクリプト
#
#####################################################################

from fabric.api import *

from terraform.cli.cli_helper import *
from helper import *
from kms.kms import *


@task
def build_ec2_tech_news():
    '''tech_news のEC2構築'''
    tf_vars = get_ec2_tf_vars(ENVIRONMENT_PRODUCTION, ROLE_INTERNAL_RAILS, TECH_NEWS)
    terraform_apply('ec2/production/tech_news', tf_vars)


@task
def build_ec2_wonderful_world():
    '''wonderful_world のEC2構築'''
    tf_vars = get_ec2_tf_vars(ENVIRONMENT_PRODUCTION, ROLE_RAILS, WONDERFUL_WORLD, REGION_US)
    terraform_apply('ec2/production/wonderful_world', tf_vars)


@task
def build_elb_wonderful_world():
    '''wonderful_world のELB構築'''
    tf_vars = get_elb_tf_vars(ENVIRONMENT_PRODUCTION, REGION_US)
    terraform_apply('elb/wonderful_world', tf_vars)


@task
def build_security_group():
    '''セキュリティグループ構築'''
    tf_vars = get_tf_vars()
    terraform_apply('security_group', tf_vars)


@task
def build_security_group_us():
    '''USのセキュリティグループ構築'''
    tf_vars = get_tf_vars(REGION_US)
    terraform_apply('security_group/us_west_1', tf_vars)


@task
def build_rds():
    '''RDS構築'''
    tf_vars = get_db_tf_vars()
    terraform_apply('rds', tf_vars)


@task
def build_rds_us():
    '''USのRDS構築'''
    tf_vars = get_db_tf_vars(REGION_US)
    terraform_apply('rds/us_west_1', tf_vars)


@task
def build_vpc():
    '''VPC構築'''
    terraform_apply('vpc')


@task
def build_vpc_us():
    '''USのVPC構築'''
    terraform_apply('vpc/us_west_1')


@task
def build_code_deploy():
    '''CodeDeploy構築'''
    terraform_apply('code_deploy')


@task
def build_code_deploy_us():
    '''USのCodeDeploy構築'''
    tf_vars = get_code_deploy_tf_vars()
    terraform_apply('code_deploy/us_west_1', tf_vars)


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
    terraform_apply('iam_user/external/wercker')
    terraform_apply('iam_user/external/circle_ci')


@task
def build_s3_log():
    '''s3-log バケットの構築'''
    terraform_apply('s3/s3_log/us_west_1')
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
def build_s3_deployment():
    '''deployment バケットの構築'''
    terraform_apply('s3/deployment/us_west_1')
    terraform_apply('s3/deployment')


@task
def build_s3_temporary():
    '''temporary バケットの構築'''
    terraform_apply('s3/temporary')


@task
def build_kms_encryption_data():
    '''encryption-dataのKMS構築'''
    build_kms(ENCRYPTION_DATA_MASTER_KEY_PARAMS)


@task
def build_cloud_trail():
    '''CloudTrailの構築'''
    terraform_apply('cloud_trail')
