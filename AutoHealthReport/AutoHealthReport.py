from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import requests
import re
import os
import zipfile
import winreg
import sys

##########################
#Enter your username here#
username = "3190110642"

#Enter your password here#
password = "123456789"

#Enter your location here (optional)#
province = "浙江省"
city = "嘉兴市"
area = "海宁市"

#*sfyxjzxgym是否意向接种
#*sfbyjzrq是否是不宜接种人群
#*jzxgymqk当前接种情况
#sffrqjwdg今日是否因发热请假未到岗（教职工）或未返校（学生）
#sfqtyyqjwdg今日是否因发热外的其他原因请假未到岗（教职工）或未返校（学生）
#tw今日是否有发热症状（高于37.2 ℃）
#sfyqjzgc今日是否被当地管理部门要求在集中隔离点医学观察
#sfcyglq今日是否居家隔离观察（居家非隔离状态填否）
#sfcxzysx是否有任何与疫情相关的，值得注意的情况
#sfsqhzjkk是否已经申领校区所在地健康码
#sqhzjkkys今日申领校区所在地健康码的颜色
#*sfzx今日是否在校
#sfzgn所在地点
#no need to check for 所在地点（请打开手机位置功能，并在手机权限设置中选择允许访问位置信息）
#*sfymqjczrj本人家庭成员(包括其他密切接触人员)是否有近14日入境或近14日拟入境的情况
#no need to check for 本人承诺
option = [[] for i in range(6)]
option[1] = ["sfyxjzxgym", "sfsqhzjkk","sqhzjkkys", "sfzx", "sfzgn"]
option[2] = ["jzxgymqk", "sffrqjwdg", "sfqtyyqjwdg", "tw", "sfyqjzgc", "sfcyglq", "sfcxzysx", "sfymqjczrj"]
option[3] = []
option[4] = []
option[5] = ["sfbyjzrq"]
##########################


directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'").replace("\\\\", "/") + "/"

def get_chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    _v= winreg.QueryValueEx(key, 'version')[0]
    return _v

def get_driver_version():
    outstd = os.popen('chromedriver --version').read()
    return outstd.split(' ')[1]

def get_version_list(url):
    rep = requests.get(url).text
    version_list = []
    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)
    for i in result:
        version = re.compile(r'.*?/').findall(i)[0][:-1]
        version_list.append(version)
    return version_list

def get_path():
    outstd = os.popen('where chromedriver').read()
    return outstd.strip('chromedriver.exe\n')

def download_driver(download_url):
    file = requests.get(download_url)
    with open(directory + "chromedriver.zip", 'wb') as zip_file:
        zip_file.write(file.content)

def unzip_driver(path):
    f = zipfile.ZipFile(directory + "chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, path)

url = 'http://npm.taobao.org/mirrors/chromedriver/'
chrome_version = get_chrome_version()
driver_version = get_driver_version()
if driver_version != chrome_version:
    version_list = get_version_list(url)
    if chrome_version not in version_list:
        version_list.append(chrome_version)
        version_list = sorted(version_list)
        chrome_version = version_list[version_list.index(chrome_version) - 1]
    download_url = url + chrome_version + '/chromedriver_win32.zip'
    download_driver(download_url)
    path = get_path()
    unzip_driver(path)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options = options)
browser.get("https://healthreport.zju.edu.cn/ncov/wap/default/index")
browser.implicitly_wait(5)

#Login
browser.find_element_by_name("username").send_keys(username)
browser.find_element_by_name("password").send_keys(password)
browser.find_element_by_id("dl").click()

#Report
option[0] = ["sfqrxxss"] #Agreement at the end, no need to change

for i in range(1, len(option)):
    for j in range(len(option[i])):
        browser.find_element_by_name(option[i][j]).find_elements_by_tag_name("span")[2*i-1].click()

for i in range(len(option[0])):
    browser.find_element_by_name(option[0][i]).find_elements_by_tag_name("span")[0].click()

def getArea():
    selection = browser.find_element_by_name("area")
    selection.click()
    start_time = time.time()
    while True:
        if selection.find_element_by_tag_name("input").get_attribute("value") != "":
            break
        elif time.time() - start_time >= 20:
            browser.find_element_by_class_name("wapat-btn-ok").click()
            Select(browser.find_element_by_class_name("hcqbtn-danger")).select_by_value(province)
            Select(browser.find_element_by_class_name("hcqbtn-warning")).select_by_value(city)
            Select(browser.find_element_by_class_name("hcqbtn-primary")).select_by_value(area)
            break
        time.sleep(1)
getArea()

browser.find_element_by_class_name("list-box").find_element_by_class_name("footers").find_elements_by_tag_name("a")[0].click()

try:
    confirm = browser.find_element_by_class_name("wapcf-btn-ok")
    confirm.click()
except:
    pass

#Close
browser.quit()
