#!/bin/bash
# 运行程序
server_url="http://localhost:12480"

api_url="${server_url}/v1/mean"
echo ${server_url}
echo ${api_url}
echo 'Running APIServer.py....'

# 放入后台运行
python APIServer.py test 1>/dev/null 2>/dev/null  &
sleep 1s
echo successful!

# 清理工作
echo 'kill APIServer'
kill  $(ps aux |grep APIServer.py |awk NR==1'{print $2}')





