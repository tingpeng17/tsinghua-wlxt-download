#-*- coding:utf8 -*-
# 导入selenium2中的webdriver库
import time
import os
from selenium.webdriver.support.select import Select
from selenium import webdriver
from bs4 import BeautifulSoup
def login(options):
    global username,password
    driver = webdriver.Chrome(chrome_options=options) 
    # 打开一个页面
    driver.get("http://learn.tsinghua.edu.cn")
    # 模拟输入和点击按钮提交
    time.sleep(0.2)
    driver.find_element_by_name('i_user').clear()
    driver.find_element_by_name('i_user').send_keys(username)
    driver.find_element_by_name('i_pass').clear()
    driver.find_element_by_name('i_pass').send_keys(password)   #password
    driver.find_element_by_id('loginButtonId').click()
    time.sleep(0.2)
    return driver
def find_courses(driver):
    driver.switch_to.window(driver.window_handles[-1]) 
    time.sleep(0.2)
    driver.get("http://learn.tsinghua.edu.cn/f/wlxt/index/course/student/")
    time.sleep(0.2)
    driver.find_element_by_id('profile2-tab').click()
    time.sleep(0.2)
    Select(driver.find_element_by_name('overtable_length')).select_by_value("-1")
    time.sleep(0.2)
    html=driver.page_source
    soup=BeautifulSoup(html,features='lxml')
    all_href=soup.find_all(target="_blank")
    all_href=all_href[2:]
    all_links=[l['href'] for l in all_href]
    names=[]
    for i in all_href:
        names.append(str(i).split("<")[-3].split(">")[-1])
    driver.quit()
    return all_links,names
def find_all_download_links():
     # 实例化出一个chrome浏览器 
    options = webdriver.ChromeOptions() 
    options.add_argument('headless')
    driver=login(options)
    all_links,names=find_courses(driver) 
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=login(options)
    all_download_links=[]
    for number in range(len(all_links)):
        driver.get("http://learn.tsinghua.edu.cn"+all_links[number])
        time.sleep(0.2)
        driver.find_element_by_id('wlxt_kczy_zy').click()
        time.sleep(0.2)
        html=driver.page_source
        soup=BeautifulSoup(html,features='lxml')
        href1=soup.find_all('tr',{'role':'row','class':'odd'})
        href2=soup.find_all('tr',{'role':'row','class':'even'})
        hrefs=[]
        for i in href1:
            hrefs.append(str(i).split("href=")[1].split("title")[0][1:-2])
        for i in href2:
            hrefs.append(str(i).split("href=")[1].split("title")[0][1:-2])
        for i in range(len(hrefs)):
            temp=str(hrefs[i]).split("amp;")
            hrefs[i]=""
            for j in temp:
                hrefs[i]=hrefs[i]+str(j)
        temp=[]
        for i in hrefs:
            time.sleep(0.2)
            driver.get("http://learn.tsinghua.edu.cn"+i)
            time.sleep(0.2)
            html=driver.page_source
            soup=BeautifulSoup(html,features='lxml')
            temp.append(soup.find_all('a',{'target':'_blank'}))
        links=[]
        for i in temp:
            for j in i:
                if "downloadUrl=" in str(j):
                    links.append(str(j['href']).split("downloadUrl=")[1].split("'")[0])
        all_download_links.append(links)
    driver.quit()
    return all_download_links,names
def download_homework():
    all_download_links,names=find_all_download_links()     
    for number in range(len(names)):
        download_url=os.getcwd()+'\{}\课程作业'.format(names[number])
        options = webdriver.ChromeOptions() 
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_url}
        options.add_experimental_option('prefs', prefs) 
        options.add_argument('headless')
        driver=login(options)
        for i in range(len(all_download_links[number])):
            with open("kczy_download_log.txt","a") as file:
                file.write('http://learn.tsinghua.edu.cn'+all_download_links[number][i])
                file.write("\n")
            print("正在下载"+'http://learn.tsinghua.edu.cn'+all_download_links[number][i])
            driver.get('http://learn.tsinghua.edu.cn'+all_download_links[number][i])  
            while True:
                n=0
                if os.path.isdir(download_url)==True:
                    for i in os.listdir(download_url):
                        if ".crdownload" in i:
                            n=n+1
                            time.sleep(0.2)
                    if n>0:
                        pass
                    else:
                        break
                else:
                    break
#        driver.quit()
def find_all_files_download_links():
     # 实例化出一个chrome浏览器 
    options = webdriver.ChromeOptions() 
    options.add_argument('headless')
    driver=login(options)
    all_links,names=find_courses(driver) 
    options = webdriver.ChromeOptions() 
    options.add_argument('headless')
    driver=login(options)
    all_files_download_links=[]
    for number in range(len(all_links)):
        driver.get("http://learn.tsinghua.edu.cn"+all_links[number])
        time.sleep(0.2)
        driver.find_element_by_id('wlxt_kj_wlkc_kjxxb').click()
        time.sleep(0.2)
        html=driver.page_source
        soup=BeautifulSoup(html,features='lxml')
        hrefs=soup.find_all('li')
        links=[]
        for i in range(len(hrefs)):
            if 'wjid' in str(hrefs[i]):
                links.append(str(hrefs[i]['wjid']))
        all_files_download_links.append(links)
    driver.quit()
    return all_files_download_links,names
def downloadfiles():
    all_download_links,names=find_all_files_download_links()     
    for number in range(len(names)):
        download_url=os.getcwd()+'\{}\课程文件'.format(names[number])
        options = webdriver.ChromeOptions() 
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory':download_url }
        options.add_experimental_option('prefs', prefs) 
        options.add_experimental_option('prefs', prefs) 
        options.add_argument('headless')
        driver=login(options)
        for i in range(len(all_download_links[number])):
            with open("kcwj_download_log.txt","a") as file:
                file.write('http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid='+all_download_links[number][i])
                file.write("\n")
            print("正在下载"+'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid='+all_download_links[number][i])
            driver.get('http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/downloadFile?sfgk=0&wjid='+all_download_links[number][i])
            while True:
                n=0
                if os.path.isdir(download_url)==True:
                    for i in os.listdir(download_url):
                        if ".crdownload" in i:
                            n=n+1
                            time.sleep(0.2)
                    if n>0:
                        pass
                    else:
                        break
                else:
                    break
#        driver.quit()
username=input("Please input your username:\n")
password=input("Please input your password:\n")
download_homework() 
downloadfiles()
print("\n\n下载完成！")
        #爬取所有的课程名称和课程的链接
#        windows = driver.current_window_handle #定位当前页面句柄
#        all_handles = driver.window_handles   #获取全部页面句柄
#        for handle in all_handles:          #遍历全部页面句柄
#            if handle != windows:          #判断条件
#                driver.switch_to.window(handle)    
#                break
#       #切换到新页面
