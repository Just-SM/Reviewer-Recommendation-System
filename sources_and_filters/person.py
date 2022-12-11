from dataclasses import dataclass


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
 