import streamlit as st
import sklearn
import pickle
from PIL import Image
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret2.json"

# Get credentials and create an API client
PATH = "credentials.json"
credentials = None

#If there are credentials
if os.path.exists(PATH):
  with open(PATH, 'r') as token:
    credentials_info = json.loads(token.read())
    credentials = Credentials.from_authorized_user_info(credentials_info, scopes=scopes)

#If there are no (valid) credentials available
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      credentials.refresh(Request())
    else:
      flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
      credentials = flow.run_console()
    with open(PATH, 'w') as token:
      token.write(credentials.to_json())

youtube = googleapiclient.discovery.build(
  api_service_name, api_version, credentials=credentials)


# Load the API key
API_KEY = "AIzaSyC5lwj-aOTq2__vuD755pVRzOPB7xPLPsg" # API key (plz don't use my API Key...I didn't set it to an environment var)
youtube2 = googleapiclient.discovery.build(
  api_service_name, api_version, developerKey=API_KEY) 

#Saved ML Model
with open('spam_model.pkl', 'rb') as model_file:
  loaded_model = pickle.load(model_file)

col1, col2 = st.columns(2)

with col1:
  st.header("CyberBuddy")
  image = Image.open('cyberbuddy.png')
  st.image(image)

with col2:
  st.write("\n")
  st.write("\n")
  st.write("\n")
  #Youtube Link: https://www.youtube.com/watch?v=ZxMtS-Pq3jE
  link = st.text_input(
    "Enter your Youtube Link 👇"
  )  
  
  if st.button("Submit"):
    video_id = link.split("=")[-1] #get id
    # Use the YouTube Data API to retrieve comments
    comments = youtube2.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    ).execute()
  
    moderation_status = "rejected" 
  
    # Extract the comments and comment IDs from the response
    for comment in comments["items"]:
        comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        comment_id = comment["id"]
        author_name = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        author_id = comment["snippet"]["topLevelComment"]["snippet"]["channelId"] #channel id of comment's author
        # Make predictions using the loaded model
        if loaded_model.predict([comment_text]) == 1: #check if comment is spam
          #remove their comment
          youtube.comments().setModerationStatus(
              id=comment_id,
              moderationStatus=moderation_status
          ).execute()
          spam_comments['users'].append(author_name)
          spam_comments['comments'].append(comment_text)
          
    st.write(":green[Success] :sunglasses:")
    


