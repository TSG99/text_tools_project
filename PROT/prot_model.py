#!/usr/bin/env python
# coding: utf-8

# In[23]:


import os
import pandas as pd
from datasets import Dataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import precision_recall_fscore_support

folder_path = os.path.join(os.path.expanduser("~"), "Reddit_data", "Prepped")

all_data = []


for file_name in os.listdir(folder_path):
    
    if file_name.endswith('.csv'):  
        
        file_path = os.path.join(folder_path, file_name)
       
        try:
            df = pd.read_csv(file_path, encoding='ISO-8859-1')  
            all_data.append(df)
            
        except Exception as e:
            print(f"Error reading {file_name}: {e}")


df_all = pd.concat(all_data, ignore_index=True)

df_all = df_all[['comment', 'region']]  


label_encoder = preprocessing.LabelEncoder()

df_all['region'] = label_encoder.fit_transform(df_all['region'])

train_df, val_df = train_test_split(df_all, test_size=0.5, random_state=42)

train_dataset = Dataset.from_pandas(train_df)

val_dataset = Dataset.from_pandas(val_df)

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=len(label_encoder.classes_))



def tokenize_function(examples):
    
    return tokenizer(examples['comment'], padding="max_length", truncation=True, max_length=128)

train_dataset = train_dataset.map(lambda x: tokenize_function(x), batched=True)

val_dataset = val_dataset.map(lambda x: tokenize_function(x), batched=True)

train_dataset = train_dataset.map(lambda x: {'labels': x['region']}, batched=True)

val_dataset = val_dataset.map(lambda x: {'labels': x['region']}, batched=True)



def compute_metrics(p):
    
    preds = p.predictions.argmax(axis=-1)
    labels = p.label_ids
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1}

training_args = TrainingArguments(
    output_dir="./results",          
    evaluation_strategy="epoch",     
    learning_rate=2e-5,             
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    num_train_epochs=1,
    weight_decay=0.01,  
    logging_dir="./logs",)

trainer = Trainer(
    model=model,
    args=training_args
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics)

trainer.train()


# In[ ]:




