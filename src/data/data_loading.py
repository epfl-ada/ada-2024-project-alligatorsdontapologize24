"""
Data loading script
--------------------------------------
This script handle all data loading steps. 
CLEAN and RAW data.
"""
from os import listdir
import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self,raw,clean):
        self.RAW_DATA_PATH = raw
        self.CLEAN_DATA_PATH = clean

    def show_data_folder(self):
        print("raw data \n")
        L = listdir(self.RAW_DATA_PATH)
        for file in L:
            if file not in (".DS_Store", ".ipynb_checkpoints"):
                print(file)
        L = listdir(self.CLEAN_DATA_PATH)
        print("\nclean data \n")
        for file in L:
            if file not in (".DS_Store", ".ipynb_checkpoints"):
                print(file)

    def movie_data(self):
        print("\nload CMU movie metadata\n")
        # load movies data
        name = ["Wikipedia movie ID",
                "Freebase movie ID",
                "Movie name",
                "Release date",
                "Box office revenue", 
                "Runtime", #minutes
                "Languages",
                "Countries",
                "Genres"]

        MovieData = pd.read_csv(self.RAW_DATA_PATH+"/CMU_Movies_Dataset/movie.metadata.tsv",
                                sep='\t',
                                header=None,
                               names = name,
                               index_col=["Wikipedia movie ID"])

        return MovieData

    def plot_data(self):
        print("\nload plot data\n")
        # load plots
        name = ["Wikipedia movie ID",
        "Plot"]

        PlotData = pd.read_csv(self.RAW_DATA_PATH+"/CMU_Movies_Dataset/plot_summaries.txt",
                   delimiter='\t',
                   header=None,
                   names = name,
                   index_col=["Wikipedia movie ID"])

        return PlotData

    def GVD_data(self):
        print("\nload GVD data\n")
        GVDData = pd.read_csv(self.RAW_DATA_PATH+"/GVD_Dataset/2023_gvdDatabase_1_0_country.csv")

        return GVDData

    def Kaggle_data(self):
        print("\nload kaggle movie data\n")
        KaggleData = pd.read_csv(self.RAW_DATA_PATH+"Kaggle_Movies_Dataset/movies_metadata.csv",
                                dtype={ 'popularity': str })

        return KaggleData

    #load all raw data
    def load_all_data(self):
        
        return self.movie_data(),self.plot_data(),self.GVD_data(),self.Kaggle_data()

    def clean_movie_data(self):
        
        MovieData = pd.read_csv(self.CLEAN_DATA_PATH+"/Movie_Data_clean.tsv",
                                sep='\t',
                               index_col=["Wikipedia movie ID"])
        return MovieData

    def data_for_violent_model(self):
        
        SentimentData = pd.read_csv(self.CLEAN_DATA_PATH+"/sentiment.csv")
        
        WordCountData = pd.read_csv(self.CLEAN_DATA_PATH+"/word_count.csv")
        Data = pd.merge(SentimentData,WordCountData, on="Wikipedia movie ID", how='outer')
        Data = Data.set_index("Wikipedia movie ID")
        return Data

    def human_labelled_data(self):
        
        ViolentData = pd.read_excel(self.RAW_DATA_PATH+"/Human_labelling_violentMovie.xlsx",sheet_name='data')
        ViolentData = ViolentData.set_index("Wikipedia ID")
        ViolentLabel = pd.read_excel(self.RAW_DATA_PATH+"/Human_labelling_violentMovie.xlsx",sheet_name='label')
        return ViolentLabel,ViolentData

    def Violent_word_list(self,keyword):
        match keyword:
            case "Physical_violence" :
                WordList = pd.read_excel(self.CLEAN_DATA_PATH+"/violent_word_list/Physical_violence.xlsx")
            case "Psychological_violence" :
                WordList = pd.read_excel(self.CLEAN_DATA_PATH+"/violent_word_list/Psychological_violence.xlsx")
            case _:
                raise TypeError("This keyword is not associated with any specific word list.")
                WordList = pd.DataFrame()
        
        return WordList.transpose().values.tolist()[0]
