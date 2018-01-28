"""This module produces SemEval Task 3, Subtask B datasets in JSON."""

from itertools import chain
from json import dump

from preprocessing import parse
from xmlfiles import XMLFiles

if __name__ == "__main__":
    result = []
    with XMLFiles(2016, "unannotated") as xmlfiles:
        assert len(xmlfiles) == 1
        corpus = parse(xmlfiles[0])
    with open("result.json", "w") as jsonfile:
        dump(corpus, jsonfile, sort_keys=True, indent=4)
