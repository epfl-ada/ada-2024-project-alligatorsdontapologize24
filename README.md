 # P2: AlligatorsDontApologize24 

 ## Project title: 
 ### The Feedback Loop of Violence: How Real-Life Violence Shapes Movies and Movies Shape Society

 ## Abstract:
 Cruel fist fights, brutal killings, rough sexual assaults - movies sometimes show more explicit violence than we would like. But do they lead to an increase in real-world violence? Or, on the contrary, do they serve as a release that reduces it? Moreover, do violent historical events impact violence displayed in movies and more generally movie genres? This study analyzes 17077 movies from the CMU Dataset (LINK HERE), enriched with data from the Kaggle Movies Dataset (LINK HERE). Using this data in combination with the GVD Dataset (LINK HERE), we examine the correlation between depicted violence in movies and real-world violence in the US. To purge the analysis from potential other factors that influence the real world violence, we use the Instrumental Variable Method. Moreover, the (WHICH DATASET?) dataset is used to evaluate the potential impact of historical events on the violent content depicted in movies.

Even if very few would have believed it 20 years ago, wars and violent political conflicts are once again present. Moreover, everyday violence seems to be on the rise worldwide, as a study on the perception of violence in one's own neighborhood states [^1]. This underlines the importance of violence as the overall subject of this study. Within our analyses we aim to provide answers on the following research questions: 

* Is there a significant (positive or negative) correlation between the prevalence of violent movies and reported violent deaths in the US?
* Can we identify an impact of violent historical events (wars, violent riots, etc.) on the prevalence of violent movies in the US?
* ...

The focus on the geographical area of the US is due to the fact that there is most data available, both for the movies and the real-world violence.
The central dataset for our study is the CMU Dataset (LINK HERE). To enrich this dataset with missing dates and the audience's perception of the movies (rankings), we use The Movies Dataset from Kaggle (LINK HERE). The GVD dataset (LINK HERE) is used as the source for real-world lethal violence in the US. This dataset integrates indicators on the major causes of lethal interpersonal and communal violence — intentional and unintentional homicides, killings in legal interventions, and direct conflict deaths — and combines them in a single violent deaths indicator [^2]. Moreover, the (WHICH DATASET) (LINK HERE) serves as a resource for violent historical events. This dataset is mainly used to identify the exact temporal span of those events in order to analyze the prevalence of violent movie content in those times.  
The first step in this analysis is to clean and filter the movie data in the CMU dataset. For this, we perform the following processing steps:
* Removing unnecessary columns and NaN entries
* Keep only the entries for which we have both metadata and a plot summary
* Lowercase all plot summaries
* Convert all entries in easily readable format (e.g. convert {"/m/09c7w0": "United States of America"} to "United States of America")
* Filter only for US movies

Moreover, we treat the Kaggle dataset in the same way. This allows us to replace incomplete or missing dates for movies in the CMU dataset with the corresponding data from the Kaggle dataset (matched by the movie title). If neither the CMU nor the Kaggle dataset provide valid information on the movie date, we drop the corresponding entry. Checking for outliers, i.e. incorrect dates, revealed no hits. The cleaned dataset is exported and saved in .tsv format.

The next step is to identify the violent movies in the cleaned dataset. For this, we defined three scores: 
* Physical violence score
* Psychological violence score
* Sentiment scores

In all three cases, the data source is the plot summary. For the physical and psychological violence score, we identified two separate lists of words that are unambigously connected to physical and psychological violence respectively. For potential further interest in the justification for each word in those lists, we created two .txt files in the data > CLEAN > violent_word_list folder. The reason why the list of psychologically violent words is by far greater than the one for physical violence is the following: While physically violent words can often be unambigously described by nouns (e.g. "murder"), psychological violence is often referred to by verbs. Thus, we had to include various different conjugations of each verb.  
We then parse through all plot summaries in the cleaned data and count how often those words appear. This leads to the absolute counts of physical and psychological words in the plot summaries. Since the length of the plot summaries varies significantly, we additionally compute the "density" of physical and psychological words by dividing the absolute counts by the number of words in the plot summary. 
For the sentiment scores, we apply the DistilBERT model trained for sentiment analysis [^3]. This model also parses through all plot summaries and computes scores for the following five sentiments: sadness, joy, love, anger, fear, surprise. The higher the score, the more prevalent is the sentiment.



[^1]: Jackson, Chris. *Views on Crime and Law Enforcement
Around the World*, Ipsos, 2023.
[^2]: Zenodo, *Global Violent Deaths (GVD) database 2004-2021, 2023 update, version 1.0*, DOI: 10.5281/zenodo.8215006, 2023
[^3]: https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion