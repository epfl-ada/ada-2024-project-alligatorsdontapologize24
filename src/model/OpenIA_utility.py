"""
GPT4mini custom model with utility functions
--------------------------------------
This script regroup all the utility functions for the LLM, and implement the model.
"""

import numpy as np
import pandas as pd
import os
import tiktoken
import openai
from openai import OpenAI
import json


class GPT4mini_ViolenceClassifier:
    def __init__(self):
        #API parameters
        #key (toc toc)
        openai.api_key = os.environ["OPENAI_API_KEY"]
        #
        self.client = OpenAI()

        #model parameters
        self.max_input = 128000 #maximum imput tokens for the model
        self.pricing = 1/1000000*0.150 #price per token
        self.encoder = tiktoken.encoding_for_model("gpt-4o-mini") #for gpt-4o-mini
        
        #prompt ingenieurring
        self.Label = """
        - **Peaceful**: The text describes no violence. There are no aggression, conflict, or harm to people or animals. Suitable for all audiences, including children and sensitive viewers.
        - **Mild**: The level of violence of the text is minimal or uncertain. There might be moments of tension or mild conflict, such as arguments. ÒÒMild action or suspense is allowed without explicit harm.
        - **Violent**: The text describe violence, such as physical aggression, conflict, or harm. Scenes may include fighting, injury, or other intense confrontations. It a prominent feature of the film."""
        
        self.Instruction = "Assign a violence level from the scale above to each movie plot provided below."
        self.Example = ""
        self.Content = f"### Violence scale : ###{self.Label}\n\n### Instructions ###\n{self.Instruction}"

        self.Prompt_size = self.count_tokens(self.Content)
        #function
        self.function = {
           "name": "Assign_violence_level",
           "description": "Predict the level of violence of a list of movie plots",
           "parameters": {
               "type": "object",
               "properties": {
                   "prediction": {
                       "type": "array",
                       "items": {
                           "type": "string",
                           "enum": [
                               "Peaceful",
                               "Mild",
                               "Violent"
                           ]
                       },
                       "description": "The list of violence levels for each movie plot, in the same order as the plots were provided."
                   }
               },
               "required": [
                   "prediction"
               ]
           }
        }
    
    def count_tokens(self,text):
        return len(self.encoder.encode(text))

    def format_plot(self,i,text):
        return f"plot{i}:{text}\n\n"

    def format_batch(self,Data):
        Text = ""
        for i in range(0,Data.shape[0]) :
            Text += self.format_plot(i+1,Data.iloc[i]['Plot'])
        #last check
        size = self.count_tokens(Text)
        if size > (self.max_input-self.Prompt_size) :
            raise Exception("ho ho.. this is too big")
        
        return Text

    def batch_plots(self,Data):
        print("prompt size",self.Prompt_size)
        batch = [0]
        currentBatch = self.Prompt_size
        for i in range(0,Data.shape[0]):
            plot_tokens = self.count_tokens(self.format_plot(i+1,Data.iloc[i]["Plot"]))
            if currentBatch + plot_tokens > self.max_input:
                batch.append(i)
                print("batch margin:",self.max_input-currentBatch)
                currentBatch = self.Prompt_size
            else:
                currentBatch += plot_tokens
        print("Final number of batchs",len(batch))
        return batch

    def Call_API(self,Text):
        #call the API
        completion = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": self.Content},
            {"role": "user","content": Text}
        ],
        functions=[self.function],
        function_call={"name": "Assign_violence_level"},
    )
        #extract the answer
        try:
            prediction = json.loads(completion.choices[0].message.function_call.arguments)["prediction"]
            return prediction
            #prediction = completion.choices[0].message
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error extracting prediction: {e}")
            return completion
    
