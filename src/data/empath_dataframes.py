import pandas as pd
import spacy
from empath import Empath

def analyze_empath_features(movie_data, plot_column, id_column, title_column, output_dir):
    """
    Analyzes Empath features from movie plot summaries and saves results to a TSV file.

    Parameters:
        movie_data (pd.DataFrame): Our pandas DataFrame containing movie data.
        plot_column (str): The name of the column containing plot summaries.
        id_column (str): The name of the column to use as the index.
        output_file (str): Path to save the output TSV file.

    Returns:
        pd.DataFrame: A DataFrame containing Empath features for each movie.
    """
    # Initialize NLP model and Empath lexicon
    nlp = spacy.load("en_core_web_sm")
    lexicon = Empath()
    
    # Results containers
    normalized_results = []
    non_normalized_results = []

    # Loop through the plot summaries
    for idx, summary in enumerate(movie_data[plot_column]):
        # Preprocessing: Lemmatize and remove stop words/punctuation
        doc = nlp(summary)
        lemmatized_text = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
        
        # Empath Analysis (normalized and not)
        normalized_features = lexicon.analyze(lemmatized_text, normalize=True)
        non_normalized_features = lexicon.analyze(lemmatized_text, normalize=False)
        
        # Append results to the matrix as a row
        normalized_results.append(normalized_features)
        non_normalized_results.append(non_normalized_features)


    # Create DataFrames from the results matrices
    normalized_df = pd.DataFrame(normalized_results, index=[f"Movie {i+1}" for i in range(len(movie_data[plot_column]))])
    non_normalized_df = pd.DataFrame(non_normalized_results, index=[f"Movie {i+1}" for i in range(len(movie_data[plot_column]))])

    # Set the desired column as the index
    normalized_df.index = movie_data[id_column]
    non_normalized_df.index = movie_data[id_column]

    # Add the "Movie name" column to both DataFrames
    normalized_df["Movie name"] = movie_data[title_column].values
    non_normalized_df["Movie name"] = movie_data[title_column].values

    # Save the DataFrames to TSV files
    normalized_file = f"{output_dir}/empath_features_normalized.tsv"
    non_normalized_file = f"{output_dir}/empath_features_non_normalized.tsv"
    normalized_df.to_csv(normalized_file, sep="\t")
    non_normalized_df.to_csv(non_normalized_file, sep="\t")
    
    return normalized_df, non_normalized_df
