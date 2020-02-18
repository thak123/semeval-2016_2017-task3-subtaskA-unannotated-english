from preprocessing import parse
from json import dump
import json
import jsonlines
import io
from collections import Counter





xmlfiles=[
    "/media/gaurish/Angela's Files/projects/semeval-2016_2017-task3-subtaskA-unannotated-english/v3.2/train/SemEval2016-Task3-CQA-QL-train-part1-subtaskA.xml",
    "/media/gaurish/Angela's Files/projects/semeval-2016_2017-task3-subtaskA-unannotated-english/v3.2/train/SemEval2016-Task3-CQA-QL-train-part2-subtaskA.xml",
    "/media/gaurish/Angela's Files/projects/semeval-2016_2017-task3-subtaskA-unannotated-english/v3.2/dev/SemEval2016-Task3-CQA-QL-dev-subtaskA.xml"
]

counter =[]

def write_to_file(data,output_path,mode ="w"):
    
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')

if __name__ == "__main__":
    result = []
    corpus = parse(xmlfiles[0])
    (counter.extend([line["THREAD_SEQUENCE"] for line in corpus]))
    output_path = "train.jsonl"
    write_to_file(corpus,output_path)

    corpus = parse(xmlfiles[1])
    (counter.extend([line["THREAD_SEQUENCE"] for line in corpus]))
    output_path = "train.jsonl"
    write_to_file(corpus,output_path,"a")
    print(Counter(counter))

    corpus = parse(xmlfiles[2])
    (counter.extend([line["THREAD_SEQUENCE"] for line in corpus]))
    output_path = "val.jsonl"
    write_to_file(corpus,output_path)
    print(Counter(counter))

    # # TODO inser test file

