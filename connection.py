import json

import psycopg2
import os
import pandas as pd

password = os.environ['Password']
user = os.environ['usernameDatabase']
connection_string = "dbname=orcid user={u} password={p} host=10.3.1.14".format(u=user, p=password)

def _records(query):
    con = psycopg2.connect(connection_string)
    cur = con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    return records

#list = _records("select distinct keywords_name from profile_keyword")
list = _records("with report as(select keywords_name,count(*) as  frequency from profile_keyword  group by keywords_name order by frequency desc) select keywords_name from report where frequency>10 and keywords_name not LIKE''")
def print_list(list):
    with open("distinct_keywords.json", "w", encoding="utf-8") as file_object:
        list_out = []
        for tup in list:
            for a in tup:
                list_out.append(a)

        file_object.write(json.dumps(list_out))

print_list(list)
