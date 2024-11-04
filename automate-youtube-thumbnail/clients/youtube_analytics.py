import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from numpy import deprecate


SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
@deprecate
class YoutubeClientAnalytics(object):
    def __init__(self, credentials_location):
        #youtube_dl.utils.std_headers['User-Agent']= "faceboookexternalhit/1.1 (+http://www.facebook.com/externalhitt_uatext.php)"
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"]= "1"
        
        flow = InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)
        credentials = flow.run_console()
        
        youtube_client = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials)
        
        self.youtube_client = youtube_client




        
    def execute_api_request(self, **kwargs):
        response = self.youtube_client.reports().query(
        **kwargs
    ).execute()
        print(response)

    # youtubeAnalytics = get_service()
    # execute_api_request(
    #  youtubeAnalytics.reports().query,
    #  ids='channel==MINE',
    #  startDate='2017-01-01',
    #  endDate='2017-12-31',
    #  metrics='estimatedMinutesWatched,views,likes,subscribersGained'
    #  dimensions='day',
    #  sort='day'
  #)
    # 
    # 
    # 
    # 
    #    



