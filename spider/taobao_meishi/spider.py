# coding:utf-8
# @File : spider.py
# @Author : Leoren
# @Date : 2019/3/10  16:09
# @Desc : 抓取淘宝商城的美食信息

import pymongo
from config import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)

# browser.set_window_size(1400, 900)


def search():
    print('正在搜索')
    try:
        browser.get('https://www.jd.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > div.form > button')))
        input.send_keys(KEYWORD)
        submit.click()
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        get_products()
        total_num = browser.find_element_by_css_selector('#J_bottomPage > span.p-skip > em:nth-child(1) > b')
        return total_num.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('翻页至', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > input'))
        )
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'),
                                                    str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#J_goodsList .gl-warp .gl-item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#J_goodsList .gl-warp .gl-item').items()
    for item in items:
        product = {
            'image': item.find('.p-img .err-product').attr('data-lazy-img'),
            'price': item.find('.p-price').text(),
            'title': item.find('.p-name').text(),
            'shop': item.find('.p-shop').text(),
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("save successful", result)
    except Exception:
        print("save failed", result)


def main():
    try:
        total = search()
        total = int(total)
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()



if __name__ == '__main__':
    main()
    


