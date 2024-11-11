"""
Twitter Sentiment analysis script
--------------------------------------
This script implement the sentiment analysis model of twitter.
Given a text, the model return a sentiment analysis that sum to 1.
Score is a array :
"joy": Score[0],
"optimism": Score[1],
"anger": Score[3],
"sadness": Score[4]
source : https://huggingface.co/cardiffnlp/twitter-roberta-base-emotion
"""


from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
import torch

# Tasks:
# emoji, emotion, hate, irony, offensive, sentiment
# stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary

task='emotion'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

# download label mapping
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def extract_emotion(plot,printting = False) :

    encoded_input = tokenizer(plot, return_tensors='pt', truncation=False)
    
    # Max tokens per chunk
    max_length = 514
    total_length = encoded_input['input_ids'].size(1)
    
    # Split the input into chunks of max_length tokens
    input_ids = encoded_input['input_ids'][0] 
    attention_mask = encoded_input['attention_mask'][0]
    
    
    # Create chunks
    input_id_chunks = [input_ids[i:i + max_length] for i in range(0, len(input_ids), max_length)]
    attention_mask_chunks = [attention_mask[i:i + max_length] for i in range(0, len(attention_mask), max_length)]
    
    
    # Convert chunks back to tensors with correct batch dimension
    chunked_inputs = [{'input_ids': ids.unsqueeze(0), 'attention_mask': mask.unsqueeze(0)} 
                      for ids, mask in zip(input_id_chunks, attention_mask_chunks)]

    Scores = np.zeros(4)
    
    for chunk in chunked_inputs:
    
        position_ids = torch.arange(chunk['input_ids'].size(1)).unsqueeze(0)
        chunk['position_ids'] = position_ids
        
        output = model(**chunk)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        Scores += scores*(chunk['input_ids'].size(1)/total_length)
    
    ranking = np.argsort(Scores)[::-1]
    for i in range(Scores.shape[0]):
        l = labels[ranking[i]]
        s = Scores[ranking[i]]
        if printting :
            print(f"{i+1}) {l} {np.round(float(s), 4)}")

    return Scores


    
    