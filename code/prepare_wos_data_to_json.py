import pandas as pd
import jsonlines
import json
import doi as doiLib



class Prepare:
    def __init__(self,source_file,output_dir):
        self.dataDict = {"WOSUID":[],
            "pubTitle":[],
            "pubYear":[],
            "pubType":[],
            "journalTitle":[],
            "publisher":[],
            "area":[],
            "areaCount":[],
            "identifier":[],
            "keywords":[],
            "abstract":[],
            "doi":[],
            "validDoi":[],
            "url":[],
            #"OA":[],
            #"OA-pdf_url":[],
            #"issn":[],
                   }
        self.source_file=source_file
        self.output_dir=output_dir
    
    def run(self):
        """
        this function opens the jsonlines file with raw data from web of science, 
        digs for the variables wanted, and stores them in a dictionary. The function "save"
        saves the dictionary in a JSON file
        """
        
        with jsonlines.open(self.source_file) as reader:   
            for obj in reader:
                
                try:
                    wosID = obj["record"]["UID"][4:]
                except KeyError:
                    wosID = None
                
                self.dataDict["WOSUID"].append(wosID)
                self.dataDict["pubTitle"].append(obj["record"]["static_data"]["summary"]["titles"]["title"][-1]["content"])
                self.dataDict["pubYear"].append(obj["record"]["static_data"]["summary"]["pub_info"]["pubyear"])
                self.dataDict["pubType"].append(obj["record"]["static_data"]["summary"]["doctypes"]["doctype"])
                self.dataDict["journalTitle"].append(obj["record"]["static_data"]["summary"]["titles"]["title"][0]["content"])
               
                try:
                    publisher = obj["record"]["static_data"]["summary"]["publishers"]["publisher"]["names"]["name"]["unified_name"]
                except KeyError:
                    publisher = None
                
                self.dataDict["publisher"].append(publisher)
                
                try:
                    areaCount = obj["record"]["static_data"]["fullrecord_metadata"]["category_info"]["subheadings"]["count"]
                except KeyError:
                    areaCount = None
                
                self.dataDict["areaCount"].append(areaCount)
            
                try:
                    area = obj["record"]["static_data"]["fullrecord_metadata"]["category_info"]["subheadings"]["subheading"]
                except KeyError:
                    area = None
                
                self.dataDict["area"].append(area)
                self.dataDict["identifier"].append(obj["record"]["dynamic_data"]["cluster_related"]["identifiers"]["identifier"])
            
                try:
                    keyword = obj["record"]["static_data"]["fullrecord_metadata"]["keywords"]["keyword"]
                except KeyError:
                    keyword = None
                
                self.dataDict["keywords"].append(keyword)

                try:
                    abstract = obj["record"]["static_data"]["fullrecord_metadata"]["abstracts"]["abstract"]["abstract_text"]["p"]
                except KeyError:
                    abstract = None
            
                self.dataDict["abstract"].append(abstract)
            

                doi = None
                url = None
                #print(index)
                for item in obj["record"]["dynamic_data"]["cluster_related"]["identifiers"]["identifier"]:
                    try:
                        if item["type"]=="doi" or item["type"]=="xref_doi":    
                            doi = item["value"]
                    except TypeError:
                        doi=None
                
                    try:
                        validDoi = doiLib.validate_doi(doi)
                    except ValueError:
                        validDoi = None
                
                self.dataDict["doi"].append(doi)
                self.dataDict["validDoi"].append(validDoi)
            
                if validDoi !=None:
                    pass
                else:
                    pass    
                
                try:
                    url = doiLib.get_real_url_from_doi(doi)
                except ValueError:
                    url=None
            
                self.dataDict["url"].append(url)      
            #index=index+1
        
        return self.dataDict
    
    def save(self,file_name):    
        with open(self.output_dir+file_name, 'w') as fp:
            json.dump(dataDict, fp)
    