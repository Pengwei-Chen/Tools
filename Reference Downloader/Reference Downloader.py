from selenium import webdriver
import requests
import re
import os
import zipfile
import winreg
import sys

directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'").replace("\\\\", "/") + "/"



###########################################################################################
#Article Title"
article_title = input()
while True:
    line = input()
    if line == "":
        break
    article_title += " " + line

#Downloads Folder
downloads_folder = directory + article_title
###########################################################################################



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
prefs = {"download.default_directory" : downloads_folder}
options.add_extension(directory + "Scopus Document Download Manager_3.20_0.crx")
options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(options = options)
browser.get("https://www.scopus.com/search/form.uri?display=basic#basic")
browser.implicitly_wait(15)

els_input = browser.find_element_by_class_name("els-input")
els_input.click()
els_input.find_element_by_class_name("flex-grow-1").send_keys(article_title)
browser.find_element_by_class_name(
    "DocumentSearchForm-module__1S2LH").find_elements_by_class_name(
        "DocumentSearchForm-module__1S2LH")[1].find_elements_by_tag_name("button")[2].click()
ddmDocTitle = browser.find_element_by_class_name("ddmDocTitle")
if ddmDocTitle.text == article_title:
    ddmDocTitle.click()
    browser.find_element_by_id("referenceSrhResults").click()
    browser.find_element_by_xpath('//*[@id="resultsPerPage-button"]/span[1]').click()
    browser.find_element_by_id("ui-id-4").click()
    browser.find_element_by_id("selectAllCheck").click()
    browser.find_element_by_xpath('//*[@id="btnToolbar"]/span/micro-ui/scopus-search-results-download/els-button').click()
    browser.find_element_by_id("btnDDMDownloadStart").click()
