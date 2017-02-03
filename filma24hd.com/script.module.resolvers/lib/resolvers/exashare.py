# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import client2


def resolve(url):
#    try:
        """
        pass#print "In exashare url =", url
        url = url.replace('/embed-', '/')
        pass#print "In exashare url 2=", url
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        pass#print "In exashare url 3=", url
        url = 'http://dowed.info/embed-%s-800x500.html' % url
        pass#print "In exashare url 4=", url
        result = client.request(url)
        pass#print "In exashare result =", result
        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        pass#print "In exashare url 5 =", url
        return url
        """
        pass#print "In exashare url =", url
#        url = url.replace('/embed-', '/')
        pass#print "In exashare url 2   =", url
        url = re.compile('embed-(.*?)-').findall(url)[0]
        pass#print "In exashare url 3=", url
        url = 'http://dowed.info/embed-%s-800x500.html' % url
        pass#print "In exashare url 4=", url
        result = client2.getUrl2(url, url)
        pass#print "In exashare result =", result
        url = re.compile('<iframe.*?src="(.*?)"').findall(result)[0]
        pass#print "In exashare url 5 =", url
        result = client2.getUrl2(url, url)
        pass#print "In exashare result 2=", result
        n1 = result.find(".mp4", 0)
        n2 = result.rfind("http", 0, n1)
        url = result[n2:(n1+3)] 
        pass#print "In exashare url 5 =", url
        return url
        
        
        
        
        
        
#    except:
#        return

