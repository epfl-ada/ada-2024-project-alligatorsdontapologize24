"""
DistillBERT Sentiment analysis script
--------------------------------------
This script implement a distill-BERT model, trained for sentiment analysis.
Given a text, the model return a sentiment analysis that sum to 1.
Result is a array :
"sadness": result[0],
 "joy": result[1],
 "love": result[2],
"anger": result[3],
"fear": result[4],
"surprise": result[5]
source : https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion
"""

# Use a pipeline as a high-level helper
from transformers import pipeline
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from torch.nn.functional import softmax
import numpy as np

pipe = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

class ViolenceDetector:
    def __init__(self):
        # Initialize tokenizer and model
        self.tokenizer = DistilBertTokenizer.from_pretrained("bhadresh-savani/distilbert-base-uncased-emotion")
        self.model = DistilBertForSequenceClassification.from_pretrained("bhadresh-savani/distilbert-base-uncased-emotion")
        
        self.space = self.tokenizer(" ")

    
    def preprocess_text(self, text):
        # Tokenize the text
        inputs = self.tokenizer(
            text,
            truncation=False,
            padding=True,
            return_tensors="pt"
        )

        # Max tokens per chunk
        max_length = 512
        total_length = inputs['input_ids'].size(1)

        # Split the input into chunks of max_length tokens
        input_ids = inputs['input_ids'][0] 
        attention_mask = inputs['attention_mask'][0]


        # Create chunks
        input_id_chunks = [input_ids[i:i + max_length] for i in range(0, len(input_ids), max_length)]
        attention_mask_chunks = [attention_mask[i:i + max_length] for i in range(0, len(attention_mask), max_length)]
        

        # Convert chunks back to tensors with correct batch dimension
        chunked_inputs = [{'input_ids': ids.unsqueeze(0), 'attention_mask': mask.unsqueeze(0)} 
                  for ids, mask in zip(input_id_chunks, attention_mask_chunks)]

        return chunked_inputs,total_length
    
    def analyze_violence(self, plot_text):
        inputs,total_length = self.preprocess_text(plot_text)

        prediction_score = torch.zeros(6)

        with torch.no_grad():
            for part in inputs :
                outputs = self.model(**part)
                predictions = softmax(outputs.logits, dim=1)
                prediction_score += predictions[0] * (part['input_ids'].size(1) / total_length)

            
        return prediction_score.numpy()


        

