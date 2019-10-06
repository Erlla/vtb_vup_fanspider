"""
需要上传
"""
# 请求头
headers=[{
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
},{"User-Agent" : "Mozilla/5.0 (Windows NT 6.3;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
} ,{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}]

# 本地册数数据库
local_config = {
    "host":"localhost", "port":"3306",
    "user":"root", "password":"****",
    "database":"vtb_fans"
}
config_uid = {
    "host":"localhost", "port":"3306",
    "user":"root", "password":"****",
    "database":"uid_info"
}

# 远程数据库
remote_mysql_config = {
    "host":"****", "port":"3306",
    "user":"lcy1274560014", "password":"****",
    "database":"fans"
}

remote_config_uid = {
    "host":"****", "port":"3306",
    "user":"lcy1274560014", "password":"****",
    "database":"uid_info"
}