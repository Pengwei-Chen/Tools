from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options = options)
browser.get("https://healthreport.zju.edu.cn/ncov/wap/default/index")

#Login
browser.find_element_by_name("username").send_keys(
    #Enter your username here#
    ""
)
browser.find_element_by_name("password").send_keys(
    #Enter your password here#
    ""
)
browser.find_element_by_id("dl").click()

#Report
keywordsSp = ["sfqrxxss"]
keywordsYes = ["sfzgn", "sfzx"]
keywordsNo = ["sffrqjwdg", "sfymqjczrj", "zgfx14rfh", "sfcxzysx", "sfhsjc", "jrsfqzfy",
"jrsfqzys", "sfcyglq", "sfyqjzgc", "sfjcqz", "sfjcbh","sfcxtz", "tw", "sfqtyyqjwdg"]

for i in range(len(keywordsNo)):
    selection = browser.find_element_by_name(keywordsNo[i])
    selection.find_elements_by_tag_name("span")[3].click()

selection = browser.find_element_by_name("sfsqhzjkk")
selection.find_elements_by_tag_name("span")[1].click()
selection = browser.find_element_by_name("sqhzjkkys")
selection.find_elements_by_tag_name("span")[1].click()

for i in range(len(keywordsYes)):
    selection = browser.find_element_by_name(keywordsYes[i])
    selection.find_elements_by_tag_name("span")[1].click()

selection = browser.find_element_by_name("sfqrxxss")
selection.find_elements_by_tag_name("span")[0].click()

def getArea():
    selection = browser.find_element_by_name("area")
    selection.click()
    while True:
        if selection.find_elements_by_tag_name("input")[0] != "":
            break
getArea()

selection = browser.find_element_by_class_name("list-box")
selection.find_element_by_class_name("footers").find_elements_by_tag_name("a")[0].click()

try:
    confirm = browser.find_element_by_class_name("wapcf-btn-ok")
    confirm.click()
except:
    pass

#Close
browser.quit()

