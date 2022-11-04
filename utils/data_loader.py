import pandas as pd
from io import BytesIO


class DataHolder:

    def __init__(self) -> None:

        self.committee_df = None
        self.authors_df = None
        self.submissions_df = None

    def load_committee(self,data):
        self.committee_df = pd.read_csv(BytesIO(data),index_col='#')

    def load_authors(self,data):
        self.authors_df = pd.read_csv(BytesIO(data))

    def load_submissions(self,data):
        self.submissions_df = pd.read_csv(BytesIO(data))

    def get_simlilar_names(self,person_data):

        pass