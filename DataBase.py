# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
from redis import Redis,ConnectionPool

# MySql
db = SQLAlchemy()
# Redis
conn_pool = ConnectionPool(host='localhost',port=6379,db=0)
alive_key = Redis(connection_pool=conn_pool)
"""
# 这里目前还不需要
 task_queue = Redis(connection_pool=conn_pool)
"""


