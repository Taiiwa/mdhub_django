# 导包
import redis

# 定义ip 和端口
host = '127.0.0.1'
port = 6379

# 生成连接对象
r = redis.Redis(host=host, port=port)

# 操作
r.set('test','TEXT')

my_test = r.get('test')

# 转码
my_test = my_test.decode('utf8')

print(my_test)
