# -*- coding: utf-8 -*-

import re
from client2 import getUrl, getUrl2


def resolve(url):
#        link = getUrl(url)
 #       stream_url=re.compile('src="(.+?)" allowfullscreen=""></iframe>').findall(link)[0]
               print "In videomega url=", url
               items = url.split("|")
               print "In videomega items=", items
               link = getUrl2(items[0], items[1])
               print "In videomega link  =", link
               vidurl = re.compile('<source src="(.+?)"').findall(link)[0]
               print "In videomega vidurl =", vidurl
               return vidurl
	       

