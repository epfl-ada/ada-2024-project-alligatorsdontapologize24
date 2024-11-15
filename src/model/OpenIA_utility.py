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
        #self.max_input = 128000 #maximum imput tokens for the model
        self.max_input = 8000 #maximum imput tokens for the model
        self.pricing = 1/1000000*0.150 #price per token
        self.encoder = tiktoken.encoding_for_model("gpt-4o-mini") #for gpt-4o-mini
        
        #prompt ingenieurring
        self.Label = """
        - **Peaceful**: The text describes no physical or psychological violence. There are no aggression, conflict, or harm to people or animals. Suitable for all audiences.
        - **Mild**: The level of violence is medium or uncertain. There might be moments of tension or mild conflict, such as arguments. Mild action or suspense is allowed.
        - **Violent**: The text describe extreme physical or psychological violence, such as physical aggression, conflict, or harm. Scenes may include fighting, injury, rape. It a prominent feature of the film."""        
        self.Instruction = "Assign a level of violence to each plot movie plot below. Respond with a dictionary where the keys are the plot numbers (e.g., 'plot1', 'plot2') and the values are the levels of violence ('Peaceful', 'Mild', 'Violent')"
        
        self.Example = """Here are some examples for each label :
        - **Peaceful**: plot1 :'norma and malcolm miochaels are a middle-aged married couple who are in the midst of a midlife crisis. both decide to separate and begin their lives anew away from each other. however, problems ensue once they discover that they are no longer as young as they used to be.'
        plot2:'in the 1840s, two sisters fall in love with the same man. while drunk, the man writes a letter proposing marriage to the wrong one.'
        plot3:'it is the final weekend of summer and a group of californian teenagers are looking forward to an upcoming surf contest. rival gangs the 'vals' and the 'lowks' are confident that they will take home the trophy, but things become complicated when reef yorpin  - leader of the lawks - discovers his sister allie  has fallen in love with 'val' surfer nick  after meeting at a beach party.'
        - **Mild**: plot1:'set in the 19th century, the plot centered around a man  who is falsely accused murder. the other side of the door was shot in monterrey, mexico.{{cite web}}'
        plot2:'in a desperate, but not-too-courageous, attempt to end his life, a man hires a murderer to do the job for him. soon, though, things are looking better and the he must now avoid the hit.'
        - **Violent**: plot1:'Richard Beck  is a police detective who believed that rape victims are to blame for the crime. He is later raped by two of the suspects he had been chasing. Ultimately, he changes his beliefs about rape victims. This made for TV movie was groundbreaking in that it portrayed the rape of a man by two other men, and because of this it has become a cult classic.'
        plot2:'newlywed carl  goes to war where he endures major suffering. back home, wife pauli  starves, becomes a prostitute to survive, and their baby dies.'
        """
        
        self.Content = f"### Violence scale : ###{self.Label}\n\n### Instructions ###\n{self.Instruction}"

        self.Prompt_size = self.count_tokens(self.Content) + self.count_tokens(self.Example)
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

    def format_batch(self,Data,size = 0):
        Text = ""
        for i in range(0,Data.shape[0]) :
            Text += self.format_plot(i+1,Data.iloc[i]['Plot'])
        #last check
        size = self.count_tokens(Text)
        if size > (self.max_input-self.Prompt_size) :
            raise Exception("ho ho.. this is too big")
        
        return Text

    def batch_plots(self,Data,size = 0):
        if size == 0:
            size = self.max_input
        print("size",self.Prompt_size)
        batch = [0]
        currentBatch = self.Prompt_size
        for i in range(0,Data.shape[0]):
            plot_tokens = self.count_tokens(self.format_plot(i+1,Data.iloc[i]["Plot"]))
            if currentBatch + plot_tokens > size:
                batch.append(i)
                #print("batch margin:",self.max_input-currentBatch)
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
            {"role": "user","content": Text},
            {"role": "assistant", "content": self.Example}
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
    
