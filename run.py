"""
需要上传
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from serve.bilibili_fans_spider_mix import Spider
from db.config import remote_mysql_config
import time
from db.record_log import record
from serve.auto_email import email_send
from serve.analysis import analysis_create_days, analysis_create_hours
start_time = time.time()


def run_spider():

    spider2 = Spider(remote_mysql_config, uid_table_name='uid_info2')
    spider3 = Spider(remote_mysql_config, uid_table_name='uid_info3')
    spider2 = threading.Thread(target=spider2.run, name='spider2')
    spider3 = threading.Thread(target=spider3.run, name='spider3')
    spider2.start()
    spider3.start()
    spider2.join()
    spider3.join()


def report_start_condition():
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    email_send('爬虫已成功启动', '爬虫已成功启动......\n\n\n{0}'.format(now_time))
    content = '\nspider started\n{0}\ncurrent threading{1}'.format(now_time, threading.current_thread())
    record(content, 'time_line.txt')
    # 记录日志文件


def send_report_mail():
    email_send('12小时运行报告', '爬虫运行{0}小时 \n 爬虫运行正常'.format((time.time() - start_time)/3600))


if __name__ == '__main__':
    scheduler2 = BackgroundScheduler() # 不阻塞线程 后台运行
    scheduler2.add_job(send_report_mail,'interval', hours=12, start_date='2019-09-09 00:00:00',
                      end_date='2022-4-01 23:00:00') # 发送状态报告
    scheduler2.start()  # 非阻塞线程，先运行

    # 发送粉丝数分析报告
    scheduler3 = BackgroundScheduler()
    scheduler4 = BackgroundScheduler()
    scheduler3.add_job(analysis_create_days, 'interval', hours=24, start_date='2019-09-09 00:00:00',
                       end_date='2022-4-01 23:00:00')
    scheduler4.add_job(analysis_create_hours, 'interval', hours=1, start_date='2019-09-09 00:08:00',
                       end_date='2022-4-01 23:00:00')
    scheduler3.start()
    scheduler4.start()

    report_start_condition() # 汇报启动情况
    scheduler1 = BlockingScheduler()
    # 在 2019-09-09 00:00:00 ~ 2019-12-31 00:00:00 之间, 每隔5分钟执行一次 run_spider 方法
    scheduler1.add_job(run_spider, 'interval', minutes=5, start_date='2019-09-09 00:00:00',
                      end_date='2020-4-01 23:00:00')
    scheduler1.start() # 阻塞线程，最后运行

