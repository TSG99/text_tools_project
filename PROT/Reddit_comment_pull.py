#!/usr/bin/env python
# coding: utf-8

# In[4]:


import time
import os
import praw

#Login
reddit = praw.Reddit(client_id= , #Get this from the reddit dev site when you select create script
                     client_secret= , #Get from the same place as client ID
                     user_agent='comment_puller 1.0 by /u/GST_99', #Feel free to change this if you want, if you do:
                     ratelimit_status=True)                        #Just replace my script name and username with yours

#Split into two separate lists to prevent request limit errors
state_list1 = ['Alabama', 'alaska', 'arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
             'Delaware', 'florida', 'Georgia', 'Hawaii', 'Idaho', 'illinois']

state_list2 = ['Indiana', 'Iowa', 'kansas', 'Kentucky',
             'Louisiana', 'Maine', 'maryland', 'massachusetts', 'Michigan', 'minnesota', 'mississippi', 'missouri']

state_list3 = ['Montana', 'Nebraska', 'Nevada', 'newhampshire', 'newjersey', 'NewMexico', 'newyork', 'NorthCarolina', 
             'northdakota', 'Ohio', 'oklahoma', 'oregon', 'Pennsylvania']
               
state_list4 = ['RhodeIsland', 'southcarolina', 'SouthDakota', 
             'Tennessee', 'texas', 'Utah', 'vermont', 'Virginia', 'Washington', 'WestVirginia', 'wisconsin', 'wyoming']

def data_pull(state_list):
    
    for sub_name in state_list:
    
        subreddit = reddit.subreddit(sub_name)

        #Set main folder name
        bdir = os.path.join('Reddit_data', 'Raw') 

        #Sets subfolder name
        subdir = os.path.join(bdir, sub_name) 

        #Creates the folders if they do not exist
        os.makedirs(subdir, exist_ok=True) 

         #Starts the loop for grabbing the top 10 posts
        for submission in subreddit.hot(limit=10):
    
            post_title = submission.title
    
            #Stops post titles from breaking my script and limits filenames to 50 words
            filtered_title = ''.join(c for c in post_title if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
    
            #Names file and sets path
            file_name = f"{filtered_title}.txt"
            file_path = os.path.join(subdir, file_name)

            #Check if the post has any comments
            if len(submission.comments) == 0:
                print(f"Skipping post with no comments: {post_title}")
                continue  # Skip this post and move on to the next

            #Save the comments of the post to a file
            with open(file_path, 'w', encoding='utf-8') as file:
        
                #Write the title separated from the rest of the doc with a '-'
                file.write(f"Title: {submission.title}\n-\n")
        
                #Checks all comments are loaded
                submission.comments.replace_more(limit=None)
        
                #Write comments separated by '*'
                for comment in submission.comments.list():
                    file.write(f"{comment.body}\n*\n")
            
            print(f"Comments saved for post: {submission.title}")
        
        
          
        print(f"All comments have been saved in the '{subdir}' directory.")

#pull data from first list
data_pull(state_list1)

#Wait for pull limit to reset smh
time.sleep(60)

#pull data from second list
data_pull(state_list2)

#keep waiting...
time.sleep(60)

data_pull(state_list3)

#still waiting...
time.sleep(60)

data_pull(state_list4)


# In[ ]:




