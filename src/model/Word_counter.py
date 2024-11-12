"""
Word counter script
--------------------------------------
This script implement a word counter. You choose the list and the model count for each plot the number of violent word and return a dataframe. 
List parameter :
"Physical_violence"
"Psychological_violence"
"All"
"""

import numpy as np
import pandas as pd


class WordCounter:
    def __init__(self,DataLoader,Dataframe):
        
        #initialise keywords
        self.keywords = ["Physical_violence","Psychological_violence"]
        self.data_loader = DataLoader
        self.dataframe = Dataframe

    def violent_word_count(self, keyword):
        #handle all keywords
        if keyword == "All" :
            dataframe = pd.DataFrame()
            for word_list in self.keywords :
                dataframe = pd.merge(dataframe, self.count_word(word_list), left_index=True, right_index=True, how='outer')
        elif keyword in self.keywords :
            dataframe = self.count_word(keyword)
        else :
            #handle case of a wrong call !
            raise Exception("Sorry, this keyword is not in the list. Reminder of the list : " + ' ,'.join(self.keywords))
        
        dataframe["total_count"] = self.dataframe["Plot"].str.split().str.len()

        return dataframe

    def count_word(self, keyword):
        dataframe = pd.DataFrame(index=self.dataframe.index)
        violent_list = self.data_loader.Violent_word_list(keyword)
        # Reshape the list
        pattern = r'\b(?:' + '|'.join(violent_list) + r')\b'
        # Calculate the appearances
        dataframe["word_count_"+keyword] = self.dataframe["Plot"].str.findall(pattern).str.len()
        return dataframe


