import pandas as pd
from io import BytesIO
import psycopg2
import yake
from dataclasses import dataclass

@dataclass
class PersonData:

    name_surname:str
    orcid:str
    calc_kw = []
    given_kw = []
    affiliation: str

    def __init__(self,name = None,orcid = None ,given_kwords = None ,calc_kwords = None,aff = None) -> None:
        self.name_surname = name
        self.orcid = orcid
        self.given_kw = given_kwords
        self.calc_kw = calc_kwords
        self.affiliation = aff


            
        
class Modelprovider:

    def __init__(self) -> None:

        self.kw_extractor = yake.KeywordExtractor()


    def extract_kw(self,text):
        return self.kw_extractor.extract_keywords(text)

class DataHolder:

    def __init__(self) -> None:

        self.committee_df = None
        self.authors_df = None
        self.submissions_df = None
        
        # Connect to an existing database
        connection = psycopg2.connect(user="confeval",
                                    password="C0nfeval2022#",
                                    host="10.3.1.14",
                                    port="5432",
                                    database="orcid")

        # Create a cursor to perform database operations
        self.cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        self.cursor.execute("SELECT version();")
        # Fetch result
        record = self.cursor.fetchone()
        print("You are connected to - ", record, "\n")


    def load_committee(self,data):
        self.committee_df = pd.read_csv(BytesIO(data),index_col='#')

    def load_authors(self,data):
        self.authors_df = pd.read_csv(BytesIO(data))

    def load_submissions(self,data):
        self.submissions_df = pd.read_csv(BytesIO(data))

    def get_titles_by_person(self,person:PersonData):
        self.cursor.execute(f"select title from work w where w.orcid = '{person.orcid}'  order by date_created desc limit 10")
        return self.cursor.fetchall()

    def get_user_data_by_orcid(self,orcid_id:str):

        self.cursor.execute(f"SELECT source_name, keywords_name FROM profile_keyword where orcid = '{orcid_id}' LIMIT 1")
        name,given_kwords = self.cursor.fetchall()[0]

        self.cursor.execute(f"select title  from work w where w.orcid = '{orcid_id}'  order by date_created desc limit 5")
        titles = self.cursor.fetchall()

        self.cursor.execute(f"SELECT name from org where id in (SELECT org_id FROM org_affiliation_relation where orcid = '{orcid_id}' and org_affiliation_relation_role = 'employment' and end_year is null LIMIT 1) limit 1")
        aff = self.cursor.fetchall()[0][0]
        return PersonData(name,orcid_id,given_kwords.split(','),None,aff)

