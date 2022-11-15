import os
from urllib.parse import quote

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


def get_reasearch_gate_links(orcid):
    list_name = _records(orcid)
    list_name2 = unique_list([i[0] for i in list_name])
    top_5 = []
    for i in list_name2[:5]:
        top_5.append('https://www.researchgate.net/search/publication?q=' + quote('"'+i+'"'))

    return top_5


