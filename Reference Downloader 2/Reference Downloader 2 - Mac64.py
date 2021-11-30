import selenium
from selenium import webdriver
import requests
import re
import os
import zipfile
import sys
import subprocess
import time

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

#PDF Filename
#Available: title, first_author, first_author_surname, year
def generate_file_name(title, first_author, first_author_surname, year, journal):
    return year + "_" + first_author
###########################################################################################

for root, dirs, files in os.walk(downloads_folder):
    for file in files:
        os.remove(root + "/" + file)

def get_chrome_version():
    file = open("/Applications/Google Chrome.app/Contents/Info.plist", 'r')
    while True:
        line = file.readline()
        if line.strip() == "<key>KSVersion</key>":
            version = file.readline().strip().lstrip("<string>").rstrip("</string>")
            break
    return version

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

def download_driver(download_url):
    file = requests.get(download_url)
    with open(directory + "chromedriver.zip", 'wb') as zip_file:
        zip_file.write(file.content)

def unzip_driver(path):
    f = zipfile.ZipFile(directory + "chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, path)
    subprocess.Popen("chmod +x " + directory + "chromedriver",
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)

def rename(name1, name2, n):
    try:
        if n == 0:
            os.renames(name1, name2 + ".pdf")
        else:
            os.renames(name1, name2 + " (" + str(n) + ").pdf")
    except FileExistsError:
        rename(name1, name2, n + 1)
            

url = 'http://npm.taobao.org/mirrors/chromedriver/'
chrome_version = get_chrome_version()
os.environ["PATH"] = os.environ.get("PATH") + ":" + directory.rstrip("/")
print(os.environ["PATH"])
try:
    driver_version = get_driver_version()
except IndexError:
    driver_version = ""
if driver_version != chrome_version:
    version_list = get_version_list(url)
    if chrome_version not in version_list:
        version_list.append(chrome_version)
        version_list = sorted(version_list)
        chrome_version = version_list[version_list.index(chrome_version) - 1]
    download_url = url + chrome_version + '/chromedriver_mac64.zip'
    download_driver(download_url)
    path = directory
    unzip_driver(path)

options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : downloads_folder.replace("/", "\\")}
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
    references = driver.find_elements_by_class_name("refCont")
    time.sleep(0.3)
    references = driver.find_elements_by_class_name("refCont")
    papers = {}
    special_filename_to_half_doi = {}
    unavailable = []
    for reference in references:
        doi = re.search(r"doi: (.*)", reference.text)
        if doi != None:
            doi = doi.group(1).lower()
            splited_doi = doi.split("/")
            if len(splited_doi) == 3:
                doi = splited_doi[0] + "/" + splited_doi[1] + r"%252F" + splited_doi[2]
            doi = doi.replace("(", "%2528")
            doi = doi.replace(")", "%2529")
            half_doi = doi.split("/")[1].lower()
            title = reference.find_element_by_class_name("refDocTitle").find_element_by_tag_name("a").text
            if title == None:
                title = ""
            if len(title) > 50:
                title = title[0:50]
            first_author = re.search(r"(.*?,.*?),", reference.find_element_by_class_name("refAuthorTitle").text)
            if first_author == None:
                first_author = re.search(r"(.*?,.*?)\.", reference.find_element_by_class_name("refAuthorTitle").text)
            if first_author != None:
                first_author = first_author.group(1)
            else:
                first_author = ""
            first_author_surname = first_author.split(",")[0]
            year_and_journal = re.search(r"\((\d{4})\) (.*?),", reference.text)
            if year_and_journal != None:
                year = year_and_journal.group(1)
                journal = year_and_journal.group(2)
            else:
                year = ""
                journal = ""
            papers[half_doi] = [doi, title, first_author, first_author_surname, year, journal]
    for paper in list(papers.values()):
        driver.execute_script('window.open("https://sci.bban.top/pdf/' + paper[0] + '.pdf?download=true")')
    driver.implicitly_wait(0.5)
    time.sleep(5)
    while True:
        windows = driver.window_handles
        if len(windows) == 1:
            break
        for i in range(len(windows) - 1, 0, -1):
            try:
                window = windows[i]
                driver.switch_to.window(window)
                try:
                    if driver.find_element_by_xpath("/html/body/center[1]/h1").text == "404 Not Found":
                        new_url = "https://sci-hub.mksa.top/" + driver.current_url.lstrip("https://sci.bban.top/pdf/").rstrip('.pdf?download=true")')
                        new_url = new_url.replace(r"%252F", "/").replace("%2528", "(").replace("%2529", ")")
                        driver.get(new_url)
                        try:
                            driver.find_element_by_xpath('//*[@id="buttons"]/ul/li[2]/a').click()
                        except:
                            download_button = driver.find_element_by_xpath('//*[@id="buttons"]/button')
                            filename = re.search(r"/([A-Za-z0-9]+?).pdf", download_button.get_attribute("onclick"))
                            if filename != None:
                                filename = filename.group(1).lower()
                                half_doi = driver.current_url.lstrip("https://sci-hub.mksa.top/").split("/")[1].lower()
                                half_doi = half_doi.replace(r"%252F", "/").replace("%2528", "(").replace("%2529", ")")
                                special_filename_to_half_doi[filename] = half_doi
                            download_button.click()
                        driver.close()
                except:
                    pass
                try:
                    if driver.find_element_by_xpath('//*[@id="first"]/h1[1]/p[1]').text == "扫码关注公众号 可发布文献求助 并获取此篇文献":
                        new_url = "https://doi.org/" + driver.current_url.lstrip("https://sci-hub.mksa.top/")
                        new_url = new_url.replace(r"%252F", "/").replace("%2528", "(").replace("%2529", ")")
                        unavailable.append(new_url)
                        driver.close()
                except:
                    pass
            except selenium.common.exceptions.NoSuchWindowException:
                pass
    start_time = time.time()
    while time.time() - start_time <= 300:
        downloaded = True
        for root, dirs, files in os.walk(downloads_folder):
            if len(files) + len(unavailable) != len(papers):
                downloaded = False
                break
            for file in files:
                if re.search(r".crdownload", file) != None:
                    downloaded = False
                    break
        if downloaded:
            break
        time.sleep(0.3)
    for file in files:
        key = re.sub(r" \(\d+\)", "", file[:-4]).replace(r"%", r"%25").lower()
        information = papers.get(key)
        if information == None:
            information = papers.get(special_filename_to_half_doi.get(key))
        if information != None:
            rename(downloads_folder + "/" + file, downloads_folder + "/" + generate_file_name(information[1],
                                                information[2],information[3],information[4],information[5]), 0)
    if len(unavailable) != 0:
        file = open(downloads_folder + "/Unavailable.txt", "w")
        for url in unavailable:
            file.write(url + "\n")
        file.close()