import pandas as pd
from io import BytesIO
import psycopg2
from psycopg2 import Error





class DataHolder:

    def __init__(self) -> None:

        self.committee_df = None
        self.authors_df = None
        self.submissions_df = None



        try:
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

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def load_committee(self,data):
        self.committee_df = pd.read_csv(BytesIO(data),index_col='#')

    def load_authors(self,data):
        self.authors_df = pd.read_csv(BytesIO(data))

    def load_submissions(self,data):
        self.submissions_df = pd.read_csv(BytesIO(data))

    def get_data_by_orcid(self,orcid_id:str):
        self.cursor.execute(f"select title  from work w where w.orcid = '{orcid_id}'  order by date_created desc limit 10")
        return self.cursor.fetchall()