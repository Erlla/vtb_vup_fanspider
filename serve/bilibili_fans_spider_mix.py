"""
需要上传
"""

from urllib import request
import re
import time
import mysql.connector
from serve.auto_email import email_send
from db.config import headers, remote_config_uid
import random


class Spider(object):
    """
    b站数据爬虫
    """
    def __init__(self, config, uid_table_name):
        """
        构造函数
        :param config: 数据库连接配置
        :param uid_table_name: uid数据库表名
        """
        self.uid_table_name = uid_table_name
        self.config = config
        # self.speed = speed

    def __mysql_read_uid(self, table_name):
        """
        查找并返回表名和uid
        :param table_name: 数据库中uid对应的表名
        :return: 返回一个列表 包含 表名和uid [（表名，uid）]
        """
        try:
            con1 = mysql.connector.connect(**remote_config_uid)
            cursor2 = con1.cursor()
            uid_list = []

            sql = 'SELECT table_name,uid from {0}'.format(table_name)
            cursor2.execute(sql)
            for one in cursor2:
                uid_list.append(one)
            con1.close()
            print('uid信息成功导入')
            return uid_list
        except Exception as e:
            print('载入uid信息失败，请检查数据库连接信息')
            print('错误信息：%s' %e)

    def __write_to_sql(self, table_name, uid):
        """

        :param table_name: vtb_fans的表名
        :return: null
        """
        con = mysql.connector.connect(**self.config)
        con.cmd_statistics() # 开启事务
        cursor = con.cursor()
        # args = (name, self.name[0], self.fans[0])
        # sql = "INSERT %s(name,fans,time) VALUES(%s,%s,NOW())"
        # cursor.execute(sql, args) # 先预编译
        sql = "INSERT {0}(name,fans,time,uid) VALUES('{1}',{2},NOW(),{3})".format(table_name, self.name[0], self.fans[0], uid)
        cursor.execute(sql)
        con.commit()
        print("成功录入{0}的粉丝信息".format(self.name[0]))
        con.close()

    def __get_htmls(self):
        table_uid_list = self.__mysql_read_uid(self.uid_table_name)
        for content in table_uid_list:
            try:
                # 获取uid
                url = 'https://api.bilibili.com/x/web-interface/card?mid={0}'.format(content[1])
                req = request.Request(url=url, headers=headers[random.randint(0, len(headers) - 1)])
                # 随机请求头
                r = request.urlopen(req)
                self.htmls = r.read()
                self.htmls = str(self.htmls, encoding='utf-8')
                self.name = re.findall(r'"name":"([\s\S]*?)",', self.htmls)
                self.fans = re.findall(r'"fans":([\s\S]*?),', self.htmls)
                self.__write_to_sql(content[0], content[1]) # 传入表名与uid
                time.sleep(0.5) # 爬取每一个粉丝数的速度，若没有代理ip建议调高

            except Exception as e:
                print('程序错误')
                nowtimes = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(nowtimes)
                msg = '爬虫出现异常\n错误信息：\n {0} \n请及时检查\n\n\n\n{1}'.format(e, nowtimes)
                email_send('爬虫出现异常', msg)  # 发送邮件
                time.sleep(5)
                print(e)
                # con.rollback()
                # 限制爬取速度，防止ip被封
        # time.sleep(self.speed)

    def run(self):
        self.__get_htmls()  # 运行主程序
        print('等待5分钟......')



