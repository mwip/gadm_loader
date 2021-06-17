# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GADMloaderDialog
                                 A QGIS plugin
 Download GADM data.
                             -------------------
        begin                : 2021-06-15
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Matthias Weigand
        email                : matthias.weigand@protonmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import urllib.request, urllib.error, urllib.parse
import re

def parse_gadm_countries():
    url = 'https://gadm.org/download_country_v3.html'
    try:
        response = urllib.request.urlopen(url, timeout = 30)
        content = response.read()
    except urllib.error.HTTPError as e:
        print(e.msg, ":", url)
    except urllib.error.URLError as e:
        print(e.reason, ":", url)
        
    # from the http content, we want to find all countries listed inside <option value> tags
    values = re.findall(r"<option value=\"\w*\">\w+</option>", str(content))
    
    # extract country codes and names from the values
    codes = [re.search(r"[A-Z]{3}", str(x)).group() for x in list(values)]
    names = [re.search(r"(?<=>)[A-Za-z ]+(?=<)", str(x)).group() for x in list(values)]
    
    # zip country codes and values into a dictionary
    out = dict(zip(codes, names))
    # add the world
    out['WRL'] = "Entire World"
    
    return out
