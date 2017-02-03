import re
import client

import urllib, urllib2
from urllib2 import Request, URLError, urlopen
def getUrl(url):
    pass  # print "Here in getUrl url =", url
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link
def resolve(url):
    try:
        print "In vidto url =", url
        result = getUrl(url)
        url = re.compile('(https://.*master.*\.m3u8)').findall(result)[0]
        print "In vidto url 2=", url
        return url
    except:
        return
