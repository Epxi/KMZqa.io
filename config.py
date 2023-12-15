# 配置文件

SECRET_KEY = 'aewdfsadf'

# MySQL所在的主机IP
HOSTNAME = '127.0.0.1'
# MySQL的端口号
PORT = '3306'
# MySQL用户名
USERNAME = 'root'
# MySQL密码
PASSWORD = '0901'
# MySQL数据库名
DATABASE = 'q&a'
DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '465'
MAIL_USE_SSL = True
MAIL_USERNAME = 'qq1318342521@163.com'
MAIL_PASSWORD = 'YAEMMTADZTKCSGXK'
MAIL_DEFAULT_SENDER = 'qq1318342521@163.com'

