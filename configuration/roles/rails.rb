include_recipe 'base.rb'

include_recipe '../cookbooks/fabric/default.rb'
include_recipe '../cookbooks/mysql_client/default.rb'
include_recipe '../cookbooks/nodejs/default.rb'
include_recipe '../cookbooks/phantomjs/default.rb'
include_recipe '../cookbooks/redis/default.rb'
include_recipe '../cookbooks/ruby/default.rb'

include_recipe '../cookbooks/user/rails.rb'

include_recipe '../cookbooks/nginx/default.rb'
include_recipe '../cookbooks/logrotate/nginx.rb'
include_recipe '../cookbooks/monit/nginx.rb'
