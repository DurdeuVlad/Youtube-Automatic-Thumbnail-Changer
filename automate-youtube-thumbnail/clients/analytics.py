# -*- coding: utf-8 -*-

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

class Analytics():

    def __init__(self, credentials_location):
        flow = InstalledAppFlow.from_client_secrets_file(credentials_location, SCOPES)
        credentials = flow.run_console()
        youtube_client = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
        self.youtube = youtube_client

        
    def execute_api_request(self, videoid: str, today: str, tomorrow: str):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        response = self.youtube.reports().query(
            ids='channel==MINE',
            filters='video=='+videoid,
            dimensions='video',
            metrics='views',
            sort='views'
        ).execute()
        return response

          

    

  

