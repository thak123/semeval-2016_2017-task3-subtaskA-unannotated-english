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
        # relquestion["RelQSubject"] = thread.find("RelQuestion/RelQSubject").text or ""
        relquestion["RelQBody"] = thread.find(
            "RelQuestion/RelQBody").text or ""

        relthread = {
            "THREAD_SEQUENCE": thread.attrib["THREAD_SEQUENCE"],
            "RelQuestion": relquestion["RelQBody"],
        }

        relcomments = []
        for i, relcomment in enumerate(thread.findall("RelComment")):
            relcomments.append({})
            for attrib in ("RELC_ID", "RELC_DATE", "RELC_USERID", "RELC_USERNAME", "RELC_RELEVANCE2RELQ"):
                if attrib == "RELC_RELEVANCE2RELQ":
                    relcomments[i][attrib] = relcomment.attrib[attrib]
            relcomments[i]["RelCText"] = relcomment.find("RelCText").text or ""
            relthread.update(
                {"comment{}".format(i): relcomments[i]["RelCText"]})
        relthread.update({"RelScore": [i["RELC_RELEVANCE2RELQ"] for i in relcomments]})

        # print(thread.attrib["THREAD_SEQUENCE"])
        threads.append(relthread)
    return threads
