#!/usr/bin/python
# -*- coding: latin-1 -*-

import sys, xbmc
import xbmc, xbmcplugin
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
from urlparse import parse_qs, urlparse
from urllib import unquote_plus
from urlresolver import resolve
import HTMLParser
# import rpdb2
# rpdb2.start_embedded_debugger('pw')

hostDict = ['allvid', 'exashare', 'filepup', 'filepup2', 'nosvideo', 'nowvideo', 'openload', 'vidlockers',
            'streamcloud', 'streamin', 'vidspot', 'vidto', 'xvidstage', 'nosvideo', 'nowvideo', 'vidbull', 'vodlocker',
            'vidto', 'youwatch', 'videomega', 'estream', 'thevideo', 'watchers', 'dailymotion']

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.filma24-al"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
    cmd = "mkdir -p " + dataPath
    system(cmd)


# Host = "http://www.filma24-al.com/movie-genre/aventure/"
def getUrl(url, data=""):
    pass  # print "Here in getUrl url =", url
    req = urllib2.Request(url, data)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def showContent():
    names = []
    urls = []
    names.append("Search for movies with Albanian Subs")
    urls.append("Kerko")
    names.append("Filma 24 TV - Filmat e fundit")
    urls.append("http://www.filma24.tv/?sort=new")
    names.append("Filma 24 HD")
    urls.append("http://www.filma24hd.com/")
    names.append("Filma On")
    urls.append("http://www.filmaon.com/filma/")
    names.append("Alb Film - Filmat e fundit")
    urls.append("http://www.albfilm.com/filma/kategoria/te-fundit")
    names.append("Seriale me titra Shqip")
    urls.append("Providers")

    i = 0
    for name in names:
        url = urls[i]
        i = i + 1
        pic = " "
        if(url == "Kerko"):
            addDirectoryItem("Search", {"name": "Search", "url": url, "mode": 11}, pic)
        elif(url == "Providers"):
            addDirectoryItem("Seriale", {"name": "Seriale", "url": url, "mode": 12}, pic)
        else:
            addDirectoryItem(name, {"name": name, "url": url, "mode": 1}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def getPage(name, url):
    pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # http://www.filma24.tv/aksion/page/2/
    for page in pages:
        url1 = url + "/page/" + str(page) + "/"
        name = "Page " + str(page)
        pic = " "
        if ("albfilm" in url):
            url1 = "http://188.166.2.77/api/movies_list.php?page=" + str(
                page) + "&lengthperpage=12&show=latest&website=true"
        if ("filma24.tv" in url):
            url1 = urlparse(url).scheme +"://"+ urlparse(url).netloc +"/page/"+ str(
                page) + "/?"+ urlparse(url).query
        addDirectoryItem(name, {"name": name, "url": url1, "mode": 2}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def ultimate_search():
    value = get_numeric_dialog()
    providers_search = ['http://www.albfilm.com/filma/kategoria/?q=', 'http://www.filma24hd.com/search/','http://www.filmaon.com/filma/?s=','http://www.filma24.tv/wp-admin/admin-ajax.php']
    for i in providers_search:
        match = search_providers(i,value)
        for pic, url, name in match:
            addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def get_numeric_dialog(default="", heading="", dlg_type=3):
    """ shows a numeric dialog and returns a value
        - 0 : ShowAndGetNumber		(default format: #)
        - 1 : ShowAndGetDate			(default format: DD/MM/YYYY)
        - 2 : ShowAndGetTime			(default format: HH:MM)
        - 3 : ShowAndGetIPAddress	(default format: #.#.#.#)
    """
    dialog = xbmcgui.Dialog()
    value = dialog.input('Enter the name of the movie', type=xbmcgui.INPUT_ALPHANUM)
    value = urllib.quote_plus(value)
    return value

def search_providers(url, value):
    if not ("filma24.tv" in url):
        content = getUrl(url + value)
    if ("filma24.tv" in url):
        values = {'action': 'load_search_results',
                  'query': value }
        values = urllib.urlencode(values)
        #url = urllib.unquote_plus(url)
        content = getUrl(url,values)
        regexvideo = '(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
    if ("albfilm" in url):
        regexvideo = 'url\((http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.jpg)\)'
    if ("filma24hd" in url):
        regexvideo = '<h2><a href="(.*)"\stitle=".*">'
    if("filmaon.com" in url):
        regexvideo = '<h2><a href="(.*)"\stitle=".*</a></h2>'
    match = re.compile(regexvideo).findall(content)
    url_x = []
    # print match
    for m in match:
        if("albfilm" in url):
            m_x = m.split("/")[5].replace(".jpg", "").replace("_", "-")
            m_y = "Albfilm | " + m_x.replace("-", " ").title()
            if (value in m_y.lower()):
                url_x.append((m, "http://albfilm.com/filma/" + m_x, m_y))
        if("filma24hd" in url):
            m_x = m.split("/")[3]
            m_y = "Filma 24 HD | " + m_x.replace("-", " ").title()
            url_x.append(('', m, m_y))
        if ("filmaon" in url):
            m_x = m.split("/")[4]
            m_y = "FilmaOn | " + m_x.replace("-", " ").title()
            url_x.append(('', m, m_y))
        if ("filma24.tv" in url):
            m_x = m.split("/")[3]
            m_y = "Filma 24 TV | " +m_x.replace("-", " ").title()
            url_x.append(('', m, m_y))
    match = url_x
    return match
    #for pic, url, name in match:
     #   addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
    #xbmcplugin.endOfDirectory(thisPlugin)


def getVideos(name1, urlmain):
    url = urlmain
    content = getUrl(url)
    pass  # print "content A =", content
    if ("http://www.filma24.tv" in urlmain):
        regexvideo = 'div class="movie-thumb".*?background-image:url\((.*?)\).*?<a href="(.*?)".*?<h4>(.*?)<'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
    elif ("http://www.filma24hd.com" in urlmain):
        regexvideo = '<img src="(.*.jpg)"\s.*\s+</a>\s+<h2>\s+<a href="(.*)"\stitle="(.*)"'
        match = re.compile(regexvideo).findall(content)
    elif ("http://www.filmaon.com" in urlmain):
        regexvideo = '<img src="(.*)"\salt.*\s+</a>\s+<h2>\s+<a href="(.*)" title="(.*)">'
        match = re.compile(regexvideo).findall(content)
    elif ("http://188.166.2.77" in urlmain):
        regexvideo = 'url\((http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.jpg)\)'
        match = re.compile(regexvideo).findall(content)
        url_x = []
        # print match
        for m in match:
            m_x = m.split("/")[5].replace(".jpg", "").replace("_", "-")
            m_y = m_x.replace("-", " ").title()
            url_x.append((m, "http://albfilm.com/filma/" + m_x, m_y))
        match = url_x
    pass  # print "match =", match
    for pic, url, name in match:
        if ("http://www.filma24.tv" in urlmain):
            name = HTMLParser.HTMLParser().unescape(name).encode("utf-8")
            addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
        elif ("http://www.filma24hd.com" in urlmain):
            name = HTMLParser.HTMLParser().unescape(name).encode("utf-8")
            addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
        elif ("http://www.filmaon.com" in urlmain):
            addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
        elif ("http://188.166.2.77" in urlmain):
            name = HTMLParser.HTMLParser().unescape(name).encode("utf-8")
            addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)

        #	name = "More videos"
        #	addDirectoryItem(name, {"name":name, "url":urlmain, "mode":3}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def getVideos2(name1, urlmain):
    url = urlmain + "&paged=2"
    content = getUrl(url)
    pass  # print "content B =", content

    regexvideo = 'div class="boxim.*?a href="(.*?)".*?Boxoffice\/timthumb.*?src=(.*?)\&amp.*?div class="btitle.*?title=".*?>(.*?)<'
    match = re.compile(regexvideo, re.DOTALL).findall(content)
    pass  # print "match =", match
    for url, pic, name in match:
        ##pass#print "Here in getVideos url =", url
        addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
    name = "More videos"
    addDirectoryItem(name, {"name": name, "url": urlmain, "mode": 4}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def getVideos3(name1, urlmain):
    url = urlmain + "&paged=3"
    content = getUrl(url)
    pass  # print "content B1 =", content

    regexvideo = 'div class="boxim.*?a href="(.*?)".*?Boxoffice\/timthumb.*?src=(.*?)\&amp.*?div class="btitle.*?title=".*?>(.*?)<'
    match = re.compile(regexvideo, re.DOTALL).findall(content)
    pass  # print "match =", match
    for url, pic, name in match:
        ##pass#print "Here in getVideos url =", url
        addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def getVideos4(name, url):
    pass  # print "In getVideos4 url A=", url
    content = getUrl(url)
    pass  # print "content C =", content
    if ("http://www.filma24.tv" in url):
        n1 = content.find('"watch-links"', 0)
        n2 = content.find('!-- End Downloads Links -->', n1)
        content = content[n1:n2]
        pass  # print "content B=", content
        regexvideo = 'a href="(.+?)".*?<li class="(.+?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        mode_one = 6
    elif ("http://www.filma24hd.com" in url):
        regexvideo = 'shape="poly" href="(htt\w+://(.*)\.\w+\/.*)"\starget'
        match = re.compile(regexvideo).findall(content)
        mode_one = 7
    elif ("http://www.filmaon.com" in url):
        regexvideo = '(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
        match = re.compile(regexvideo).findall(content)
        matchi = []
        for m in match:
            # print m
            for k in hostDict:
                # print k
                if k in urlparse(m).netloc:
                    matchi.append((m, k))
        match = matchi
        mode_one = 7
    elif ("http://albfilm.com" in url):
        regexvideo = '(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
        match = re.compile(regexvideo).findall(content)
        matchi = []
        for m in match:
            for k in hostDict:
                if k in urlparse(m).netloc:
                    matchi.append((m, k))
        match = matchi
        mode_one = 7
    pass  # print "match B=", match
    for url, name in match:
        if not name.lower() in hostDict:
            continue
        pic = " "
        pass  # print "name B=", name
        pass  # print "url B=", url
        addDirectoryItem(name, {"name": name, "url": url, "mode": mode_one}, pic)

    xbmcplugin.endOfDirectory(thisPlugin)


def getVidurl(name, url):
    name = name.lower()
    try:
        vidurl = resolve(url)
        return vidurl
    except:
        return url

def getVideos5(name, url):
    pass  # print "In getVideos5 name =", name
    pass  # print "In getVideos5 url =", url
    urlmain = url
    content = getUrl(url)
    content = content.decode('utf8')
    pass  # print "content E =", content
    regexvideo = 'window.location="(.+?)"'
    match = re.compile(regexvideo, re.DOTALL).findall(content)
    url = match[0]
    pass  # print "In getVideos5 match =", match
    #if "videomega" in url:
        #url = url + "|" + urlmain
    stream_url = getVidurl(name, url)
    pass  # print "stream_url =", stream_url
    playVideo(name, stream_url)


# def getVideos5X(name1, urlmain):
#     url = urlmain + "/videos?p=5"
#     content = getUrl(url)
#     # pass#print "content B =", content
#
#     regexvideo = 'thumb_container video.*?href="(.*?)" title="(.*?)">'
#     match = re.compile(regexvideo, re.DOTALL).findall(content)
#     ##pass#print "match =", match
#     for url, name in match:
#         name = name.replace('"', '')
#         url = "http://www.deviantclip.com" + url
#         pic = " "
#         ##pass#print "Here in getVideos url =", url
#         addDirectoryItem(name, {"name": name, "url": url, "mode": 3}, pic)
#     xbmcplugin.endOfDirectory(thisPlugin)


def playVideo(name, url):
    pass  # print "Here in playVideo url =", url
    pic = "DefaultFolder.png"
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
    player = xbmc.Player()
    player.play(url, li)


std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
}


def addDirectoryItem(name, parameters={}, pic=""):
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
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

def parso(regex, url):
    return re.compile(regex).findall(getUrl(url))

def kerkoserialet():
    content = getUrl("http://tvseriale.com/")
    categories_regex = '<li class="(.*)'
    match = re.compile(categories_regex).findall(content)
    categories = match[0]
    links_regex = 'href="([/\w:\.-]+)"'
    links = re.compile(links_regex).findall(categories)
    pic = ''
    for i in links:
        names = i.split('/')[4].replace('-',' ').title()
        if(not 'Seriale' in names and not 'Uncategorized' in names and not 'Infos'in names):
            addDirectoryItem(names, {"name": names, "url": i, "mode": 13}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def listo_serialet(url):
    pic = ''
    regexi = '<h1 class="archiveTitle"><a href="(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" rel="bookmark" title="(.*)"'
    match = parso(regexi, url)
    #match = sorted(list(set([x for x in match if not url == x and not 'feed' in x and 'tvseriale' in x  ])))
    for urli, namei in sorted(match):
        namei = namei.decode('utf-8').strip()
        namei = HTMLParser.HTMLParser().unescape(namei).encode('utf-8')
        addDirectoryItem(namei, {"name": namei, "url": urli, "mode": 14}, pic)
    try:
        matchi = parso('(class="navigation">\s.*\s+</div><!-- /innerLeft -->)', url)[0]
        regex = '(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)" >([&\;\w\s]+)</a>'
        matchi = re.compile(regex).findall(matchi)
        for url, name in matchi:
            name = HTMLParser.HTMLParser().unescape(name).encode("utf-8")
            addDirectoryItem(name, {"name": name, "url": url, "mode": 13}, pic)
    except:
        pass
    xbmcplugin.endOfDirectory(thisPlugin)

def parso_source(url):
    pic = ''
    i = parso('((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)', url)
    for x in i:
        for k in hostDict:
            if k in urlparse(x).netloc:
                    addDirectoryItem(x, {"name": x, "url": x, "mode": 7}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

params = parameters_string_to_dict(sys.argv[2])
name = str(params.get("name", ""))
url = str(params.get("url", ""))
url = urllib.unquote(url)
mode = str(params.get("mode", ""))
pass  # print "name =", name
pass  # print "url =", url

if not sys.argv[2]:
    ok = showContent()
else:
    if mode == str(1):
        ok = getPage(name, url)
    elif mode == str(2):
        ok = getVideos(name, url)
    elif mode == str(3):
        ok = getVideos2(name, url)
    elif mode == str(4):
        ok = getVideos3(name, url)
    elif mode == str(5):
        ok = getVideos4(name, url)
    elif mode == str(6):
        ok = getVideos5(name, url)
    elif mode == str(7):
        stream_url = getVidurl(name, url)
        playVideo(name, stream_url)
    elif mode == str(10):
        value_key = get_numeric_dialog("1", "Search for movies", 3)
        match = search_providers(url,value_key)
        for pic, url, name in match:
            addDirectoryItem(name, {"name": name, "url": url, "mode": 5}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
    elif mode == str(11):
        ok = ultimate_search()
    elif mode == str(12):
        kerkoserialet()
    elif mode == str(13):
        listo_serialet(url)
    elif mode == str(14):
        parso_source(url)
