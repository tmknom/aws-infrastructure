variable "application_name" {}    # .bash_profileに環境変数定義 : TF_VAR_application_name
variable "db_port" {}             # .bash_profileに環境変数定義 : TF_VAR_db_port
variable "db_name" {}             # .bash_profileに環境変数定義 : TF_VAR_db_name
variable "db_master_user_name" {} # .bash_profileに環境変数定義 : TF_VAR_db_master_user_name
variable "db_initial_password" {} # .bash_profileに環境変数定義 : TF_VAR_db_initial_password

variable "vpc_id" {}                      # .bash_profileに環境変数定義 : TF_VAR_vpc_id
variable "db_subnet_ids" {}               # .bash_profileに環境変数定義 : TF_VAR_db_subnet_ids
variable "db_source_security_group_id" {} # .bash_profileに環境変数定義 : TF_VAR_db_source_security_group_id

variable "environment" {
  default = "Production"
}

module "security_group" {
  source = "../../terraform/module/security_group/source_security_group_id"

  name = "${var.environment}-${var.application_name}-MySQL"
  source_security_group_id = "${var.db_source_security_group_id}"
  vpc_id = "${var.vpc_id}"
  description = "allow ${var.environment} ${var.application_name} MySQL"

  port = "${var.db_port}"
}

module "rds" {
  source = "../../terraform/module/rds"

  rds_name = "${var.application_name}"
  environment = "${var.environment}"

  db_port = "${var.db_port}"

  db_name = "${var.db_name}"
  master_user_name = "${var.db_master_user_name}"
  master_user_password = "${var.db_initial_password}"

  availability_zone = "ap-northeast-1c"
  subnet_ids = "${var.db_subnet_ids}"
  security_group_id = "${module.security_group.id}"

  storage_size = 5
  backup_retention_period = 5
  multi_az = false
}
