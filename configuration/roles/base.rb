include_recipe '../cookbooks/sudo/default.rb'
include_recipe '../cookbooks/user/default.rb'
include_recipe '../cookbooks/sshd/default.rb'
include_recipe '../cookbooks/cloud_init/default.rb'
include_recipe '../cookbooks/swap/default.rb'
include_recipe '../cookbooks/rpm_repository/default.rb'
include_recipe '../cookbooks/rpm_package/default.rb'
include_recipe '../cookbooks/command_log/default.rb'
include_recipe '../cookbooks/monit/default.rb'
include_recipe '../cookbooks/cloud_watch/default.rb'