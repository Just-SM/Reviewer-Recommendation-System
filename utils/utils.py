import pandas as pd
import psycopg2
import yake
from dataclasses import dataclass
from multiprocessing import Pool
import argparse
import json
import pandas as pd 
import yake
import gensim.downloader
import gensim
import numpy as np
from numpy.linalg import norm
import pandas as pd

def cosine(a,b):
    d = np.dot(a,b)
    na = norm(a)
    nb = norm(b)
    nanb = na*nb
    return d / nanb
euclidian = lambda a,b : norm(a-b)



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


@dataclass
class PersonData:

    name_surname:str
    orcid:str
    calc_kw:list
    given_kw:list
    affiliation: str

    def __init__(self,name = None,orcid = None ,given_kwords = None ,calc_kwords = None,aff = None) -> None:
        if name is None:
            self.name_surname = ""
        else:
            self.name_surname = name

        if orcid is None:
            self.orcid = ""
        else:
            self.orcid = orcid
        
        if given_kwords is None:
            self.given_kw = ['']
        else:
            self.given_kw = given_kwords
        
        if calc_kwords is None:
            self.calc_kw = ['']
        else:
            self.calc_kw = calc_kwords

        if aff is None:
            self.affiliation = ""
        else:
            self.affiliation = aff

    def is_full(self):
        return self.name_surname != '' and self.orcid != '' and len(self.calc_kw) > 0 and self.affiliation != ''
        
class Modelprovider:

    def __init__(self) -> None:

        self.kw_extractor = yake.KeywordExtractor(top=5,n=1)

        self.kwords = dict()


    def extract_kw(self,text):
        return self.kw_extractor.extract_keywords(text)

    def get_vectors(self,data):
        vectorised_data = []
        for sentence in data:
            sentence = sentence.replace("-"," ")
            words = sentence.split()
            sentence_vector = np.zeros([300])
            for word in words:
                try:
                    sentence_vector = sentence_vector + self.vect[word.lower()]
                except Exception:
                    sentence_vector = None
                    break
            vectorised_data.append(sentence_vector) 
        return vectorised_data

    def get_sum_vec(self,data):
        sum_vec1 = np.zeros([300])
        for vec in data:
            if vec is not None:
                sum_vec1 = sum_vec1 + vec
        
        return sum_vec1

    def get_weight_sum_vec(self,data,norm=0):
        sum_vec1 = np.zeros([300])
        for ind,vec in enumerate(data):
            if vec is not None:
                sum_vec1 = sum_vec1 + (vec * (1 - (norm * ind)))
        return sum_vec1

    def get_vec_rpr(self,data):
        title,keys,abstract = data

        kw_from_abstract = [words for words,val in self.kw_extractor.extract_keywords(abstract)]

        kw_from_keys = [word for word in keys.split('\n')]

        vec_abstract = self.get_vectors(kw_from_abstract)

        sum_vec_abstract = self.get_weight_sum_vec(vec_abstract,norm=0)

        vec_keys = self.get_vectors(kw_from_keys)

        sum_vec_keys = self.get_weight_sum_vec(vec_keys)

        return sum_vec_abstract,sum_vec_keys,sum_vec_abstract+sum_vec_keys

    def load_vectorizer(self):
        self.vect = gensim.models.KeyedVectors.load_word2vec_format(r"C:\Users\romaf\gensim-data\wiki-2017-gensim\model.bin", binary=True)

    def prep_papers(self,papers):
        self.papers_data = []
        self.papers_vectors = []
        for ind,row in papers.iterrows():
             self.papers_data.append((row['title'],row['keywords'],row['abstract']))
             self.papers_vectors.append(self.get_vec_rpr([row['title'],row['keywords'],row['abstract']])[2])


    def prep_persons(self,persons,norm_fact = 0):
        self.persons_data = []
        for person in persons:
            kw = person.calc_kw + person.given_kw
            vec_keys = self.get_vectors(kw)
            sum_vec_keys = self.get_weight_sum_vec(vec_keys,norm_fact)
            self.persons_data.append((person,sum_vec_keys))


    def find_matches_for_paper(self,paper,top_n = 4):
        if isinstance(paper,dict):
            paper_vec = self.get_vec_rpr([paper['title'],paper['keywords'],paper['abstract']])[2]
        else:
            paper_vec = self.get_vec_rpr([paper[0],paper[1],paper[2]])[2]
        res = []
        for person,vec in self.persons_data:
            res.append((person,cosine(paper_vec,vec)))
        res.sort(key=lambda x : x[1],reverse=True)
        return res[:top_n]


    def find_matches_for_person(self,person:PersonData,top_n = 4):
        kw = person.calc_kw + person.given_kw
        # print(kw)
        vec_keys = self.get_vectors(kw)
        # print(vec_keys)
        sum_vec_keys = self.get_sum_vec(vec_keys)
        # print(sum_vec_keys)
        print("Paper ================================")
        print(self.papers_vectors[0])
        res = []
        for ind,paper in enumerate(self.papers_data):
            res.append({"title":paper[0],"abstract":paper[2],"sim":cosine(sum_vec_keys,self.papers_vectors[ind])})

        df = pd.DataFrame.from_dict(res)
        df.sort_values(['Similarity'],inplace=True,ascending=False)
        return df.head(top_n)
        
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
