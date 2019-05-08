# coding=utf-8
from selenium import webdriver
from time import sleep



accout = 'tongxiaolong'
password = 'gmcc5678'


while True:
    browser = webdriver.Chrome(executable_path='E:/chromedriver.exe')
    browser.implicitly_wait(5)
    browser.get('https://auth.nfjd.gmcc.net/')
    browser.find_element_by_xpath("/html/body/blockquote/form/table/tbody/tr[4]/td[1]/table/tbody/tr[1]/td[3]/input").send_keys(accout)
    browser.find_element_by_xpath("/html/body/blockquote/form/table/tbody/tr[4]/td[1]/table/tbody/tr[2]/td[3]/input").send_keys(password)
    browser.find_element_by_xpath("/html/body/blockquote/form/table/tbody/tr[4]/td[1]/table/tbody/tr[5]/td[3]/input").click()
    browser.find_element_by_xpath('//*[@id="DSIDConfirmForm"]/blockquote/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input[1]').click()
    sleep(12000)
    browser.close()
