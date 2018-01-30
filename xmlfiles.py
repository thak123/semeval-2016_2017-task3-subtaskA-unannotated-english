"""This module provides a facade for accessing unannotated SemEval Task 3, Subtask A datasets."""

from zipfile import ZipFile

import wget

URLS = {
    "QL-unannotated-data-subtaskA.xml.zip": "http://alt.qcri.org/semeval2016/task3/data/uploads/QL-unannotated-data-subtaskA.xml.zip"}

XMLFNAMES = {
    2016 : {
        "unannotated": [("QL-unannotated-data-subtaskA.xml.zip", "QL-unannotated-data-subtaskA.xml")]}}

class XMLFiles():
    def __init__(self, *path):
        obj = XMLFNAMES
        for segment in path:
            obj = obj[segment]
        self.zipfnames, self.xmlfnames = zip(*obj)
        self.zipfiles = []
        self.xmlfiles = []

    def __enter__(self):
        for zipfname, xmlfname in zip(self.zipfnames, self.xmlfnames):
            try:
                zipfile = ZipFile(zipfname)
            except IOError:
                assert wget.download(URLS[zipfname]) == zipfname
                zipfile = ZipFile(zipfname)
                self.zipfiles.append(zipfile)
            xmlfile = zipfile.open(xmlfname, 'r')
            self.xmlfiles.append(xmlfile)
        return self.xmlfiles

    def __exit__(self, type, value, traceback):
        for xmlfile in self.xmlfiles:
            xmlfile.close()
        for zipfile in self.zipfiles:
            zipfile.close()
