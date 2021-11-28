from selenium import webdriver
from pyshadow.main import Shadow
import requests
import re
import os
import zipfile
import winreg
import sys
import subprocess

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
    outstd = str(subprocess.Popen('chromedriver --version',
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE).stdout.readline())
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
    outstd = str(subprocess.Popen('where chromedriver',
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE).stdout.readline())
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
prefs = {"download.default_directory" : downloads_folder.replace("/", "\\")}
options.add_extension(directory + "Scopus Document Download Manager_3.20_0.crx")
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options = options)
driver.get("https://www.scopus.com/search/form.uri?display=basic#basic")
driver.implicitly_wait(10)

els_input = driver.find_element_by_class_name("els-input")
els_input.click()
els_input.find_element_by_class_name("flex-grow-1").send_keys(article_title)
driver.find_element_by_xpath('//*[@id="documents-tab-panel"]/div/form/div[2]/div[2]/button').click()
while True:
    ddmDocTitle = driver.find_element_by_xpath('//*[@id="resultDataRow0"]/td[1]/a')
    if ddmDocTitle.text != "":
        break
if ddmDocTitle.text == article_title:
    ddmDocTitle.click()
    driver.find_element_by_xpath('//*[@id="referenceSrhResults"]/span[1]').click()
    try:
        driver.find_element_by_xpath('//*[@id="resultsPerPage-button"]/span[1]').click()
    except:
        driver.find_element_by_xpath('//*[@id="referenceSrhResults"]/span[1]').click()
        driver.find_element_by_xpath('//*[@id="resultsPerPage-button"]/span[1]').click()
    driver.find_element_by_id("ui-id-4").click()
    driver.find_element_by_id("selectAllCheck").click()
    driver.find_element_by_xpath('//*[@id="btnToolbar"]/span/micro-ui/scopus-search-results-download/els-button').click()
    start_button = driver.find_element_by_id("btnDDMDownloadStart")
    while start_button.get_attribute('disabled') != "true":
        try:
            start_button.click()
        except:
            pass
    main_window_handle = driver.current_window_handle
    driver.execute_script('window.open()')
    all_window_handles = driver.window_handles
    for window_handle in all_window_handles:
        if window_handle != main_window_handle:
            driver.switch_to.window(window_handle)
            driver.get("chrome://settings/content/pdfDocuments")
            shadow = Shadow(driver)
            shadow.find_element("#radioCollapse").click()
    driver.close()
    driver.switch_to.window(main_window_handle)
    while True:
        if driver.find_element_by_xpath('//*[@id="btnDDMDownloadComplete"]/span').text == "Done":
            publisher_sites = driver.find_elements_by_xpath('//*[@id="ddmVAPStatus"]/a')
            publisher_sites = publisher_sites[:-1]
            for i in range(len(publisher_sites)):
                publisher_sites[i] = publisher_sites[i].get_attribute("href")
            driver.implicitly_wait(1)
            for publisher_site in publisher_sites:
                driver.execute_script('window.open("' + publisher_site+ '")')
            all_window_handles = driver.window_handles
            for window_handle in all_window_handles:
                if window_handle != main_window_handle:
                    driver.switch_to.window(window_handle)
                    try:
                        link = driver.find_element_by_xpath('//*[@id="screen-reader-main-content"]/div[2]/div[1]/ul/li[1]/a').get_attribute("href")
                        driver.get(link)
                    except:
                        pass
            break
