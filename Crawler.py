import inspect
import os
import sqlite3
import pafy
import urllib
import re

def insert_data(video_url,title,duration,views,thumb_url,thumb_path,original_thumb_url,original_thumb_path):
    db_connection = sqlite3.connect('youtube.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        """INSERT INTO YOUTUBE_DATA (video_url , title, \
                   duration  , views  , thumb_img_url , thumb_img_path , big_thumb_url \
                   ,big_thumb_path ) values (?,?,?,?,?,?,?,?)""", [
            video_url, title,duration, views, thumb_url, thumb_path, original_thumb_url, original_thumb_path]
        )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

def get_playlist_data(playlist_url):
    playlist = pafy.get_playlist(playlist_url)
    for i in range(len(playlist['items'])) :
        video= playlist['items'][i]['pafy']
        thumb_path = current_path+'Thumb\\'+'thumb%d.jpg' % i
        bigthumb_path = current_path + 'Original_Thumb\\'+'bigthumb%d.jpg' % i
        urllib.urlretrieve(video.thumb, thumb_path)
        urllib.urlretrieve(video.bigthumb, bigthumb_path)
        insert_data(video.watchv_url, video.title, video.duration, video.viewcount, video.thumb , thumb_path,
         video.bigthumb, bigthumb_path)
    db_cursor.close()
    db_connection.close()

def get_channel_data(playlist_url):
    re_filter = r'<a.*?/a>'
    read_url = urllib.urlopen(playlist_url)
    all_links_temp = re.findall(re_filter, read_url.read(), re.MULTILINE)
    video_link_class = 'class="yt-uix-sessionlink yt-uix-tile-link'
    video_titles = []
    video_links = []
    for temp in all_links_temp:
        if video_link_class in temp:
            title_filter = r'title=".*?"'
            video_title_temp = re.findall(title_filter, temp, re.MULTILINE)
            video_titles.append(video_title_temp)
            url_filter = r'href=".*?"'
            video_link_temp = re.findall(url_filter, temp, re.MULTILINE)
            video_links.append(video_link_temp)
    j = 0
    for i in video_titles:
        temp_title = str(i)
        temp_title = temp_title[9:-3]
        temp_link = str(video_links[j])
        temp_link = "https://www.youtube.com"+temp_link[8:-3]
        video = pafy.new(temp_link)
        thumb_path = current_path+'Thumb\\'+'thumbs%d.jpg' % j
        bigthumb_path = current_path + 'Original_Thumb\\'+'bigthumbs%d.jpg' % j
        urllib.urlretrieve(video.thumb, thumb_path)
        urllib.urlretrieve(video.bigthumb, bigthumb_path)
        insert_data(video.watchv_url, video.title, video.duration, video.viewcount, video.thumb, thumb_path,
                    video.bigthumb, bigthumb_path)
    db_cursor.close()
    db_connection.close()
    j = j + 1

current_path = inspect.getfile(inspect.currentframe())+r'images\\'
current_path= current_path.replace('Crawler.py','')
current_path= current_path.replace("\\\\",'\\')
db_connection = sqlite3.connect('youtube.db')
db_cursor = db_connection.cursor()
db_cursor.execute('CREATE TABLE IF NOT EXISTS YOUTUBE_DATA (ID INTEGER PRIMARY KEY, video_url  varchar, title varchar, \
                   duration text , views Integer , thumb_img_url varchar, thumb_img_path varchar, big_thumb_url varchar\
                   ,big_thumb_path varchar)')
url = "https://www.youtube.com/user/AsapSCIENCE/videos"
if 'list' in  url:
    get_playlist_data(url)
else:
            get_channel_data(url)

