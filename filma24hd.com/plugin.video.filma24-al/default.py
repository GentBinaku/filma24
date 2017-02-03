#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys, xbmc
import xbmc,xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus
import resolvers
import urlresolver
#import rpdb2
#rpdb2.start_embedded_debugger('pw')

hostDict = ['allvid', 'exashare', 'filepup', 'filepup2', 'nosvideo', 'nowvideo', 'openload', 'vidlockers', 'streamcloud', 'streamin', 'vidspot', 'vidto', 'xvidstage', 'nosvideo', 'nowvideo', 'vidbull', 'vodlocker', 'vidto', 'youwatch', 'videomega', 'vidlox', 'estream', 'thevideo', 'watchers']

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.filma24-al"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
       
#Host = "http://www.filma24-al.com/movie-genre/aventure/"
def getUrl(url):
        pass#print "Here in getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	yield link
	
def showContent():
        names = []
        urls = []
        names.append("Aksion")
        urls.append("http://www.filma24.tv/aksion")
        names.append("Aventure")
        urls.append("http://www.filma24.tv/aventure")
        names.append("Fantazi")
        urls.append("http://www.filma24.tv/fantazi")
        names.append("Drame")
        urls.append("http://www.filma24.tv/drame")
        names.append("Horror")
        urls.append("http://www.filma24.tv/horror")
        names.append("Hindi")
        urls.append("http://www.filma24.tv/hindi")
        names.append("Komedi")
        urls.append("http://www.filma24.tv/komedi")
        names.append("Krim")
        urls.append("http://www.filma24.tv/krim")
        names.append("Romance")
        urls.append("http://www.filma24.tv/romance")
        names.append("Thriller")
        urls.append("http://www.filma24.tv/thriller")
        names.append("Filma 24 HD")
        urls.append("http://www.filma24hd.com/")
        for name,url in zip(names,urls):
                pic = " "
                addDirectoryItem(name, {"name":name, "url":url, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
        
def getPage(name, url):
                #http://www.filma24.tv/aksion/page/2/
                for page in range(1,11):
                        url1 = url + "/page/" + str(page) + "/"
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)
        
        

def getVideos(name1, urlmain):
        url = urlmain
	content = getUrl(url)
	pass#print "content A =", content
        if ("http://www.filma24.tv" in urlmain):
            regexvideo = 'div class="movie-thumb".*?background-image:url\((.*?)\).*?<a href="(.*?)".*?<h4>(.*?)<'
            match = re.compile(regexvideo, re.DOTALL).findall(content)
        elif ("http://www.filma24hd.com" in urlmain):
            regexvideo = '<img src="(.*.jpg)"\s.*\s+</a>\s+<h2>\s+<a href="(.*)"\stitle="(.*)"'
            match = re.compile(regexvideo).findall(content)
        pass#print "match =", match
        for pic, url, name in match:
            if ("http://www.filma24.tv" in urlmain):
                addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
            elif ("http://www.filma24hd.com" in urlmain):
                addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)


#	name = "More videos"
#	addDirectoryItem(name, {"name":name, "url":urlmain, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
        
def getVideos2(name1, urlmain):
        url = urlmain + "&paged=2"
	content = getUrl(url)
	pass#print "content B =", content

	regexvideo = 'div class="boxim.*?a href="(.*?)".*?Boxoffice\/timthumb.*?src=(.*?)\&amp.*?div class="btitle.*?title=".*?>(.*?)<'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, pic, name in match:
                 ##pass#print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
	name = "More videos"
	addDirectoryItem(name, {"name":name, "url":urlmain, "mode":4}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
        	        		
def getVideos3(name1, urlmain):
        url = urlmain + "&paged=3"
	content = getUrl(url)
	pass#print "content B1 =", content

	regexvideo = 'div class="boxim.*?a href="(.*?)".*?Boxoffice\/timthumb.*?src=(.*?)\&amp.*?div class="btitle.*?title=".*?>(.*?)<'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, pic, name in match:
                 ##pass#print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         

def getVideos4(name, url):
    pass#print "In getVideos4 url A=", url
    content = getUrl(url)
    pass#print "content C =", content
    if ("http://www.filma24.tv" in url):
        n1 = content.find('"watch-links"', 0)
        n2 = content.find('!-- End Downloads Links -->', n1)
        content = content[n1:n2]
        pass#print "content B=", content
        regexvideo = 'a href="(.+?)".*?<li class="(.+?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        mode_one=6
    elif ("http://www.filma24hd.com" in url):
        regexvideo = 'shape="poly" href="(htt\w+://(.*)\.\w+\/.*)"\starget'
        match = re.compile(regexvideo).findall(content)
        mode_one = 7
    pass#print "match B=", match
    for url, name in match:
           if not name.lower() in hostDict:
                  continue
           pic = " "
           pass#print "name B=", name
           pass#print "url B=", url
           addDirectoryItem(name, {"name":name, "url":url, "mode":mode_one}, pic)
    
    xbmcplugin.endOfDirectory(thisPlugin)
    
def getVidurl(name, url):
          name = name.lower()
          pass#print "In getVidurl url =", url
          pass#print "In getVidurl name =", name
          if ("nowvideo" in name) or ("nowvideo" in url):
                   pass#print "In getVidurl nowvideo url 2=", url
                   from resolvers.nowvideo import resolve
        
          elif ("allvid" in name) or ("allvid" in url):               
                   from resolvers.allvid import resolve
          elif ("exashare" in name) or ("exashare" in url):                
                   from resolvers.exashare import resolve         
          elif ("streamin" in name) or ("streamin" in url): 
                   from resolvers.streamin import resolve
          elif ("vidzi" in name) or ("vidzi" in url): 
                   from resolvers.vidzi import resolve
          elif ("nosvideo" in name) or ("nosvideo" in url): 
                   from resolvers.nosvideo import resolve
          elif ("openload" in name) or ("openload" in url): 
                   from resolvers.openload import resolve         
          elif ("uptobox" in name) or ("uptobox" in url): 
                   from resolvers.uptobox import resolve
          elif ("filepup" in name) or ("filepup" in url): 
                   from resolvers.filepup2 import resolve
          elif ("vidbull" in name) or ("vidbull" in url): 
                   from resolvers.vidbull import resolve
          elif ("vodlocker" in name) or ("vodlocker" in url): 
                   pass#print "In getVidurl vodlockero url 2=", url
                   from resolvers.vodlocker import resolve
          elif ("vidto" in name) or ("vidto" in url): 
                   pass#print "In getVidurl vidto url 2=", url
                   from resolvers.vidto import resolve
          elif ("videomega" in name) or ("videomega" in url): 
                   pass#print "In getVidurl videomega url =", url
                   from resolvers.videomega import resolve
          elif ("youwatch" in name) or ("youwatch" in url): 
                   from resolvers.youwatch import resolve   
          elif ("zstream" in name) or ("zstream" in url): 
                   from resolvers.zstream import resolve
          elif ("vidlox" in name) or ("vidlox" in url):
                   from resolvers.vidlox import resolve
          elif ("estream" in name) or ("estream" in url):
              from urlresolver import resolve
          elif ("thevideo" in name) or ("thevideo" in url):
              from urlresolver import resolve
          elif ("watchers" in name) or ("watchers" in url):
              from urlresolver import resolve
          try:               
                   vidurl = resolve(url)
                   pass#print "In getVidurl vidurl =", vidurl
                   return vidurl
          except:         
                   pass#print "In getVidurl url B=", url
                   return url

    

def getVideos5(name, url):
        pass#print "In getVideos5 name =", name
        pass#print "In getVideos5 url =", url
        urlmain = url
        content = getUrl(url)
        content = content.decode('utf8')
        pass#print "content E =", content
        regexvideo = 'window.location="(.+?)"'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
	url = match[0]
	pass#print "In getVideos5 match =", match
	if "videomega" in url:
	       url = url + "|" + urlmain
	stream_url = getVidurl(name, url)
        pass#print "stream_url =", stream_url
        playVideo(name, stream_url)


def getVideos5X(name1, urlmain):
        url = urlmain + "/videos?p=5"
	content = getUrl(url)
	#pass#print "content B =", content

	regexvideo = 'thumb_container video.*?href="(.*?)" title="(.*?)">'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        ##pass#print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 url = "http://www.deviantclip.com" + url
                 pic = " " 
                 ##pass#print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

                
def playVideo(name, url):
           pass#print "Here in playVideo url =", url
           pic = "DefaultFolder.png"
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}  

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))
pass#print "name =", name
pass#print "url =", url

if not sys.argv[2]:
	ok = showContent()
else:
        if mode == str(1):
		ok = getPage(name, url)
	elif mode == str(2):
		ok = getVideos(name, url)
	elif mode == str(3):
	        ok = getVideos2(name, url)
#		ok = playVideo(name, url)	
	elif mode == str(4):
		ok = getVideos3(name, url)	
	elif mode == str(5):
		ok = getVideos4(name, url)
	elif mode == str(6):
#	        ok = playVideo(name, url)
		ok = getVideos5(name, url)
	elif mode == str(7):
            stream_url = getVidurl(name, url)
            playVideo(name, stream_url)



































































