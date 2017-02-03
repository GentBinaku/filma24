# -*- coding: utf-8 -*-


import re
import client


def resolve(url):
               pass#print "Here in allvid url=", url
               result = client.request(url)
               pass#print "Here in allvid result =", result
               s = '<img src="(.*?)/i/'
               match=re.compile(s).findall(result);
               vip = match[0]
               regexkey = '\|mp4\|(.*?)\|'
               match1=re.compile(regexkey).findall(result);
               key = match1[0]
               vurl = vip + "/" + key + "/v.mp4"
               return vurl
               