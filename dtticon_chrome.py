'''
Desc:
Download icons from web site https://brandspace.deloitte.com.
Details please see also variable EntryURL defined in this program

Requirements:
1.It needs chromedriver as web driver which can be downloaded from site:
https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver
2.Module selenium is also required, you can perform commands below to install:
pip install selenium
3.Only for Deloitte employees to use because of the identification verify.
You have to enter into Deloitte intranet at first, for example via VPN.

Author:
Bodhi Wang (bodwang@deloitte.com.cn)
2017.9.25
'''
# coding utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException
import time, sys, os


def getHumanTime(sec):
    if sec >= 3600:  # Converts to Hours
        return '{0:d} hour(s)'.format(int(sec / 3600))
    elif sec >= 60:  # Converts to Minutes
        return '{0:d} minute(s)'.format(int(sec / 60))
    else:  # No Conversion
        return '{0:d} second(s)'.format(int(sec))


EntryURL="https://brandspace.deloitte.com/content/index/guid/image_library?search_term=&list_size=24&assettag%5B17%5D%5B%5D=46"

entryWaitSecs = 5
downloadWaitSecs= 0.5
count = 0
percent = 0.3
filesPerPage = 24

start = time.time()

try:
    driver = webdriver.Chrome()
except Exception as e:
    print("Failed to load Chrome webdriver:{0}".format(str(e)))
    sys.exit(1)

try:
    driver.get(EntryURL)
except Exception as e:
    print("Failed to get entryURL:{0}".format(str(e)))
    driver.close()
    sys.exit(1)

try:
    login = driver.find_element_by_link_text("Deloitte professional")
    print(login.text)
    print("login click...")
    login.click()
    print("login click... done")
except Exception as e:
    print("Failed to fetch login:{0}".format(str(e)))
    sys.exit(1)

time.sleep(entryWaitSecs)
try:
    if driver.current_url != EntryURL:
        driver.get(EntryURL)
except Exception as e:
    print("Failed to enter entry URL:{0}".format(str(e)))
    sys.exit(1)

if driver.current_url != EntryURL:
    print("current URL {0} is not EntryURL".format(driver.current_url))
    driver.close()
    sys.exit(1)

try:
    driver.refresh()
    time.sleep(downloadWaitSecs)
    total = int(driver.find_elements(By.CLASS_NAME, "summary")[0].text.split()[3])
    print("total {0} files reported by summary page.".format(total))
except Exception as e:
    print("Failed to fetch summary information:{0}".format(str(e)))
    sys.exit(1)

errind = 0
maxicons = total * (1 + percent)
while count <= maxicons:
    try:
        downloadx = list()
        downloads = list()
        downloadx = driver.find_elements_by_class_name("download")
        downloads = [download for download in downloadx if download.text == 'Download file']
        files = downloads.__len__()
    except Exception as e:
        print("Failed to fetch download {0}".format(str(e)))
        continue

    for download in downloads:
        if download.text != "Download file":
            print("download {0} ignored.".format(download.text, str(e)))
            continue

        print("download {0}|{1}...".format(total, count+1))

        try:
            download.click()
            count += 1
            print("download {0}|{1}...done".format(total,count))
        except Exception as e:
            print("Failed to fetch download elements:{0}".format(str(e)))
            print("download {0}|{1}...cancelled".format(total, count+1))
            continue

        time.sleep(downloadWaitSecs)

    # Check if the last page arrives.
    if files < filesPerPage:
        print("There're only {0} files to download in current page.".format(files))
        break

    # After current page has been processed:
    try:
        nexts = list()
        nexts = driver.find_elements(By.CLASS_NAME, "next")
    except Exception as e:
        print("Failed to fetch download elements:{0}".format(str(e)))
        errind = 1
        break

    if nexts.__len__() > 0:
       try:
           nexts[0].click()
       except ElementNotVisibleException as e:
           print("No more resources to download:{0}".format(str(e)))
           break
       except Exception as e:
           print("Failed to fetch download elements:{0}".format(str(e)))
           errind = 1
           break

    time.sleep(downloadWaitSecs)

end = time.time()
print("success to perform {0} click times to download total files {1}.".format(count, total))
print("Elapsed time {0}".format(getHumanTime(end - start)))
try:
    driver.close()
except Exception as e:
    pass
sys.exit(errind)