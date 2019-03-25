# coding=utf-8
# @File : spider.py
# @Author : Leoren
# @Date : 2019/3/18  10:43
# @Desc : 抓取全国行政区划的名字和代码

import requests
from requests.exceptions import ConnectionError
import re
import time
import pymysql

db = pymysql.connect("localhost", "root", "root", "play")
cursor = db.cursor()


class Address(object):
    def __init__(self, id, name, level, parent_id, cities_url):
        self.id = id
        self.name = name
        self.level = level
        self.parent_id = parent_id
        self.cities_url = cities_url

    def printof(self):
        print('{')
        print('id :', self.id)
        print('name : ', self.name)
        print('level : ', self.level)
        print('parent_id :', self.parent_id)
        print('cities_url : ', self.cities_url)
        print('}')

    def insertInfo(self):
        print('(', self.id, ',', self.level, ',', self.parent_id, ',', '\'', self.name, '\'),')

    def insertInfo1(self):
        print('(', self.id, ',', self.level, ',', self.parent_id, ',', '\'', self.name, '\')')


base_url = 'https://xingzhengquhua.51240.com/'

max_count = 5
city_count = 1

proxy_pool_url = 'http://127.0.0.1:5000/get'
proxy = None

addressList = []
cityUrlList = []


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    time.sleep(2)
    print('Crawling ', url)
    print('Trying Count', count)
    global proxy
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            print('Using Proxy', proxy)
            response = requests.get(url, proxies=proxies)
        else:
            response = requests.get(url)
        if response.status_code == 503:
            # Need Proxy
            print('503')
            proxy = get_proxy()
            if proxy:
                print('Using proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
        html = response.text
        return html
    except ConnectionError:
        if count > max_count:
            print('请求次数太多')
            return None
        count += 1
        get_html(url, count)

# <tr><td bgcolor="#FFFFFF"><a href="/110000000000__xingzhengquhua/">北京市</a></td>


def parse_province(html, parent_id=0, level=1):
    if html == None:
        return
    pattern = re.compile('<tr><td bgcolor="#FFFFFF"><a href="(/\d+.*?/)">(.*?)</a></td>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'cities_url': base_url + item[0],
            'province_name': item[1],
            'parent_id': parent_id,
            'level': level
        }


def get_district():
    global city_count
    for i in range(31, len(addressList)):
        address = addressList[i]
        district_html = get_html(address.cities_url)
        for item in parse_province(district_html, address.id, 3):
            address = Address(city_count, item['province_name'], item['level'], item['parent_id'], item['cities_url'])
            address.printof()
            city_count += 1
            addressList.append(address)


def get_city():
    global city_count
    global addressList
    for i in range(len(addressList)):
        address = addressList[i]
        city_html = get_html(address.cities_url)
        for item in parse_province(city_html, address.id, 2):
            address = Address(city_count, item['province_name'], item['level'], item['parent_id'], item['cities_url'])
            address.printof()
            city_count += 1
            addressList.append(address)
        get_district()


def insertMysql(sql):
    sql = "INSERT INTO address(id,level,parent_id,NAME) VALUES" + sql
    print('inser 语句', sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print('hahah')
        db.rollback()


def main():
    global city_count
    global addressList
    html = get_html(base_url)
    for item in parse_province(html):
        address = Address(city_count, item['province_name'], item['level'], item['parent_id'], item['cities_url'])
        address.printof()
        city_count += 1
        addressList.append(address)
    get_city()
    sql = ""
    for i in range(len(addressList)):
        address1 = addressList[i]
        if i == len(addressList):
            sql = sql + address1.insertInfo1()
            break
        sql = sql + address1.insertInfo()
    print('value 语句' + sql)
    insertMysql(sql)


if __name__ == '__main__':
    main()
