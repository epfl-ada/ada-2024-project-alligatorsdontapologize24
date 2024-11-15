def movie_information(Moviedata, PlotData,ID):
    """
    print info on a movie
    """
    print("Movie\n") 
    display(MovieData.loc[ID])
    print("\nPlot")
    display(PlotData.loc[ID]["Plot"])


def categorize_value(x):
    if x < -1/3:
        return -1
    elif -1/3 <= x <= 1/3:
        return 0
    else:
        return 1

choices = [-1.0, 0.0, 1.0]