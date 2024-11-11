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

    def clean_movie_data(self):
        
        MovieData = pd.read_csv(self.CLEAN_DATA_PATH+"/Movie_Data_clean.tsv",
                                sep='\t',
                               index_col=["Wikipedia movie ID"])
        
        return MovieData

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

    
    def load_all_data(self):
        return self.movie_data(),self.plot_data(),self.GVD_data(),self.Kaggle_data()
