"""This module provides preprocessing routines for unannotated SemEval Task 3, Subtask A datasets."""

from lxml import etree
from lxml.etree import XML, XMLSchema, XMLParser

def parse(xmlfile):
    tree = etree.parse(xmlfile)
    threads = []
    for thread in tree.findall("Thread"):
        relquestion = {}
        for attrib in ("RELQ_ID", "RELQ_CATEGORY", "RELQ_DATE", "RELQ_USERID", "RELQ_USERNAME"):
            relquestion[attrib] = thread.find("RelQuestion").attrib[attrib]
        relquestion["RelQSubject"] = thread.find("RelQuestion/RelQSubject").text or ""
        relquestion["RelQBody"] = thread.find("RelQuestion/RelQBody").text or ""

        relcomments = []
        for i, relcomment in enumerate(thread.findall("RelComment")):
            relcomments.append({})
            for attrib in ("RELC_ID", "RELC_DATE", "RELC_USERID", "RELC_USERNAME"):
                relcomments[i][attrib] = relcomment.attrib[attrib]
            relcomments[i]["RelCText"] = relcomment.find("RelCText").text or ""

        threads.append({
            "THREAD_SEQUENCE": thread.attrib["THREAD_SEQUENCE"],
            "RelQuestion": relquestion,
            "RelComments": relcomments})
    return threads
