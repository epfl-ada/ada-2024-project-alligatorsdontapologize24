def movie_information(Moviedata, PlotData,ID):
    """
    print info on a movie
    """
    print("Movie\n") 
    display(MovieData.loc[ID])
    print("\nPlot")
    display(PlotData.loc[ID]["Plot"])
