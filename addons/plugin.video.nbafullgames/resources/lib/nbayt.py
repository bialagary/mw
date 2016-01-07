from webutils import *
import json
YOUTUBE_API_KEY='AIzaSyAO7A3iaRS6RJOYUf-o9caPPK-aiMcrnEk'


def get_channel_id_from_uploads_id(uploads_id):
    url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&id=%s&key=%s'%(uploads_id,YOUTUBE_API_KEY)
    read=read_url(url)
    decoded_data=json.loads(read)
    channel_id=decoded_data['items'][0]['snippet']['channelId']

    return channel_id

def get_playlists2(channelID,page):

    channelID=get_channel_id_from_uploads_id(channelID)

    if page=='1':
        url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=10&key=%s'%(channelID,YOUTUBE_API_KEY)
    else:#
        url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=10&pageToken=%s&key=%s'%(channelID,page,YOUTUBE_API_KEY)
    read=read_url(url)
    decoded_data=json.loads(read)
    playlists=[]
    try:
        next_page=decoded_data['nextPageToken']
    except:
        next_page='1'
    playlists.append(next_page)
    for i in range(len(decoded_data['items'])):
        if decoded_data['items'][i]['kind']=='youtube#playlist':
            playlist_id=decoded_data['items'][i]['id']
            playlist_name=decoded_data['items'][i]['snippet']['title']
            thumb=decoded_data['items'][i]['snippet']['thumbnails']['high']['url']

            playlists.append([playlist_id,playlist_name,thumb])
    return playlists
def get_latest_from_youtube(playlist_id,page):
    
    if page=='1':
        req_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId=%s&key='%playlist_id+YOUTUBE_API_KEY
    else:
        req_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken=%s&maxResults=20&playlistId=%s&key='%(page,playlist_id)+YOUTUBE_API_KEY
    
    read=read_url(req_url)
    decoded_data=json.loads(read)
    listout=[]
    try:
        next_page=decoded_data['nextPageToken']
    except:
        next_page='1'
    listout.append(next_page)
    for x in range(0, len(decoded_data['items'])):
        try:
            title=decoded_data['items'][x]['snippet']['title']
            video_id=decoded_data['items'][x]['snippet']['resourceId']['videoId']
            thumb=decoded_data['items'][x]['snippet']['thumbnails']['high']['url']
            desc=decoded_data['items'][x]['snippet']['description']
            listout.append([title,video_id,thumb,desc])
        except: pass #video is private
    return listout


def get_playlists(page):
    channelID='UCWJ2lWNubArHWmf3FIHbfcQ'

    if page=='1':
        url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=10&key=%s'%(channelID,YOUTUBE_API_KEY)
    else:#
        url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=10&pageToken=%s&key=%s'%(channelID,page,YOUTUBE_API_KEY)
    read=read_url(url)
    decoded_data=json.loads(read)
    playlists=[]
    try:
        next_page=decoded_data['nextPageToken']
    except:
        next_page='1'
    playlists.append(next_page)
    for i in range(len(decoded_data['items'])):
        if decoded_data['items'][i]['kind']=='youtube#playlist':
            playlist_id=decoded_data['items'][i]['id']
            playlist_name=decoded_data['items'][i]['snippet']['title']
            thumb=decoded_data['items'][i]['snippet']['thumbnails']['high']['url']

            playlists.append([playlist_id,playlist_name,thumb])
    return playlists

def get_latest_from_youtube(playlist_id,page):
    
    if page=='1':
        req_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId=%s&key='%playlist_id+YOUTUBE_API_KEY
    else:
        req_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken=%s&maxResults=20&playlistId=%s&key='%(page,playlist_id)+YOUTUBE_API_KEY
    
    read=read_url(req_url)
    decoded_data=json.loads(read)
    listout=[]
    try:
        next_page=decoded_data['nextPageToken']
    except:
        next_page='1'
    listout.append(next_page)
    for x in range(0, len(decoded_data['items'])):
        try:
            title=decoded_data['items'][x]['snippet']['title']
            video_id=decoded_data['items'][x]['snippet']['resourceId']['videoId']
            thumb=decoded_data['items'][x]['snippet']['thumbnails']['high']['url']
            desc=decoded_data['items'][x]['snippet']['description']
            listout.append([title,video_id,thumb,desc])
        except: pass #video is private
    return listout
