from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options = options)
browser.get("https://healthreport.zju.edu.cn/ncov/wap/default/index")

#Login
browser.find_element_by_name("username").send_keys(
    #Enter your username here#
    "3190110642"
)
browser.find_element_by_name("password").send_keys(
    #Enter your password here#
    "123456789"
)
browser.find_element_by_id("dl").click()

#Report
option = []
for i in range(6):
    option.append([])

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

option[1] = ["sfyxjzxgym", "sfsqhzjkk","sqhzjkkys", "sfzx", "sfzgn"]
option[2] = ["sffrqjwdg", "sfqtyyqjwdg", "tw", "sfyqjzgc", "sfcyglq", "sfcxzysx", "sfymqjczrj"]
option[3] = ["jzxgymqk"]
option[4] = []
option[5] = ["sfbyjzrq"]

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
        if selection.find_elements_by_tag_name("input")[0].text != "":
            break
        elif time.time() - start_time >= 20:
            browser.find_element_by_class_name("wapat-btn-ok").click()
            Select(browser.find_element_by_class_name("hcqbtn-danger")).select_by_value("省")
            Select(browser.find_element_by_class_name("hcqbtn-warning")).select_by_value("市")
            Select(browser.find_element_by_class_name("hcqbtn-primary")).select_by_value("区")
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
