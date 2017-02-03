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
import client


def resolve(url):
#    try:
        url1 = re.compile('//.+?/.+?/([\w]+)').findall(url)[0]
        print "url1 =", url1
        url = 'http://www.filepup.net/play/%s' % url1

        result = client.request(url)
        print "result =", result
        url = re.compile('"video/mp4".*?"(.*?)"').findall(result)[0]
        print "url =", url
#        url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
        return url
#    except:
#        return

