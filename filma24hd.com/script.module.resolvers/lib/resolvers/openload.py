# -*- coding: utf-8 -*-


import re
import client
import urllib, urllib2
Request = urllib2.Request
urlopen = urllib2.urlopen
#cj = cookielib.LWPCookieJar()

openloadhdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}           

def getHtml(url, referer, hdr=None):
    if not hdr:
        req = Request(url, '', headers)
    else:
        req = Request(url, '', hdr)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    response = urlopen(req, timeout=60)
    data = response.read()
#    cj.save(cookiePath)
    response.close()
    return data

def resolve(url):
        pass#print "In openload-py url =", url
        url = url.split("|")[0]
        pass#print "In openload-py url B=", url       
#    try:
        n1 = url.find("/f/", 0)
        vid = url[(n1+3):]
        pass#print "In openload-py vid =", vid 
        openloadurl = "https://openload.co/embed/" + vid + "/"
        pass#print "In openload-py openloadurl=", openloadurl  
        openloadsrc = getHtml(openloadurl, '', openloadhdr)
        pass#print "In openload-py openloadsrc=", openloadsrc
        videourl = decodeOpenLoad(openloadsrc)
        pass#print "In openload-py videourl B=", videourl

        return videourl
#    except:
#        return

def decodeOpenLoad(html):

    aastring = re.search(r"<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)</script", html, re.DOTALL | re.IGNORECASE).group(1)
    
    # decodeOpenLoad made by mortael, please leave this line for proper credit :)
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))","8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))","7")
    aastring = aastring.replace("((o^_^o) +(o^_^o))","6")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))","5")
    aastring = aastring.replace("(ﾟｰﾟ)","4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))","2")
    aastring = aastring.replace("(o^_^o)","3")
    aastring = aastring.replace("(ﾟΘﾟ)","1")
    aastring = aastring.replace("(+!+[])","1")
    aastring = aastring.replace("(c^_^o)","0")
    aastring = aastring.replace("(0+0)","0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]","\\")
    aastring = aastring.replace("(3 +3 +0)","6")
    aastring = aastring.replace("(3 - 1 +0)","2")
    aastring = aastring.replace("(!+[]+!+[])","2")
    aastring = aastring.replace("(-~-~2)","4")
    aastring = aastring.replace("(-~-~1)","3")
    
    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+"+ decodestring
    decodestring = decodestring.replace("+","")
    decodestring = decodestring.replace(" ","")
    
    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/","/")

    videourl = re.search(r"vr\s?=\s?\"|'([^\"']+)", decodestring, re.DOTALL | re.IGNORECASE).group(1)
    return videourl

def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')
