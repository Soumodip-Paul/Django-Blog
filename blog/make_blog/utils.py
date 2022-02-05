import re, requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse,Http404
from django.shortcuts import redirect, render as Render
from django.utils import timezone
from math import ceil
from .models import UserModel, YoutubeCoursePlayList, YoutubeVideo

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class Pages:
    listItem = None
    pages = 0
    p = 0
    def __init__(self,listItem,pages:int,p:int):
        self.listItem = listItem
        self.pages =pages
        self.p = p  

class InternalServerError(HttpResponse):
    status_code = 500
    def __init__(self, content: object = ..., *args, **kwargs) -> None:
        print(content)
        super().__init__(content="Internal server error", *args, **kwargs)

def isEmail(email : str) -> bool:
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def pretty_date(time=False) -> str:
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = timezone.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"

def prettyFilter(blogs): 
    for blog in blogs :
        blog.blog_date = pretty_date(blog.blog_date)
        blog.blog_content = BeautifulSoup(blog.blog_content,"html.parser").get_text()
    return blogs
      
def paginateResults(req: HttpRequest, filter_list, ResultPerPage:int, Redirect:str) -> Pages:
    pages = ceil(len(filter_list) / ResultPerPage)
    p = int(req.GET.get('p') or 1)
    if pages > 0 and p > pages or p < 1: return redirect(Redirect)
    else : return Pages(listItem=filter_list[ (p - 1) * ResultPerPage: p * ResultPerPage],pages=pages,p=p)
       
def urlify(s : str) -> str:

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s

def render(req:HttpRequest, template_name:str, context =None):
    from .config import config as CONFIG
    item_dict = {'testimonial' : getTestimonial(), 'config': CONFIG}
    if context is not None:
        for item in context:
            item_dict[item] = context[item]
    return Render(req,template_name,item_dict)

def renderPage(req:HttpRequest, name:str, pages) -> HttpResponse:
    from .config import config as CONFIG     
    if pages != None and len(pages) != 0 :
        page = pages[0]
        page.page = page.page.format(site_domain=CONFIG.site_domain,site_name=CONFIG.site_name,contact_email=CONFIG.contact_email)
        return render(req, 'page.html', { 'pageName' : name, 'page' : page, 'desc': BeautifulSoup(page.page,'html.parser').get_text()})
    else : raise Http404()

def getTestimonial():
    userModels = UserModel.objects.exclude(star_ratings__lte=2).filter(testimonial=True)
    userModels = userModels.order_by('-star_ratings')[:4]
    userModels.starRange = range(5)
    for item in userModels:
        item.star_ratings = int(item.star_ratings)
    return userModels

def getPlayListdata(obj : YoutubeCoursePlayList, req: HttpRequest = None):
    from .config import config as CONFIG
    if (CONFIG.youtube_api_key == None or len(CONFIG.youtube_api_key) == 0): 
        if (req != None) : messages.warning(req, 'No Api Key')
        return
    playlist_id = obj.playlist_id
    response = requests.get(url="https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&id={list_id}&key={api_key}".format(list_id=playlist_id,api_key=CONFIG.youtube_api_key))
    response2 = requests.get(url="https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&part=id&part=snippet&part=status&maxResults=50&playlistId={id}&key={api_key}".format(id=playlist_id,api_key=CONFIG.youtube_api_key))
    if response.status_code != 200 or response2.status_code != 200 : 
        if (req != None) : messages.warning(req, 'Forbidden')
        return 
    data = response.json()['items'][0]
    data2 = response2.json()['items']
    obj_data = data['snippet']
    obj.course_title = obj_data['title']
    obj.course_description = obj_data['description']
    obj.video_thumbnail_default = obj_data['thumbnails']['default']['url']
    obj.video_thumbnail_medium = obj_data['thumbnails']['medium']['url']
    obj.video_thumbnail_high = obj_data['thumbnails']['high']['url']
    obj.video_thumbnail_standard = obj_data['thumbnails']['standard']['url']
    obj.save()
    for item in data2:
        snippet = item['snippet']
        object = YoutubeVideo.objects.get_or_create(video_id=snippet['resourceId']['videoId'])
        video : YoutubeVideo = object[0]
        print(snippet,video,)
        # video.video_id = snippet['resourceId']['videoId']
        video.video_title = snippet['title']
        video.video_description = snippet['description'] 
        video.video_thumbnail_default = snippet['thumbnails']['default']['url']
        video.video_thumbnail_high = snippet['thumbnails']['high']['url']
        video.video_thumbnail_medium = snippet['thumbnails']['medium']['url']
        video.video_thumbnail_standard = snippet['thumbnails']['standard']['url']
        video.save()
        obj.videos.add(video)
    obj.save()

def getYoutubeVideoData(obj : YoutubeVideo, req: HttpRequest = None):
    from .config import config as CONFIG
    if (CONFIG.youtube_api_key == None or len(CONFIG.youtube_api_key) == 0): 
        if (req != None) : messages.warning(req, 'No Api Key')
        return
    video_id = obj.video_id
    response = requests.get(url="https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}".format(id=video_id,api_key=CONFIG.youtube_api_key))
    if response.status_code != 200 : 
        if (req != None) : messages.warning(req, 'Forbidden')
        return 
    obj_data = response.json()['items'][0]['snippet']
    obj.video_title = obj_data['title']
    obj.video_description = obj_data['description']
    obj.video_thumbnail_default = obj_data['thumbnails']['default']['url']
    obj.video_thumbnail_medium = obj_data['thumbnails']['medium']['url']
    obj.video_thumbnail_high = obj_data['thumbnails']['high']['url']
    obj.video_thumbnail_standard = obj_data['thumbnails']['standard']['url']
    obj.save()
    return