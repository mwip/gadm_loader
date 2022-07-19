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

import re
import urllib.error
import urllib.parse
import urllib.request


def parse_gadm_countries():
    url = "https://gadm.org/download_country.html"
    try:
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read()
    except urllib.error.HTTPError as e:
        print(e.msg, ":", url)
    except urllib.error.URLError as e:
        print(e.reason, ":", url)

    # from the http content, we want to find all countries listed inside <option value> tags
    values = re.findall(r"<option value=\"[\w\s]*\">[\w|\s]+</option>", str(content))

    # extract country codes and names from the values
    codes = [re.search(r"[A-Z]{3}", str(x)).group() for x in list(values)]
    names = [re.search(r"(?<=>)[A-Za-z ]+(?=<)", str(x)).group() for x in list(values)]

    # zip country codes and values into a dictionary
    out = dict(zip(names, codes))
    # add the world
    out["Entire World"] = "WORLD"

    return out


# construct url
def get_url(country_code: str, gadm_version_no_sep: int) -> str:
    if country_code == "WORLD":
        url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_{gadm_version_no_sep}0-gpkg.zip"
    else:
        url = (
            f"https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm{gadm_version_no_sep}_"
            f"{country_code}.gpkg"
        )
    return url
