import re
from bs4 import BeautifulSoup
from datetime import datetime
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from math import ceil

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
