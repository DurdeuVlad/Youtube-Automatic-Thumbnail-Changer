from asyncio.windows_events import NULL
import datetime
from msilib.schema import Error
from clients.yt_stats import YTstats
import time
import requests
import os
from pathlib import Path
from configparser import ConfigParser
from clients.youtube_client import YoutubeClient
from clients.youtube_title import YoutubeTitle

def get_current_date():
    today = datetime.date.today().__str__()
    return today

def get_next_date():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow=tomorrow.__str__()
    return tomorrow

YOUTUBE_DATA_API_CREDENTIALS_LOCATION = Path(__file__).parent.absolute().joinpath('creds/client_secret.json')
youtube_client = YoutubeClient(YOUTUBE_DATA_API_CREDENTIALS_LOCATION)
youtube_title = YoutubeTitle(YOUTUBE_DATA_API_CREDENTIALS_LOCATION)

def get_views(api:str, channel:str, video_id:str):
    Views = []

    part = 'statistics'
    yt = YTstats(api, channel)
    a = yt._get_single_video_data(video_id,part)
    Views.append(a['viewCount'])

    return Views

def get_api_key(folder_dir: Path):
    if(not Path.exists(folder_dir)):
        print("Could not find config file, creating a new one.")
        Path.touch(folder_dir)

        # Generate default config data.
        config = ConfigParser()
        config.add_section('main')
        config.set('main', 'api', 'HERE GOES YOUR APY KEY')
        config.set('main', 'channel_id', 'HERE GOES YOUR APY KEY')
        file = open(folder_dir, 'a')
        config.write(file)
        file.close()
        api_key="NULL"
        channel_id="NULL"
    else:
        # Grab configuration values.
        config = ConfigParser()
        config.read(folder_dir)

        # Grab the values.
        api_key = config.get('main', 'api')
        channel_id = config.get('main', 'channel_id')

    return api_key, channel_id

def change_thumbnail(video_id: str, thumbnail: str):
    response = youtube_client.set_thumbnail(video_id, thumbnail)

def change_title(video_id: str, title: str):
    response = youtube_title.change_title(video_id, title)

def rotate_thumbnails(rotation_time:int, rotation_counts:int, video_id:str, list_thumbnails):
    views = []
    api_key, channel_id = get_api_key(Path(__file__).parent.absolute().joinpath('creds/api_key'))
    if(rotation_counts<=0):
        rotation_counts=1
    for x in range(rotation_counts):
        print("Starting round #"+ str(x) +". Showing photos for " + str(rotation_time) + " seconds each.")
        for thumbnail in list_thumbnails:
            startViews =  int(get_views(api_key, channel_id, video_id)[0])
            print("Showing "+ str(thumbnail))
            change_thumbnail(video_id, thumbnail)
            time.sleep(rotation_time)
            endViews = int(get_views(api_key, channel_id, video_id)[0])
            
            if(x==0):
                views.append([endViews-startViews, thumbnail])
            else:
                views[x][0]+=endViews-startViews
    print(views)
    print("Sorted: ")
    views.sort(reverse=False)
    print(views)
    print("DONE!")
    return views

def rotate_thumbnails_titles(rotation_time:int, rotation_counts:int, video_id:str, list_thumbnails, list_titles):
    views = []
    api_key, channel_id = get_api_key(Path(__file__).parent.absolute().joinpath('creds/api_key'))
    if(rotation_counts<=0):
        rotation_counts=1
    for x in range(rotation_counts):
        print("Starting round #"+ str(x) +". Showing photos for " + str(rotation_time) + " seconds each.")
        for title in list_titles:
            for thumbnail in list_thumbnails:
                startViews =  int(get_views(api_key, channel_id, video_id)[0])
                print("Showing "+ str(thumbnail))
                change_thumbnail(video_id, thumbnail)
                change_title(video_id, title)
                time.sleep(rotation_time)
                endViews = int(get_views(api_key, channel_id, video_id)[0])
                
                if(x==0):
                    views.append([endViews-startViews, thumbnail, title])
                else:
                    views[x][0]+=endViews-startViews
    print(views)
    print("Sorted: ")
    views.sort(reverse=False)
    print(views)
    print("DONE!")
    return views

def rotate_titles(rotation_time:int, rotation_counts:int, video_id:str, list_titles):
    views = []
    api_key, channel_id = get_api_key(Path(__file__).parent.absolute().joinpath('creds/api_key'))
    if(rotation_counts<=0):
        rotation_counts=1
    for x in range(rotation_counts):
        print("Starting round #"+ str(x) +". Showing photos for " + str(rotation_time) + " seconds each.")
        for title in list_titles:
            startViews =  int(get_views(api_key, channel_id, video_id)[0])
            change_title(video_id, title)
            time.sleep(rotation_time)
            endViews = int(get_views(api_key, channel_id, video_id)[0])
                
            if(x==0):
                views.append([endViews-startViews, title])
            else:
                views[x][0]+=endViews-startViews
    print(views)
    print("Sorted: ")
    views.sort(reverse=False)
    print(views)
    print("DONE!")
    return views

def get_thumbnails(name: str):
    imagelist = []
    folder_dir = Path(__file__).parent.absolute().joinpath("thumbnails")
    folder_dir = folder_dir.joinpath(name)
    if(Path.exists(folder_dir)):
        for images in os.listdir(folder_dir):   
            # check if the image ends with png
            if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):
                print(images)
                imagelist.append(folder_dir.joinpath(images))
    else:
        print("Could not find folder, creating a new one.")
        try:
            Path.mkdir(folder_dir)
        except:
            pass
    print(imagelist)
    return imagelist

def get_settings(name: str):
    rotation_time = 0
    rotation_count = 0
    name = name+".ini"
    folder_dir = Path(__file__).parent.absolute()
    folder_dir = folder_dir.joinpath(name)
    generated_folder = not Path.exists(folder_dir)
    print(folder_dir)
    print(generated_folder)
    # Generate config file if it doesn't exist
    if(generated_folder):
        print("Could not find config file, creating a new one.")
        #Path.mkdir(folder_dir)
        Path.touch(folder_dir)

        # Generate default config data.
        config = ConfigParser()
        config.add_section('main')
        config.set('main', 'rotation_time', '20')
        config.set('main', 'rotation_count', '2')
        config.set('main', 'video_id', 'v84gOjUoqRs')
        config.set('main', 'thumbnail_folder', 'default')
        file = open(folder_dir, 'a')
        config.write(file)
        file.close()
    
    # Grab configuration values.
    config = ConfigParser()
    config.read(folder_dir)

    # Grab the values.
    rotation_time = config.get('main', 'rotation_time')
    rotation_count = config.get('main', 'rotation_count')
    video_id = config.get('main', 'video_id')
    thumbnail_folder = config.get('main', 'thumbnail_folder')
    print("rotation_time = "+ rotation_time)
    print("rotation_count = "+ rotation_count)
    print("video_id = "+ video_id)
    print("thumbnail_folder = "+ thumbnail_folder)
    rotation_time=int(rotation_time)
    rotation_count=int(rotation_count)
    return rotation_time, rotation_count, video_id, thumbnail_folder

def get_titles(thumbnail_folder:str):
    name = "titles.txt"
    folder_dir = Path(__file__).parent.absolute().joinpath("thumbnails")
    folder_dir = folder_dir.joinpath(thumbnail_folder)
    folder_dir = folder_dir.joinpath(name)
    generated_config = not Path.is_file(folder_dir)
    try:
        if(generated_config):
            print("Could not find config file, creating a new one at:")
            print(folder_dir)
            Path.touch(folder_dir)

            # Generate default config data.
            file = open(folder_dir, 'a')
            file.write("unu,doi,trei patru")
            file.close()
    except:
        pass

    file = open(folder_dir, 'r')
    titles = file.readlines()
    for x in range(len(titles)):
        titles[x]=titles[x].upper()
    file.close()
    return generated_config, titles

def check_thumbnail_folder(thumbnail_folder:str) -> bool:
    folder_dir = Path(__file__).parent.absolute().joinpath("thumbnails")
    folder_dir = folder_dir.joinpath(thumbnail_folder)
    generated_config = not Path.is_file(folder_dir)
    if(generated_config):
        try:
            Path.mkdir(folder_dir)
        except:
            pass
    return generated_config

def run():
    
    # Get settings: rotation_time, rotation_count, video_id, 
    print('Getting thumbnail config data...\n')
    time.sleep(5)
    rotation_time , rotation_count, video_id, thumbnail_folder = get_settings("config")

    time.sleep(5)
    print('Done getting thumbnail config data...\n')
    
    print('Getting title config data...\n')
    time.sleep(5)
    name = "titles.ini"
    folder_dir = Path(__file__).parent.absolute().joinpath("thumbnails")
    folder_dir = folder_dir.joinpath(thumbnail_folder)
    folder_dir = folder_dir.joinpath(name)
    generated_config = not Path.is_file(folder_dir)
    if(generated_config):
        print("Generated config file for titles.")
    read_again = input("Press one NOT to change the title:\n")
    if(read_again!='1'):
        generated_config, titles = get_titles(thumbnail_folder)
        if_changing_title=True
    else:
        if_changing_title=False
    time.sleep(5)
    print(titles)
    print('Done getting title config data...\n')

    print('Getting thumbnails...\n')
    time.sleep(5)
    # Get a list of all posible thumbnails DONE
    generated_folder=check_thumbnail_folder(thumbnail_folder)
    read_again = input("Generated thumbnail folder. Press 1 NOT to change thumbnails:\n")
    
    if(read_again!='1'):
        images = get_thumbnails(thumbnail_folder)
        if_changing_thumbnails=True
    else:
        if_changing_thumbnails=False
    time.sleep(5)
    print('Done getting thumbnails...\n')    

    
    # Change the thumbnails every rotationTime seconds and repeat for rotationCount
    # Gather the click ratio for every thumbnail test clip: v84gOjUoqRs
    print('Starting rotating thumbnails...\n')
    time.sleep(5)
    if(if_changing_thumbnails):
        if(if_changing_title):
            views = rotate_thumbnails_titles(rotation_time, rotation_count, video_id, images, titles)
        else:
            views = rotate_thumbnails(rotation_time, rotation_count, video_id, images)
    else:
        if(if_changing_title):
            views = rotate_titles(rotation_time, rotation_count, video_id, titles)
        else:
            print("Nothing to change.")
            return -1
    time.sleep(5)
    print('Done rotating thumbnails...\n')  

    #get_click_ratio(videoid)
    
    # Change thumbnail to the image with the best click ratio
    print('Putting the best performening thumbnail and title...\n')
    time.sleep(5)
    if(if_changing_thumbnails):
        change_thumbnail(video_id, views[0][1])
        if(if_changing_title):
            change_title(video_id, views[0][2])
    else:
        if(if_changing_title):
            change_title(video_id, views[0][1])
    time.sleep(5)
    print('Done putting the best performening thumbnail and title...\n')  

if __name__ == '__main__':
    run()