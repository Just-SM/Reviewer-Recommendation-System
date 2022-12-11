import argparse
from multiprocessing import Pool
import psycopg2
import json

def _get_Name(orcid):
    # print('et_user_data_by_orcid:   Getting Name')
    connection = psycopg2.connect(user="confeval",
                        password="C0nfeval2022#",
                        host="10.3.1.14",
                        port="5432",
                        database="orcid")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    cursor.execute(f"SELECT given_names,family_name FROM record_name where orcid = '{orcid}' ;")
    res = cursor.fetchall()
    if len(res) == 0:
        return 1,None
    else:
        return 1,res[0][0] +" "+ res[0][1]


def _get_Aff(orcid):
    # print("get_user_data_by_orcid:   Getting aff")
    connection = psycopg2.connect(user="confeval",
                        password="C0nfeval2022#",
                        host="10.3.1.14",
                        port="5432",
                        database="orcid")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    cursor.execute(f"SELECT name from org where id in (SELECT org_id FROM org_affiliation_relation where orcid = '{orcid}' and org_affiliation_relation_role = 'employment' and end_year is null LIMIT 1) limit 1")
    res = cursor.fetchall()
    if len(res) == 0:
        return 2,None
    else:
        return 2,res[0][0]


def _get_Kwords(orcid):
    # print("get_user_data_by_orcid:   Getting kwords")
    connection = psycopg2.connect(user="confeval",
                        password="C0nfeval2022#",
                        host="10.3.1.14",
                        port="5432",
                        database="orcid")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    cursor.execute(f"SELECT keywords_name FROM profile_keyword where orcid = '{orcid}' LIMIT 5;")
    res = cursor.fetchall()
    if len(res) == 0:
        return 3,None
    else:
        return 3,[x[0] for x in res]


def _get_Titles(orcid):
    # print("get_user_data_by_orcid:   Getting titles")
    connection = psycopg2.connect(user="confeval",
                        password="C0nfeval2022#",
                        host="10.3.1.14",
                        port="5432",
                        database="orcid")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    cursor.execute(f"select title from work w where w.orcid = '{orcid}'  order by date_created desc limit 10")
    res = cursor.fetchall()
    if len(res) == 0:
        return 4,None
    else:
        return 4,res

class Result():
    def __init__(self):
        self.val = {1:None,2:None,3:None,4:None}

    def update_result(self, val):
        self.val[val[0]] = val[1]

    def get_formated(self):
        return json.dumps(self.val)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("orcid")

    args = parser.parse_args()

    with Pool(4) as pool:
        result = Result()
        result.update_result((0,args.orcid))
        # multiple_results = [pool.apply_async(_get_Name,args=(args.orcid,))]
        multiple_results = [pool.apply_async(_get_Name,args=(args.orcid,),callback=result.update_result),pool.apply_async(_get_Kwords,(args.orcid,),callback=result.update_result),pool.apply_async(_get_Titles,(args.orcid,),callback=result.update_result),pool.apply_async(_get_Aff,(args.orcid,),callback=result.update_result)]
        try:
            results = [res.get(timeout=40) for res in multiple_results]
            # print(results)
            print(result.get_formated())
        except:
            print(result.get_formated())
