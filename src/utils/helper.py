import ast
import re
from collections import Counter
import spacy



def longest_consecutive_sequence(sorted_years):
    """
    Finds the longest consecutive sequence of years in a sorted list of integers.

    Args:
        sorted_years (list[int]): A list of integers representing years, sorted in ascending order.

    Returns:
        list[int]: A list containing the longest consecutive sequence of years.
                   If there are multiple sequences of the same maximum length, the first one encountered is returned.

    Example:
        >>> longest_consecutive_sequence([2000, 2001, 2002, 2004, 2005, 2006, 2007])
        [2004, 2005, 2006, 2007]
    """
    # Initialize variables to track the longest sequence
    max_length = 1
    current_length = 1
    start_year = sorted_years[0]
    best_start = start_year

    # Iterate through the sorted list and find the longest consecutive sequence
    for i in range(1, len(sorted_years)):
        if sorted_years[i] == sorted_years[i - 1] + 1:
            current_length += 1
        else:
            if current_length > max_length:
                max_length = current_length
                best_start = start_year
            # Reset for the next sequence
            start_year = sorted_years[i]
            current_length = 1

    # Check the last sequence
    if current_length > max_length:
        best_start = start_year
        max_length = current_length

    # Create the list of the longest consecutive sequence
    longest_sequence = list(range(best_start, best_start + max_length))
    return longest_sequence


# Convert genres, countries and languages in an understandable format
def extract_data(text):
    # Look for all names using a regex pattern: it matches quoted text appearing after colon
    return ", ".join(re.findall(r'": "([^"]+)"', text))

# Create a function to generate a bag-of-words DataFrame
def generate_bow(data, condition, plot_title, output_file):
    # Filter data based on the condition (violent or non-violent)
    filtered_data = data[data['Prediction'] == condition]
    
    # Perform the bag-of-words operation
    word_counter = Counter()
    for summary in filtered_data["Plot"]:
        doc = nlp(summary)
        lemmatized_words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        word_counter.update(lemmatized_words)

    # Convert to DataFrame
    bow_df = pd.DataFrame(word_counter.items(), columns=["Word", "Frequency"]).sort_values(by="Frequency", ascending=False)

    # Save to CSV
    bow_df.to_csv(output_file, index=False)

    return bow_df