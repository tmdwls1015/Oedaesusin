from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #현재 디렉토리

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox") #이거 안넣으면 오류나더라고
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu") #여기 세줄 추가하면 headless Chrome으로 켜짐

path = "C:/Users/User/Downloads/chromedriver" #크롬드라이버 path
os.environ["webdriver.chrome.driver"] = path
driver = webdriver.Chrome(path, chrome_options=options) # driver객체 실행 driver=브라우저라 생각하면 편함

latest_url = 'https://webs.hufs.ac.kr/src08/jsp/lecture/LECTURE2020L.jsp'
driver.get(latest_url)

data = {} #데이터 저장할 리스트

j = 1

html = driver.page_source #모든 페이지 소스를 가져올거야
soup = BeautifulSoup(html, 'html.parser')

while True:
    if j == 1:
        major_list = soup.select('body > div > form > div.table.write.margin_top30 > table > tbody > tr:nth-child(4) > td > div > select > option') #이부분이 서울캠퍼스 전공 70가지
    elif j == 2:
        driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[5]/th/label').click() #교양 라디오버튼
        major_list = soup.select('body > div > form > div.table.write.margin_top30 > table > tbody > tr:nth-child(5) > td > div > select > option') #이부분이 서울캠퍼스 교양 18가지
    elif j == 3:
        driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[3]/td/label[2]').click() #글로벌 라디오버튼
        driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[4]/th/label').click() #전공 라디오버튼
        major_list = soup.select('body > div > form > div.table.write.margin_top30 > table > tbody > tr:nth-child(4) > td > div > select > option') #이부분이 글로벌캠퍼스 전공 63가지
    elif j == 4:
        driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[5]/th/label').click() #교양 라디오버튼
        major_list = soup.select('body > div > form > div.table.write.margin_top30 > table > tbody > tr:nth-child(5) > td > div > select > option') #이부분이 글로벌캠퍼스 교양 16가지
    else:
        break
    driver.find_element_by_xpath('/html/body/div/form/div[2]/button').click() #조회(Search)버튼 클릭

    l = 1
    for ml in major_list:
        if j == 1 or j == 3:
            driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[4]/td/div/select/option['+str(l)+']').click()
        else:
            driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[5]/td/div/select/option['+str(l)+']').click()
        #req = requests.get(latest_url)
        html = driver.page_source #모든 페이지 소스를 가져올거야
        soup = BeautifulSoup(html, 'html.parser')
        #print(ml.text)

        classlist = soup.select('#premier1 > div > table > tbody > tr > td') #여기가 과목부분

        for cl in classlist:
            data[cl.text] = cl.get('text')
            with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
                json.dump(data, json_file)  #json파일로 저장하는부분
        l = l+1
        if j == 3 and l == 64:
            break
    j = j+1

# /html/body/div/form/div[1]/table/tbody/tr[3]/td/label[2] #글로벌캠퍼스 라디오버튼
# /html/body/div/form/div[1]/table/tbody/tr[5]/th/label #교양수업 라디오버튼
