# -*- coding: utf-8 -*-

import re
import urllib2
import jsunpack
#from client2 import getUrl, getUrl2

def getUrl2(url, referer):
        pass#print "Here in videomega client2 getUrl url =", url
	req = urllib2.Request(url)
#	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25')

        req.add_header('Referer', referer)
	response = urllib2.urlopen(req)
	pass#print "Here in videomega client2 getUrl response=", response
	link=response.read()
	pass#print "Here in videomega client2 getUrl link=", link
	response.close()
	return link	
	
def resolve(url):
#        link = getUrl(url)
 #       stream_url=re.compile('src="(.+?)" allowfullscreen=""></iframe>').findall(link)[0]
               pass#print "In videomega url=", url
               items = url.split("|")
               pass#print "In videomega items=", items
               html = getUrl2(items[0], items[1])
               pass#print "In videomega html  =", html
#               if jsunpack.detect(html):
               js_data = jsunpack.unpack(html)
               pass#print "Here in videomega-py js_data =", js_data
               match = re.search('"src"\s*,\s*"([^"]+)', js_data)
               pass#print "Here in videomega-py match =", match
               if match:
                               return match.group(1) 
               
               else:
                      pass#print "No video"
                      return "No video"
