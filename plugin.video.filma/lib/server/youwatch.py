# -*- coding: UTF-8 -*-
# /*
# *      Copyright (C) 2015 Lubomir Kucera
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */
import re
import util

__author__ = 'Jose Riha/Lubomir Kucera'
__name__ = 'youwatch'


def supports(url):
    return re.search(r'youwatch\.org/embed\-[^\.]+\.html', url) is not None


def resolve(url):
    refererurl = re.search(r'<iframe src="([^"]+)".*', util.request(url), re.I | re.S).group(1)
    try:
        data=[x for x in util.request(refererurl).splitlines() if 'file:' in x and '.mp4' in x][0]
    except:
        return None
    streamurl = re.search(r'.*file:"([^"]+?)".*', data).group(1)
    headers={'Referer': refererurl}
    return [{'url': streamurl, 'headers': headers}]
