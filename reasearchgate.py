import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote
import cloudscraper

import psycopg2

password = os.environ['Password']
user = os.environ['usernameDatabase']
connection_string = "dbname=orcid user={u} password={p} host=10.3.1.14".format(u=user, p=password)


def _records(orcid):
    con = psycopg2.connect(connection_string)
    cur = con.cursor()
    query = f"select title  from work w where w.orcid = '{orcid}'  order by date_created desc limit 10"
    cur.execute(query)
    records = cur.fetchall()
    return records


def unique_list(x):
    return list(dict.fromkeys(x))

def extract_source(url):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    info = scraper.get(url).text
    return info

def get_reasearch_gate_links(orcid):
    list_name = _records(orcid)
    list_name2 = unique_list([i[0] for i in list_name])
    top_5 = []
    for i in list_name2[:5]:
        top_5.append(('https://www.researchgate.net/search/publication?q=' + quote('"'+i+'"'),i))

    return top_5

def get_abstract(top5):
    list = []
    if len(top5)==0:
        return list
    for i in top5:
        try:
            driver = webdriver.Edge()
            driver.get(i[0])
            time.sleep(2)
            link = driver.find_element(By.PARTIAL_LINK_TEXT,i[1])
            desired_link = link.get_attribute('href')
            print(desired_link)
            driver.get(desired_link)
            abstract=driver.find_element(By.XPATH,"//div[contains(@class,'abstract')]")
            list.append(abstract.text)
        except Exception as e:
            print('some error fetching abstract' +str(e))
    driver.close()
    return list


links = get_reasearch_gate_links('0000-0001-7387-9210')
print(*links,sep='\n')
print(*get_abstract(links),sep='\n')

# print()
