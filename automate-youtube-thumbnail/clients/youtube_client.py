import errno
import os
from urllib import response

from googleapiclient.http import MediaFileUpload
import google_auth_oauthlib.flow
import googleapiclient.discovery
import argparse


class YoutubeClient(object):
    def __init__(self, credentials_location:str):
        #youtube_dl.utils.std_headers['User-Agent']= "faceboookexternalhit/1.1 (+http://www.facebook.com/externalhitt_uatext.php)"
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"]= "1"

        api_service_name = "youtube"
        api_version = "v3"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(credentials_location, scopes)
        credentials = flow.run_console()
        
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        self.youtube_client = youtube_client

    def set_thumbnail(self, video_id:str, thumbnail:str):
        request = self.youtube_client.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail)
        )
        response = request.execute()
        return response