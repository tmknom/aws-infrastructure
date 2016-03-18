# -*- encoding:utf-8 -*-

from fabric.api import *
from fabric.contrib.console import *

BUCKET_IDENTIFIER = 'terraform'
REGION = 'ap-northeast-1'

@task
def terraform_plan(resource_dir):
  '''terraform planコマンド実行'''
  execute_terraform(resource_dir, 'plan')

@task
def terraform_plan_destroy(resource_dir):
  '''terraform plan -destroyコマンド実行'''
  execute_terraform(resource_dir, 'plan -destroy')

@task
def terraform_apply(resource_dir):
  '''terraform applyコマンド実行'''
  if not confirm("実行するとリソースを更新します。本当に実行しますか？"):
    abort('リソースの更新を中止しました。')
  execute_terraform(resource_dir, 'apply')

@task
def terraform_destroy(resource_dir):
  '''terraform destroyコマンド実行'''
  if not confirm("実行するとリソースを破棄します。本当に実行しますか？"):
    abort('リソースの破棄を中止しました。')
  execute_terraform(resource_dir, 'destroy -force')


def execute_terraform(resource_dir, command):
  with lcd('%s' % (resource_dir)):
    remote_config(resource_dir)
    local('terraform remote pull')
    local('terraform %s' % (command))
    local('terraform remote push')

def remote_config(resource_dir):
  bucket_name = get_bucket_name()
  command = ' terraform remote config' \
          + ' -backend=S3' \
          + ' -backend-config="bucket=%s"' % (bucket_name) \
          + ' -backend-config="key=%s/terraform.tfstate"' % (resource_dir) \
          + ' -backend-config="region=%s"' % (REGION)
  local(command)

def get_bucket_name():
  s3_suffix = get_s3_suffix()
  return "%s-%s" % (BUCKET_IDENTIFIER, s3_suffix)

def get_s3_suffix():
  command = 'echo $TF_VAR_s3_suffix'
  result = local(command, capture=True)
  return result

