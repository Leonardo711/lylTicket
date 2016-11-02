# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 23:59:05 2016

@author: Zero
"""

from stations import stations
import requests
from prettytable import PrettyTable

def cli():
   # arguments = docopt(__doc__)
    
    from_station = stations.get('shanghai')
    to_station = stations.get('suzhou')
    date = '2016-11-08'
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )
    
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    #print(r.json())
    
    rows = r.json()['data']['datas']
    trains = TrainCollection(rows)
    #trains.pretty_print()
    trains.get_station()


class TrainCollection(object):

    # 显示车次、出发/到达站、 出发/到达时间、历时、一等坐、二等坐、软卧、硬卧、硬座
    header = 'train station time duration first second softsleep hardsleep hardsit'.split()

    def __init__(self, rows):
        self.rows = rows

    def _get_duration(self, row):
        """
        获取车次运行时间
        """
        duration = row.get('lishi').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for row in self.rows:
            train = [
                # 车次
                row['station_train_code'],
                # 出发、到达站
                '\n'.join([row['from_station_name'], row['to_station_name']]),
                # 出发、到达时间
                '\n'.join([row['start_time'], row['arrive_time']]),
                # 历时
                self._get_duration(row),
                # 一等坐
                row['zy_num'],
                # 二等坐
                row['ze_num'],
                # 软卧
                row['rw_num'],
                # 软坐
                row['yw_num'],
                # 硬坐
                row['yz_num']
            ]
            yield train

    def pretty_print(self):
        """
        数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来。
        `prettytable`这个库可以让我们它像MySQL数据库那样格式化显示数据。
        """
        pt = PrettyTable()
        # 设置每一列的标题
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
            #print train
        print(pt)
    def get_station(self):
        from_stations = []
        to_stations = []
        for train in self.trains:
            temp = train[1].split('\n')
            from_stations.append(temp[0])
            to_stations.append(temp[1])
        from_stations_set = set(from_stations)
        to_stations_set = set(to_stations)  
        return from_stations_set,to_stations_set

def getStations(from_city,to_city):
   # arguments = docopt(__doc__)
    
    from_station = stations.get(from_city)
    to_station = stations.get(to_city)
    date = '2016-11-08'
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )
    
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    #print(r.json())
    
    rows = r.json()['data']['datas']
    trains = TrainCollection(rows)
    #trains.pretty_print()
    from_stations_set, to_stations_set = trains.get_station()
    return from_stations_set,to_stations_set

if __name__ == '__main__':
#    cli()
    from_stations_set, to_stations_set = getStations('shanghai','beijing')
    for x in from_stations_set:
        print x
    print
    for x in to_stations_set:
        print x