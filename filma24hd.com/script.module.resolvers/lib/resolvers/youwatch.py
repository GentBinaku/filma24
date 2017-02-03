# -*- coding: utf-8 -*-

import re
import client
from client2 import getUrl, getUrl2


def resolve(url):
               pass#print "In youwatch url =", url
               content2 = getUrl(url)
               pass#print "In getVideos4 youwatch content2 =", content2
               regexvideo = 'src="(.*?)"'
	       match = re.compile(regexvideo,re.DOTALL).findall(content2)
	       url = match[0]
	       pass#print "In youwatch url 2=", url
	       url = url.replace("\n", "")
	       pass#print "In youwatch url 3=", url
	       content3 = getUrl2(url, url)
               pass#print "In getVideos4 youwatch content3 =", content3
	       regexvideo = 'file:"(.*?)"'
	       match = re.compile(regexvideo,re.DOTALL).findall(content3)
	       
	       vidurl = match[0] 
               pass#print "vidurl =", vidurl 
               return vidurl
	       

