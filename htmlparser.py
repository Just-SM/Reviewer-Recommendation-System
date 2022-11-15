import os
from tqdm import tqdm
import psycopg2
import requests
from bs4 import BeautifulSoup

password = os.environ['Password']
user = os.environ['usernameDatabase']
connection_string = "dbname=orcid user={u} password={p} host=10.3.1.14".format(u=user, p=password)


def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source = requests.get(url, headers=headers)
    return source


def extract_para_scoupus(url):
    page = extract_source(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    section = soup.find(id='abstractSection')
    para = section.find('p').text
    return para


# def extract_para_doi(url):
#     page = extract_source(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     section = soup.find(id='abstractSection')
#     para = section.find('p').text
#     return para


def _records(query):
    con = psycopg2.connect(connection_string)
    cur = con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    return records


def get_abstract(orcid):
    # records = _records(f"select work_url,title  from work w where w.work_url like '%scopus%' and w.orcid ='{orcid}'")
    records = _records(f"select work_url,title from work w where w.work_url like '%scopus%' limit 6")
    return records


# print(get_abstract('0000-0003-1706-0205'))


def returnDictTitleAbstract(orcid):
    dict = {}
    list_of_records = get_abstract(orcid)
    for i in tqdm(list_of_records):
        try:
            print('===============')
            print(i)
            dict[i[1]] = extract_para_scoupus(i[0])
        except:
            dict[i[1]] = f'{i[1]}'
            print(f'Exception was casued at {i}')
            continue
    return dict

# print(returnDictTitleAbstract('11'))

temp = returnDictTitleAbstract(1)

for i,v in temp.items():
    print('*****************')
    print(i +' : '+v)
    print('*****************')

