"""
需要上传
"""

import time

nowtime = time.asctime(time.localtime(time.time()))
# 记录爬虫启动的时间
def record(content, file_name):
    f = open(file_name, mode='a+')
    f.write(content)
    f.write('\n')
    f.write('---------------------')
    f.close()
#
# if __name__ == '__main__':
#     record('6666')
