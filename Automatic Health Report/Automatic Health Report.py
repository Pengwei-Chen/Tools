import datetime
import os
import sys

directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'").replace("\\\\", "/") + "/"

# Check the log to report only once a day
log = open(directory + "Records.txt", "r", encoding = "utf-8")
for line in log:
    last_report = line.split("\t")
    if last_report[0] == str(datetime.date.today()):
        log.close()
        os.popen(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --connect 89.187.178.94_udp.ovpn').readlines()
        sys.exit()
log.close()

########################################################
headless = True # 是否无窗口启动浏览器
sfzx = "1" # 今日是否在校
campus = "海宁校区" # 所在校区
internship = 2 # 今日是否进行实习或实践
sqhzjkkys = 1 # 今日申领健康码的状态？
tw = "0" # 今日是否有发热症状（高于37.2 ℃）
sfcxzysx = 0 # 今日是否有涉及涉疫情的管控措施
sfjcbh = 0 # 是否有与新冠疫情确诊人员或密接人员有接触的情况?
sfqrxxss = 1 # 本人承诺
province = "浙江省" # 省
city = "嘉兴市" # 市
area = "浙江省 嘉兴市 海宁市" # 省 市 区
address = "浙江省嘉兴市海宁市硖石街道浙江大学海宁国际校区"
geo_api_info = "{\"type\":\"complete\",\"position\":{\"Q\":30.5183460829,\"R\":120.72932617187502,\"lng\":120.729326,\"lat\":30.518346},\"location_type\":\"html5\",\"message\":\"Get geolocation success.Convert Success.Get address success.\",\"accuracy\":40,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"0573\",\"adcode\":\"330481\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"\u6d77\u5dde\u4e1c\u8def\",\"streetNumber\":\"718\u53f7\",\"country\":\"\u4e2d\u56fd\",\"province\":\"\u6d59\u6c5f\u7701\",\"city\":\"\u5609\u5174\u5e02\",\"district\":\"\u6d77\u5b81\u5e02\",\"towncode\":\"330481004000\",\"township\":\"\u7856\u77f3\u8857\u9053\"},\"formattedAddress\":\"\u6d59\u6c5f\u7701\u5609\u5174\u5e02\u6d77\u5b81\u5e02\u7856\u77f3\u8857\u9053\u6d59\u6c5f\u5927\u5b66\u6d77\u5b81\u56fd\u9645\u6821\u533a\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}" # 定位信息
########################################################

import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome
import requests
import re
import zipfile
import winreg
import subprocess
# import easyocr
# import pyautogui

# # Check background to prevent lock screen
# # Code image may not be available if the screen is locked
# position = None
# try:
#     postion = pyautogui.locateOnScreen(directory + "Background.png")
# # Screenshot raise OSError when the screen is locked
# except OSError as e:
#     pass
# while postion == None:
#     try:
#         postion = pyautogui.locateOnScreen(directory + "Background.png")
#     except OSError as e:
#         pass
#     time.sleep(0.1)

def get_chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    _v= winreg.QueryValueEx(key, 'version')[0]
    return _v

def get_driver_version():
    outstd = str(subprocess.Popen('chromedriver --version',
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE).stdout.readline())
    return outstd.split(' ')[1]

def get_version_list(url):
    rep = requests.get(url).text
    version_list = re.compile(r'<Key>(\d+\.\d+\.\d+\.\d+)/chromedriver_win32.zip</Key>').findall(rep)
    return version_list

def get_version_list_from_mirror(url):
    rep = requests.get(url).text
    version_list = re.compile(r'"name":"(\d+\.\d+\.\d+\.\d+)/"').findall(rep)
    return version_list

def download_driver(download_url):
    file = requests.get(download_url)
    with open(directory + "chromedriver.zip", 'wb') as zip_file:
        zip_file.write(file.content)

def unzip_driver(path):
    f = zipfile.ZipFile(directory + "chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, path)

def clear_window():
    # 找到Python安装目录下\Lib\site-packages\selenium\webdriver\common
    # 打开service.py，找到第76行：
    # 把原来的stdin=PIPE) 改成
    # stdin=PIPE,creationflags=134217728)
    # 这一步是为了完全关闭运行时的命令行窗口
    outstd = str(subprocess.Popen('where python',
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE).stdout.readline())
    service = outstd.lstrip("b'").rstrip(r"python.exe\\r\\n'").replace(
        r"\\", "/") + "/Lib/site-packages/selenium/webdriver/common/service.py"
    file_data = ""
    with open(service, "r") as f:
        for line in f:
            line = line.replace("stdin=PIPE)", "stdin=PIPE,creationflags=134217728)").replace(
                "creationflags=self.creationflags)", "creationflags=134217728)")
            file_data += line
    with open(service, "w") as f:
        f.write(file_data)
    return

url = "https://chromedriver.storage.googleapis.com/"
url_mirror = "https://registry.npmmirror.com/-/binary/chromedriver/"
index_url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
save_url = "https://healthreport.zju.edu.cn/ncov/wap/default/save"
chrome_version = get_chrome_version()
os.environ["PATH"] = os.environ.get("PATH") + ";" + directory.rstrip("/").replace("/", "\\") + ";"
try:
    driver_version = get_driver_version()
except IndexError:
    driver_version = ""
if driver_version != chrome_version:
    try:
        version_list = get_version_list(url)
    except:
        url = url_mirror
        version_list = get_version_list_from_mirror(url)
    if chrome_version not in version_list:
        version_list.append(chrome_version)
        version_list = sorted(version_list)
        chrome_version = version_list[version_list.index(chrome_version) - 1]
    download_url = url + chrome_version + '/chromedriver_win32.zip'
    download_driver(download_url)
    path = directory
    unzip_driver(path)
    clear_window()

try:
    options = Options()
    if headless:
        options.add_argument("--headless")
    # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"')
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = Chrome(options = options)
    browser.get(index_url)
    browser.implicitly_wait(10)

    def decrypt(string):
        decrypted = ""
        for character in string:
            decrypted += chr(ord(character) - 5)
        return decrypted

    # Login
    login_infomation = open(directory + "Login Information.txt", "r")
    username = decrypt(login_infomation.readline().rstrip())
    password = decrypt(login_infomation.readline())
    login_infomation.close()
    browser.find_element(By.NAME, "username").send_keys(username)
    browser.find_element(By.NAME, "password").send_keys(password)
    browser.find_element(By.ID, "dl").click()

    # # Recognize and input verification code
    # browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/span/img").screenshot(directory + "code.png")
    # reader = easyocr.Reader(["en"])
    # result = reader.readtext(directory + "code.png")
    # verification_code = result[0][1].replace(" ", "").replace("~", "")

    html = browser.page_source
    old_info = json.loads(re.findall(r'oldInfo: ({[^\n]+})', html)[0])
    def_info = json.loads(re.findall(r'def = ({[^\n]+})', html)[0])
    id = def_info['id']
    name = re.findall(r'realname: "([^\"]+)",', html)[0]
    number = re.findall(r"number: '([^\']+)',", html)[0]

    info = old_info.copy()
    info['id'] = id
    info['name'] = name
    info['number'] = number
    today = datetime.date.today()
    info["date"] = "%4d%02d%02d" % (today.year, today.month, today.day)
    info["created"] = round(time.time())
    info['jcqzrq'] = ""
    info['gwszdd'] = ""
    info['szgjcs'] = ""
    info['zgfx14rfhsj'] = ""
    del info['created_uid']
    # del info['jrdqtlqk']

    info["sfzx"] = sfzx
    info["campus"] = campus
    info["internship"] = internship
    info["sqhzjkkys"] = sqhzjkkys
    info["tw"] = tw
    info["sfcxzysx"] = sfcxzysx
    info["sfjcbh"] = sfjcbh
    info["sfqrxxss"] = sfqrxxss
    info["province"] = province
    info["city"] = city
    info["area"] = area
    info["address"] = address
    info["geo_api_info"] = geo_api_info
    info["verifyCode"] = ""
    # info["verifyCode"] = verification_code

    response = browser.request("POST", save_url, data = info).json()

    # while "验证码错误" in response["m"]:
    #     code_image = browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/span/img")
    #     code_image.click()
    #     code_image.screenshot("code.png")
    #     reader = easyocr.Reader(["en"])
    #     result = reader.readtext("code.png")
    #     verification_code = result[0][1].replace(" ", "").replace("~", "")
    #     response = browser.request("POST", save_url, data = info).json()

    # Log
    log = open(directory + "Records.txt", "a", encoding = "utf-8")
    log.write("\n" + str(datetime.date.today()) + "\t" + str(response))
    log.close()
    
except Exception as e:
    try:
        browser.close()
        browser.quit()
    except:
        pass
    raise e

# Close
browser.close()
browser.quit()

# Connect to VPN Service
os.popen(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --connect 89.187.178.94_udp.ovpn').readlines()