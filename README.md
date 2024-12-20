 # P3: AlligatorsDontApologize24 

 ## Project title: 
 ### The feedback loop of violence: How violent movies shape real-world violence

 ### Link to our data story: https://jadetherras.github.io/ADAlligators_website/ 
 ### Link to our dataset drive: https://epflch-my.sharepoint.com/:f:/r/personal/raphael_hellmann_epfl_ch/Documents/MA_3/ADA/PROJECT_DATA?csf=1&web=1&e=t72tTL
 

 ## Abstract:
 Cruel fist fights, brutal killings, rough sexual assaults - movies sometimes show more explicit violence than we would like. But do they lead to an increase in real-world violence? Or, on the contrary, do they serve as a release that reduces it? This study analyzes 17077 movies from the CMU Dataset [^1], enriched with data from the Kaggle Movies Dataset [^2]. Using this data in combination with the NIBRS dataset [^3], we examine the correlation between depicted violence in movies and real-world violence in the US. To purge the analysis from potential other factors that influence the real world violence, we use an auto-regressive distributed lag (ARDL) model with time-fixed effects. Moreover, we introduce different approaches of data normalisation before applying it on the model. The study shows that based on the data used, there is no significant correlation between the prevalence of violent movies and real-world violence.

## Main part
Even if very few would have believed it 20 years ago, wars and violent political conflicts are once again present. Moreover, everyday violence seems to be on the rise worldwide, as a study on the perception of violence in one's own neighborhood states [^4]. This underlines the importance of violence as the overall subject of this study. Within our analyses we aim to provide answers on the following research questions: 

* Is there a significant (positive or negative) correlation between the prevalence of violent movies and reported violent crimes in the US?
* Can we identify particularly violent time periods in the US? 
* Can we identify periods of abnormally many releases of violent movies? 
* Can we identify genres that are particularly violent?

The focus on the geographical area of the US is due to the fact that there is most data available, both for the movies and the real-world violence.

### Movie Datasets
The central dataset for our study is the CMU Dataset [^1]. Since time will play a crucial role in our study and precise release dates are often unavailable, we will fill in missing dates using The Movies Dataset from Kaggle [^2]. 
The first step is to clean and filter the movie data as explained in the "Datasets" section on our website.

### Movie Classification - 3 Classes

The next step is to identify the violent movies in the cleaned dataset. First, we want to distinguish between the following three classes: 

* Violent 
* Mild
* Peaceful

To achieve this, we implemented two different models:

* Model 1: Multiclass logistic regression model trained by us
* Model 2: Pre-trained LLM

#### Model 1:
Here, we first compute three different scores based on the plot summaries: 

* Physical violence score
* Psychological violence score
* Sentiment scores

For the physical and psychological violence score, we identified two separate lists of words that are unambigously connected to physical and psychological violence respectively. For potential further interest in the justification for those words, we created two .txt files in the data > CLEAN > violent_word_list folder.   
We parse through all plot summaries in the cleaned data and count how often those words appear. Since the length of the plot summaries varies significantly, we additionally compute the "density" of physical and psychological words by dividing the absolute counts by the number of words in the plot summary. 
For the sentiment scores, we apply the DistilBERT model trained for sentiment analysis [^5]. This model also parses through all plot summaries and computes scores for the following five sentiments: sadness, joy, love, anger, fear, surprise. The higher the score, the more prevalent is the sentiment. 
Those three scores are the features for the model. It is trained on a set of movies that we labelled by hand using the crowdsourcing approach, i.e. by activating our own social network. Model 1, however, showed unsatisfying results, since our features do not seem to sufficiently capture the complex notion of violence. 

#### Model 2: 
Here, we use a pre-trained LLM (GPT-4o mini from OpenIA [^6]) with custom prompts, our three different violence classes and a set of instructions. The assessment of the model performance is done on the same human-labelled movies as before. Due to the subjectivity of the human labelling process, model performance evaluation is not trivial. This is where the use of the Empath package comes in, as explained on the main page of our website. 
Generally, the performance of Model 2 is significantly better than Model 1. Thus, we chose Model 2 for the further analysis.

### Movie Classification - 2 Classes
By further studying the classification results of Model 2, we realized that the the middle class "Mild" was predicted very frequently and especially for all those cases that were slightly ambiguous between "Violent" and "Peaceful". As also stated on our website, the classification in those categories seems to be immensely subjective. Allowing for a "fallback" class in between "Violent" and "Peaceful" seems thus to unintentionally smooth out our classification results. Therefore, we decided to reduce the number of classes to 2: "Violent" and "Peaceful". 

This is also a more convenient classification for the subsequent usage in the ARDL model, as we will explain later.

### Violence Datasets

For real-world violence, we rely on the following dataset:

* NIBRS [^3]: Offers daily-level crime data for all states in the US.

The *offense_type_id* feature in NIBRS determines whether a crime qualifies as violent. With the exact date given for each recorded criminal offense, it provides the necessary time resolution for our ARDL model. 

### Correlation Analysis

A simple linear regression of violent movies on violent crimes would overlook confounding factors. To address this, we will implement an auto-regressive distributed lag (ARDL) model with time-fixed effects, offering the following advantages:

* Fine temporal resolution: Analyzing weekly data captures immediate effects of violent movie releases.
* Time-fixed effects: Absorbs macro-level influences like wars or riots.
* Auto-regressive lag: Accounts for the persistence of violence over time.
* Distributed lag: Accounts for the fact that the influence of movies on society is generally longer than one week.
  
This approach allows us to isolate the specific impact of violent movies on real-world criminal offenses.

We use the *select_order* function from the Statsmodels module to find the optimal lags for the auto-regressive and the distributed part to be included in the model. In the "Models & Methods" section on our website, we explain the model setup, the data normalisation approaches and the results in detail. 

### Conclusion
The central research question of this study was to find out if there is a correlation between the prevalence of violent movies on real-world violence. Using the ARDL model and the datasets described above, we could not find a statistically significant correlation between the two. Based on these findings, we assume that there is no correlation between violent movies and real-world violence. The exact results of the different ARDL models are provided in the "Models & Methods" section on our website. 

However, we must state that ARDL models are very demanding on the underlying data, i.e. they need a substantial amount of data to produce reliable results [^7]. With the limited amount of input data to our model, we must therefore be very cautious when interpreting the results. 

The plots on the main page of our website allow to clearly identify times of high and low violence levels as well as periods of high and low release numbers of violent movies.

Additionally, we could identify violent movie genres, like "Thriller", "Horror" and "Action" as opposed to more peaceful movie genres like "Comedy", "Romance" and "Family Film". This finding is naturally in line with our expectations and underlines the reliability of our classification mechanism. 

### Share of Work within the Team

The work of this project has been equally shared between the team members in the following way: 

* Jade: implementation of both classifier models (logistic regression and LLM), web design for website, writing the data story
* Emma: data exploration and cleaning for movie datasets, validation of LLM classification with Empath, computation of the psychological violence score for Model 1, writing the data story
* Jennifer: creating most of the graphs, violence score computation for ARDL model, identifying times of high and low violence levels and violent/peaceful genres
* Lucie: exploring, extracting and cleaning the real-world violence data, violence score computation for ARDL model, creating plots for real-world violence
* Raphael: setup, implementation and testing of the ARDL model, computation of the physical violence score for Model 1, writing the readme

[^1]: http://www.cs.cmu.edu/~ark/personas/
[^2]: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
[^3]: https://www.dolthub.com/repositories/Liquidata/fbi-nibrs/data/main
[^4]: Jackson, Chris. *Views on Crime and Law Enforcement Around the World*, Ipsos, 2023.
[^5]: https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion
[^6]: https://platform.openai.com/docs/models#gpt-4o-mini
[^7]: Ponziani, R. M. (2023). Inflation forecasting using autoregressive distributed lag (ARDL) models. Jurnal Ekonomi & Studi Pembangunan, 24(2), 316-330