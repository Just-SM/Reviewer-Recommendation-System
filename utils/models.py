import yake


class Modelprovider:

    def __init__(self) -> None:

        self.kw_extractor = yake.KeywordExtractor()


    def extract_kw(self,text):
        return self.kw_extractor.extract_keywords(text)