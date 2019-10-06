import mysql.connector
import datetime, time
remote_mysql_config = {
    "host":"106.13.83.102", "port":"3306",
    "user":"lcy1274560014", "password":"lcy568972!!!!!",
    "database":"fans"
}


def get_time(flags):
    if flags == 'l8':
        now_time = datetime.datetime.fromtimestamp(time.time()) # 时间戳转datetime
        start_time = str(now_time)[0:11] + '08:00:00'
        start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_timestamp = int(time.mktime(start_time_array))
        yesterday = datetime.datetime.fromtimestamp(start_timestamp - 86400)
        return [str(yesterday), start_time]

    # 返回一天前的这个时刻整点
    if flags == 'd':
        cur_time = int(time.time())
        hour_stamp = cur_time - (cur_time % 3600)  # 当前时间整点时间戳
        now_time = datetime.datetime.fromtimestamp(hour_stamp)  # 当前时间整点datetime
        last_hour = datetime.datetime.fromtimestamp(hour_stamp - 86400)  # 返回上一小时整点
        return [ str(last_hour), str(now_time)]

    # 返回上一个小时的整点
    if flags == 'h':
        cur_time = int(time.time())
        hour_stamp = cur_time - (cur_time % 3600)  # 当前时间整点时间戳
        now_time = datetime.datetime.fromtimestamp(hour_stamp)  # 当前时间整点datetime
        last_hour = datetime.datetime.fromtimestamp(hour_stamp - 3600) # 返回上一小时整点
        return [str(last_hour), str(now_time)]


class get_change():
    """
    运行run后返回的list [名称，uid，粉丝数增长情况]
    """

    def __init__(self, start_date, end_date, reverse=True):
        self.start_date = start_date
        self.end_date = end_date
        self.reverse = reverse

    def __get_table_name(self):
        con = mysql.connector.connect(**remote_mysql_config)
        cursor = con.cursor()
        sql = 'show tables'
        cursor.execute(sql)
        table_name = []
        for one in cursor:
            table_name.append(one[0])
        con.close()
        return table_name

    def get_one_hour_fans(self):
        table_name = self.__get_table_name()
        con1 = mysql.connector.connect(**remote_mysql_config)
        cursor1 = con1.cursor()
        incre_list = []
        for content in table_name:
            sql_select = "select name, fans,uid from {0} where time between '{1}' and '{2}' ".format(content, self.start_date, self.end_date)
            cursor1.execute(sql_select)
            one_data = cursor1.fetchall()
            try:
                increase_fans = one_data[-1][1] - one_data[0][1]
                cell = [one_data[0][0], one_data[0][1], increase_fans]
                incre_list.append(cell)

            except:
                cell = [content, '数据不足']
                incre_list.append(cell)
        con1.close()
        rank_result = sorted(incre_list, key=lambda s: s[2], reverse=self.reverse)
        return rank_result


    def get_ranked_uid(self):
        """
        获取排好序的uidlist
        :return: uid list
        """
        ranked_uid = []
        for i in self.increment:
            ranked_uid.append(i[1])
        return ranked_uid

    def get_ranked_name(self):
        """
        获取排好序的name
        :return: name list
        """

        ranked_name = []
        for i in self.increment:
            ranked_name.append(i[0])
        return ranked_name

    def get_ranked_change(self):
        """
        获取排好序的粉丝数变化list
        :return: list change
        """
        ranked_change = []
        for i in self.increment:
            ranked_change.append(i[2])
        return ranked_change

    def run(self):
        self.increment = self.get_one_hour_fans()
        return self.increment


# if __name__ == "__main__":
#     res = get_time(flags='h')
#     print(res)
#     # get_one = get_change(res[0], res[1])
#     # all = get_one.run()
#     # uid = get_one.get_ranked_uid()
#     # print(all)
#     # print(uid)
