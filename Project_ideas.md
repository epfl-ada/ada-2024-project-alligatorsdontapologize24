## Raphael

Ideas:

1) Influence of U.S. Political Activism on Diversity in Movie Characters

How did U.S. political movements advocating for equality, such as the Civil Rights, Women’s Rights, and LGBTQ+ movements, influence diversity in global cinema? We hypothesize that the prominence of these movements shaped the representation of diverse characters, especially in terms of race and gender, in films worldwide.
We will analyze how the gross revenue of movies with diverse casts evolved over time in relation to these movements, with a focus on the depiction of women. To achieve this, we will use a combination of datasets: the character metadata (character.metadata.tsv), including information on ethnicity and gender, and movie metadata (movie.metadata.tsv), containing the box office revenues. Additionally, we will utilize freely available data on the timeline of these movements, such as information on the Civil Rights Movement from Statista.com.
By parsing plot summaries (plot_summaries.txt), we will also examine how often films address political issues like segregation, racism, or voting rights. Thus, this study analyses how U.S. political advocacy has influenced global film diversity and shaped the financial success of movies featuring diverse characters.

2) Influence of Economic Uncertainty on Movie Genres

How did periods of economic uncertainty, such as the Great Depression, the 1973 Oil Crisis, the 2008 Global Financial Crisis, and the COVID-19 Economic Crisis, influence the prevalence of specific movie genres and the length of films in different regions?
We hypothesize that during financial hardship, people turn to escapist genres like fantasy or science fiction to disconnect from reality. We will examine whether the production of such genres increases during crises and if longer, more immersive films become more popular. Another aspect of this study is to investigate whether audience spending on these genres rises during times of economic distress.
Using movie metadata (movie.metadata.tsv), which includes data on genres, box office revenues, and runtimes, along with publicly available economic data, we aim to explore whether there are regional differences in these trends. By this, we will try to understand if escapist films provide a collective form of relief during economic downturns.

3) Patriotism in Film: Impact of Donald Trump's Election on Box Office Trends

How did Donald Trump's election and patriotic rhetoric influence the U.S. film industry? We will analyse whether Trump's emphasis on "American values" and patriotism has led to an increase in the production of patriotic-themed films, biographical films about American heroes, and war narratives, and whether these themes have contributed to higher box office revenues.
For this, we will utilise publicly available data on Trump's political discourse, such as Twitter posts and surveys, to detect a growing focus on patriotism during Trump's presidency campaign. Moreover, by utilising the movie metadata (movie.metadata.tsv) on genres and earnings, as well as parsing plot summaries (plot_summaries.txt) for keywords like "patriotism," "America," and "hero," we examine the influence of such a focus shift on film content. With this we aim to find out if Trump’s presidency campaign and his political rhetoric has shaped the cultural output of the American film industry.

Answer from TA: --> Grade: Great

Overall, the proposal demonstrates strong potential for insightful analysis of historical and political influences on cinema.\\\\Idea 1: Influence of U.S. Political Activism on Diversity in Movie Characters\\\\Strong but needs more focus. The analysis of how political movements influenced diversity in global cinema is highly relevant, and the focus on specific movements adds depth. The methodology is solid, but the global aspect of the analysis could be challenging. More clarity on how global vs. U.S. film industries will be compared, and how diverse casts will be defined and measured, would strengthen the proposal. The use of plot summaries to identify political issues is a great addition, but the process for parsing and analyzing these summaries could be more detailed.\\Idea 2: Influence of Economic Uncertainty on Movie Genres\\\\Interesting and timely. Analyzing how economic crises influence movie genres is a compelling idea. The hypothesis that people turn to escapist genres during tough times is strong, but more detail is needed on how "escapist" genres will be defined and measured. The analysis of regional differences in response to economic uncertainty is a good addition, but how these differences will be identified and compared should be clarified. Additionally, the method for linking economic data with film data could be elaborated further.\\Idea 3: Patriotism in Film: Impact of Donald Trump's Election on Box Office Trends\\\\Unique but needs refinement. The idea of analyzing how Trump's election and patriotic rhetoric influenced film production and box office trends is intriguing. The methodology of using Trump's public discourse (e.g., Twitter posts) to detect a shift in patriotic themes is creative, but more details on how this data will be connected to film content and box office performance would strengthen the proposal. Additionally, the process of keyword analysis in plot summaries could be expanded to ensure a robust analysis of how patriotism is portrayed in films.

## Emma

First idea: do violent movies increase real-world violence, or do they serve as a release that reduces it?

How does the impact of violent movies differ across age groups and genders? Do different types of violent content (e.g., realistic vs. fantastical) affect behaviour differently? Is there a difference between physical versus psychological violence? Do some movie genres have a greater effect in the phenomenon? Does the language in movies change during violent epochs (e.g. World War 2)? Does watching violent movies substitute for other potentially more harmful activities?  
The objective of this investigation is to explore the correlation between crime rates and the release of violent movies, to find answers to the above interrogations.  
To achieve this, movie genres (from the CMU dataset) will be classified as violent (e.g., Crime/Psychological Thriller) or non-violent (e.g., Family Film, Romantic Comedy). To improve the robustness, keywords related to violence (such as "murder," "blood," "kill") will be extracted from movie summaries and subtitles (which can be obtained from the Linguistic Data of 32k Film Subtitles dataset). Ideally, other datasets, such as Movie Body Counts, would also be included to measure violence by the number of deaths in a film.
  
Finally, this analysis will be combined with crime statistics from the United Nations Office on Drugs and Crime or the Small Arms Survey's Global Violent Deaths (GVD) database. The correlation between movie releases and crime rates in a given year can then be quantified using statistical tests (e.g., Pearson). Due to the complexity of violent phenomena it might be that some false correlation appear due to external factors (e.g. socioeconomic conditions). DAGs can help determine if prior conditioning is needed to account for such factors.

Second idea: actors and characters, how much do they blend?

How much does an actor's first role influence the rest of their career? Is there a notable difference between contemporary actors and older celebrities? Are actors tailored for specific types of characters, meaning: when blockbusters feature the same actor, do they tend to play similar roles (villain, hero, etc.)? Can actors influence the genres of blockbusters? Specifically, can an actor drive the box office success of movies, leading to the emergence of new trends around specific genres?  
In order to answer these questions, box office data alongside actor filmographies would be used to reveal patterns in genre evolution over time. Studies of actors' career paths and roles they've taken throughout their careers can shed light on how specific actors contribute to the changing landscape of cinema.

Third idea: are we really more attracted to low-complexity movies?

To answer this, summaries and subtitles will be used to assess movies' complexity (using the datasets listed in idea 1). A list of keywords can help to determine whether a plot is rich or linear, recurrent or original, etc. From the subtitles, information on the richness of language can be extracted. By doing this over various decades, the aim is to identify if a (decreasing) trend in complexity exists. Additional factors can strengthen the classification: movie duration, genres, music, etc.  
Finally, the plot could be enriched with a tag analysis, using movie tags (from the MovieLens dataset) such as "thought-provoking" or "complex plot" to assess movies complexity. Or even with a review on sentiment analysis, using IMDB reviews to determine the audience's perception of complexity.

Answer from TA: --> Grade: Great

Overall, your proposal raises several interesting and important questions, especially in terms of the social impact of violent movies and the impact of actors on the genre. I prefer your first idea to the second and third. In comparison, both idea2 and idea3 lack sufficient execution details, especially on how to translate complex theories into actionable data analysis.\\\\Idea 1: Do violent movies increase violence in the real world?\\The idea is very socially relevant and the topic is innovative and relevant. However, how are you going to clarify the connection between violent movies and real violence. It is suggested that further detail be provided on how the correlation can be analyzed through the classification of film genres and crime statistics.\\\\Idea 2: Integration between actors and characters\\The idea is very innovative and proposes a long-term study on actors and role types. However, the proposal lacks clear implementation steps and it is suggested that more detail be provided on how data analysis can be used to draw conclusions about the evolution of actors and roles.\\\\Idea 3: Do we really prefer movies with simple plots?\\Interesting idea, but the definition of plot complexity and the methodology for analyzing it need to be further clarified. It is suggested to add a step to analyze the relationship between plot complexity and movie popularity.\\\\Translated with DeepL.com (free version)

## Jade

1] Actors vs. Characters: How far are they?

Without actors, characters wouldn’t come alive. But how similar are actors to the characters they play? Movies often serve as a window into the world, and we frequently compare ourselves to on-screen characters. This raises several perspectives.
Is there a significant gap between the ages of characters and their actors? Does this differ by period or gender? What about ethnic representation?\\
Do specific actors tend to get "typecast" or play roles similar to their first successful character? Can we find correlations between actors' real-life traits and the roles they are assigned?
To explore these questions, we will analyze the dataset on both characters and actors and incorporate movie dialogue from the Cornell Movie-Dialogs Corpus. External databases can give more information about actors, like the UCI movie dataset, which includes actor roles and movie citations, and the Wikiperson dataset, which provides detailed information about actors. Similarly to how the paper identified character types, we could extract actor archetypes to match actor and character types.

2] Can movies rhyme with eco-friendly?

The voice of ecology has gained strength over the past century, but is this reflected in the film industry? This question can be viewed from two main perspectives.
First, how is the theme of ecology treated in movies? This section will examine documentaries, fiction, and films that address ecological issues. We will analyze movie themes and dialogue, investigating if eco-anxiety and ecological catastrophe have become more prevalent recently. Does this representation change with social and political contexts or major environmental events? We could use the SPEED database for historical events and the International Disaster Database for environmental events.
Secondly, creating a movie has a significant ecological impact. Is there a trend toward a more sustainable film industry? This question is more challenging to address due to the lack of extensive databases on the impact of individual films. However, we can explore environmental certifications for films, such as those found in the Green Film Database, and extract selected films and their features.

3] Flying cars? Martian attack? Ecological tragedy? A story about how we envision the future.

Humans have always imagined what the future might look like, speculating about future technologies, societal changes, environmental issues... The CMU dataset spans movies from 1888 to 2018, offering a unique opportunity to explore how visions of the future have evolved.
How do we imagine the future depending on the period, country, or economic and political events? Can we compare past visions with today's reality?
To answer these questions, we'll first extract movies that envision the future and analyze their genres, plot summaries, and geographical origin. Then, by aligning political and historical events with the cinematographic timeline, we can investigate how filmmakers envision the future correlates with real-world events. For example, we could use external historical and political event databases such as SPEED, to identify key global events and assess their influence on these evolving visions of the future.

Answer from TA: --> Grade: Great

This proposal includes interesting and creative ideas, especially the first two. The third idea is also strong but may require more data refinement. Overall, clear direction but could benefit from more execution details.

Idea 1: Actors vs. Characters
Great idea! The comparison between actors' real-life traits and their characters is compelling. Be cautious about data availability for correlating personal traits with character roles.

Idea 2: Can movies rhyme with eco-friendly?
Super relevant and creative! Exploring the ecological impact of filmmaking is unique. However, addressing the lack of comprehensive data on sustainability in film may be challenging.

Idea 3: How we envision the future
Good concept, but could use more clarity on how past visions of the future will be systematically compared with real-world events. Ensure there's enough data to make meaningful correlations.

## Lulu

### Ideas

1) **Star Power Unveiled - What Makes the Greatest Cast?**
What makes a cast appeal to both audiences and critics? Beyond box office numbers, this project explores the hidden factors that determine whether a cast becomes legendary or forgettable. We will use metadata from the CMU Movie Summary Corpus to investigate the casting process. How a mix of established stars, young talent, and diversity in gender, ethnicity, and genre experience contributes to a movie’s success.
By combining film reviews (IMDb, Rotten Tomatoes) with box office performance, we will uncover patterns behind casting decisions. Do experienced actors outperform newcomers, or does chemistry and diversity within the cast capture audiences? Can we predict which combinations of actors and genres produce hits and critical acclaim?
We will also explore how actors excel in different roles: do comedic actors thrive in dramas? Does casting diversity across genres increase the likelihood of success? This analysis will reveal casting strategies that elevate a film from average to iconic.
This project will provide insights into how casting directors can assemble the most attractive cast for success, looking beyond typical selections to identify the hidden patterns that make star power shine.
2) **The Final Cut - How Movie Endings Shape Success**
This project explores how the tone of a film's ending (positive, negative, or ambiguous) affects its box office performance and critical reception. Using the CMU Movie Summary Corpus, we will categorize endings through sentiment analysis of plot summaries (e.g., tragic, open-ended). We will then analyze correlations between different ending types and audience satisfaction, critical reviews, and box office success.
To enhance the analysis, we may include data from IMDb or social media to see real-time audience reactions. Do happy endings outperform darker conclusions? Is there a link between genre and preferred ending types? Do films with ambiguous endings struggle initially but develop adoration followings over time?
This project will provide insights into how a film's conclusion affects its legacy, allowing directors to make informed narrative decisions to boost audience engagement and box office performance.
3) **Cinema as Catalyst - How Films Influence Societal Change**
This project will explore how films that tackle themes of dictatorship, democracy, or social injustice influence societal debate and potentially drive change. Using the CMU Movie Summary Corpus, we will identify movies with political or justice-related plots. By integrating datasets of significant political events (e.g., democratic movements, revolutions, or major protests) from the Global Database of Events, Language, and Tone (GDELT), which covers the period from 1979 to 2014, we will analyze correlations between the release of such films and shifts in public activism.
We will also examine Google search trends to measure the impact of these films on public interest. For example, if a movie focuses on feminism does it cause a spike in searches? Do politically charged films raise awareness and encourage internet engagement? Through both public interest and historical events, this analysis will uncover the influence of cinema on societal values, political engagement, and long-term political outcomes.

Answer from TA: --> Grade: Excellent

This proposal presents three excellent and creative ideas with clear paths for execution. Each idea is well-structured, innovative, and makes great use of available data. The balance between creativity and analytical rigor is strong, making this proposal stand out.

**Idea 1:** Star Power Unveiled
Excellent! This concept is both insightful and practical. Analyzing cast dynamics and their impact on a film’s success provides a fresh angle. The use of both critical reviews and box office data is a strong approach, and exploring diversity and genre versatility adds depth.

**Idea 2:** The Final Cut
Great idea! The relationship between movie endings and their success is an underexplored area. Sentiment analysis of plot summaries is a smart method. Be mindful of how different genres may skew audience expectations of endings.

**Idea 3:** Cinema as Catalyst
Super insightful! This idea effectively connects cinema with societal change, providing a timely analysis. Using datasets like GDELT to track the societal impact of political films is a great approach. This project has strong potential to uncover meaningful correlations between film and public activism.


## Jen 

1) **Does watching movies make you happy?**
Philosophy and psychology may have something to say about this, but what can data analysis reveal? Can computed data analysis become a third lens in understanding this relationship? To investigate, common movies between the CMU and IMDb datasets will be analyzed. Sentiment analysis of IMDb reviews will be conducted and compared with the year-specific World Happiness Report. A movie's reception will serve as a basis for examining its potential impact on global happiness. If a movie is well received, regardless of its topic, does it influence the mood of audiences worldwide? Has society become dependent on its entertainment industry, or is it the other way around—does people's happiness affect how they perceive a film? This question may be as elusive as “Which came first: the chicken or the egg?” First, is the impact of movies on happiness real, or just speculative? Statistical relevance will be tested. Can we find a correlation, and if so, how strong is it? Finally, patterns will be explored, such as whether a rise in movie viewership corresponds to increased happiness. Ultimately, we may get closer to solving the "egg problem."

2) **The Role of Politics in Cinematography**
Politics influence our lives in many ways. Our nationality can affect our rights and shape our beliefs. Can we see these roles reflected in cinematography? All levels will be considered—from the location of the movie set to the nationality of the producer and actors. But the investigation won't stop there. Metrics like literacy and wealth (e.g., GDP) of the country where the movie is released will also be taken into account. What if we go further and examine the main action setting? Does fantasy mimic reality, or does it oppose it? Are rebellions more prominent in democratic countries, for instance? A map will be created based on these findings. Time and socio-economic context will also be factored in. All data will be analyzed by decade to enable meaningful comparisons.

3) **Identity Card of the Hero and the Villain Biases are present in cinematography.**

Everyone has in mind the voluptuous woman in distress and her savior—an athletic, good-looking man. But what is the depth of these prejudices? Is it possible to identify the hero's characteristics and those of his antagonist? Are nationality, age, and gender part of these traits? What are the other hidden traits of these protagonists? By leveraging the work of Bamman et al. on persona, protagonists will be filtered. Can key features be identified? Can we observe the well-known stereotypes? Perhaps there isn't a global definition of our hero and villain. It might be country- or time-dependent. If so, maps or timelines will be created to reflect these changes and enable comparisons with social movements such as the rise of feminism or nationalism.

**General comment**
This proposal presents creative ideas with clear potential. Ideas 1 and 2 are particularly strong, while Idea 3 may need refinement in data analysis. Overall, well thought out but with minor challenges in execution.

**Idea 1: Does watching movies make you happy?**
Great idea! Sentiment analysis and happiness correlation are interesting. Be cautious about isolating movie effects from other societal influences.

**Idea 2: The Role of Politics in Cinematography**
Super creative! Mapping political influences is compelling. Simplify variables to avoid overcomplication.

**Idea 3: Identity Card of the Hero and the Villain**
Interesting but data extraction may be complex. Refine how to handle character traits across periods and regions.