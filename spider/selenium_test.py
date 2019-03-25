# coding:utf-8
# @File : selenium_test.py
# @Author : Leoren
# @Date : 2019/3/10  9:34
# @Desc :

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


browser = webdriver.Chrome()
# browser2 = webdriver.Firefox()
# browser3 = webdriver.Edge()
# browser4 = webdriver.Safari()
# browser5 = webdriver.PhantomJS()
# try:
#     browser.get('https://www.taobao.com')
#     input = browser.find_element_by_id('q')
#     input.send_keys('Python')
#     input.send_keys(Keys.ENTER)
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
#     print(browser.current_url)
#     print(browser.get_cookies())
#     print(browser.page_source)
# finally:
#     browser.close()

# browser.get('https://taobao.com')
# input = browser.find_element_by_id('q')
# input.send_keys('iPhone')
# time.sleep(1)
# input.clear()
# input.send_keys('iPad')
# button = browser.find_element_by_class_name('btn-search')
# button.click()

browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
