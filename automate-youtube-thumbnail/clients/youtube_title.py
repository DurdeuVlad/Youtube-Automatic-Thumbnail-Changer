# Update the snippet metadata for a video. Sample usage:
#   python update_video.py --video_id=<VIDEO_ID> --tags="<TAG1, TAG2>" --title="New title" --description="New description"

import argparse
import os
from pathlib import Path

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

class YoutubeTitle:

    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
    # the {{ Google Cloud Console }} at
    # {{ https://cloud.google.com/console }}.
    # Please ensure that you have enabled the YouTube Data API for your project.
    # For more information about using OAuth2 to access the YouTube Data API, see:
    #   https://developers.google.com/youtube/v3/guides/authentication
    # For more information about the client_secrets.json file format, see:
    #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    CLIENT_SECRETS_FILE = Path(__file__).parent.absolute().joinpath('creds/client_secret.json')
    # This OAuth 2.0 access scope allows for full read/write access to the
    # authenticated user's account.
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'


    def __init__(self, client_secret_file):
        self.CLIENT_SECRETS_FILE = client_secret_file
        flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
        credentials = flow.run_console()
        self.youtube_client = build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)


    # Authorize the request and store authorization credentials.

    def update_video(self, title:str, video_id:str):
        # Call the API's videos.list method to retrieve the video resource.
        videos_list_response = self.youtube_client.videos().list(
            id=video_id,
            part='snippet'
        ).execute()

        # If the response does not contain an array of 'items' then the video was
        # not found.
        if not videos_list_response['items']:
            print('Video '+video_id+' was not found.')

        # Since the request specified a video ID, the response only contains one
        # video resource. This code extracts the snippet from that resource.
        videos_list_snippet = videos_list_response['items'][0]['snippet']

        # Set video title, description, default language if specified in args.
        videos_list_snippet['title'] = title
        # if args.description:
        #     videos_list_snippet['description'] = args.description

        # Preserve any tags already associated with the video. If the video does
        # not have any tags, create a new array. Append the provided tag to the
        # list of tags associated with the video.
        # if 'tags' not in  videos_list_snippet:
        #     videos_list_snippet['tags'] = []
        # if args.tags:
        #     videos_list_snippet['tags'] = args.tags.split(',')
        # elif args.add_tag:
        #     videos_list_snippet['tags'].append(args.add_tag)

        #print(videos_list_snippet)

        # Update the video resource by calling the videos.update() method.
        videos_update_response = self.youtube_client.videos().update(
            part='snippet',
            body=dict(
            snippet=videos_list_snippet,
            id=video_id
            )).execute()

        print('The updated video metadata is:\n' +
                'Title: ' + videos_update_response['snippet']['title'] + '\n')
        # if videos_update_response['snippet']['description']:
        #     print ('Description: ' +
        #         videos_update_response['snippet']['description'] + '\n')
        # if videos_update_response['snippet']['tags']:
        #     print ('Tags: ' + ','.join(videos_update_response['snippet']['tags']) + '\n')

    def change_title(self, video_id:str, title:str):
        try:
            self.update_video(title, video_id)
        except HttpError:
            print('error: ')
            print(HttpError)