# coding:utf-8
# @File : spider.py
# @Author : Leoren
# @Date : 2019/3/18  9:53
# @Desc :  抓取微信文章

from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError


base_url = 'https://weixin.sogou.com/weixin?'

keyword = '风景'

header = {
    'Cookie': 'IPLOC=CN1401; SUID=0322313B1810990A000000005C8EF910; SUV=1552873744268244; ABTEST=6|1552873745|v1; SNUID=8CADBEB4909514DB088DB0FA90BC0E2B; weixinIndexVisited=1; JSESSIONID=aaa3m6BMGj77s4jDjH-Lw; ppinf=5|1552873799|1554083399|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTUlQjElQjElRTglOEQlQUYlRTglOUIlOEIlRTUlQUQlOTB8Y3J0OjEwOjE1NTI4NzM3OTl8cmVmbmljazozNjolRTUlQjElQjElRTglOEQlQUYlRTglOUIlOEIlRTUlQUQlOTB8dXNlcmlkOjQ0Om85dDJsdUNKd1UwcnBVRGczRlg3WXQ1TjZWZDRAd2VpeGluLnNvaHUuY29tfA; pprdig=DKQ69qpET-VnkEvGYMQQjAFDw7h3A1SU4PKVenPVP1YQUtZBGzWRf-nwHAt2sX8TPaiwg_TqkcjqSgFZI53r8ZZUjxiv1U9AtTT4Y8g2irocRj9O00gkP99d7Gy-4FIHoNuZYEFUShDbNnnSBUP91jMY4mPkEfu-RdoRBKRrh08; sgid=27-39737075-AVyOibUfSTrFw0WAG6TdTdQk; ppmdig=1552873799000000eec52864667f8e179ba4046cdfbe1f19; sct=2',
    'Host': 'weixin.sogou.com',
    'Ugrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}

proxy_pool_url = 'http://127.0.0.1:5000/get'

proxy = None
max_count=5


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling ', url)
    print('Trying Count', count)
    global proxy
    if count >= max_count:
        print('Tried Too Much')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=header, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=header)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page':page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        print(html)


if __name__ == '__main__':
    main()


