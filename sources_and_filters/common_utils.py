import streamlit as st

import yake
import gensim.downloader
import gensim

import numpy as np
from numpy.linalg import norm

import pandas as pd 

from .person import PersonData

def cosine(a,b):
    d = np.dot(a,b)
    na = norm(a)
    nb = norm(b)
    nanb = na*nb
    return d / nanb
euclidian = lambda a,b : norm(a-b)

def move_next_page():
    st.session_state['work_flow_stage'] =  st.session_state['work_flow_stage'] + 1


class ModelProvider:

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