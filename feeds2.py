#!usr/bin/python
import re
import datetime
import urllib2
import feedparser

def update_feeds(url):
    derror = None
    guid = None
    dtMax = None
    dtMod = None
    try:
		d = feedparser.parse(url)
    except urllib2.URLError, e:
        print url
        print e
        return
    if d.get('status', 200) in (200, 307):
        cc=[{"author":"","title":"","content":"","description":"","link":""}]
        for entry in d.entries:
            try:
                dt = datetime.datetime.now()
                if entry.has_key('updated_parsed') and entry.updated_parsed:
                    dt = datetime.datetime(*entry.updated_parsed[:6])
                content = entry.get('content', [{'value':''}])[0]['value']
                description = entry.get('description', '')
                title = entry.get('title', 'Untitled')
                author = entry.get('author','Anonymous')
                link = entry.link
                cc+=[{"author":author,"title":title,"content":content,"description":description,"link":link}]
            except Exception, e:
                pass
    elif d.status in (301, 302, 303):
        url = d.get('href', url)
    elif d.status in (304,):
        pass
    else:
        derror = int(d.status)
    return cc

url='http://talentcalling.wordpress.com/feed/'
cd=update_feeds(url)
