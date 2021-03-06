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

import os
from zipfile import ZipFile

import requests
from PyQt5.QtCore import QThread, pyqtSignal


class DownloadThread(QThread):
    download_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def set_vars(self, url, folder_name, chunk_size=128):
        self.url = url
        self.folder_name = folder_name
        self.chunk_size = chunk_size

    def run(self):
        try:
            req = requests.get(self.url, stream=True)
            file_size = req.headers["Content-Length"]

            archive = self.folder_name + "/" + os.path.basename(self.url)

            offset = 0
            with open(archive, "wb") as fileobj:
                for chunk in req.iter_content(chunk_size=self.chunk_size):
                    fileobj.write(chunk)
                    offset = offset + len(chunk)
                    progress = offset / int(file_size) * 100
                    self.download_signal.emit(int(progress))

            if archive.endswith(".zip"):
                try:
                    with ZipFile(archive) as z:
                        z.extractall(self.folder_name)
                    os.remove(archive)
                except:
                    raise Exception("Failed to extract zip archive:", archive)

        except Exception as e:
            print(e)

        finally:
            self.quit()
