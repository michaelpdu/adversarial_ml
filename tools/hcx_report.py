import os, sys, re
from logging import *

DECISION_NORMAL = 0
DECISION_FEEDBACK = 1
DECISION_MALICIOUS = 2

class HouseCallXReport:
    """"""

    @staticmethod
    def get_scores(file_path):
        scores = {}
        with open(file_path, 'r') as fh:
            for line in fh.readlines():
                pattern = re.compile(r".*?\[.*?\]\s\[.*\]\s\[.*?\]\s\[(.*?)\]\s\[(.*?)\]\s\[(.*?)\]\sin\s(.*)\s\[")
                m = pattern.match(line)
                if m:
                    data = m.groups()
                    decision = int(data[0])
                    conf_level = int(data[1].strip())
                    file_name = os.path.split(data[3].replace('\\', '/'))[-1]

                # pattern = re.compile(r"([^\[\r\n]+?)\s\[.*?\]\s\[.*\]\s\[(.*?)\]\s\[(.*?)\]\s\[(.*?)\]\s\[(.*?)\]\sin\s(.*)\s\[")
                # m = pattern.match(line)
                # if m:
                #     data = m.groups()
                #     action = data[0]
                #     rule = data[1].strip()
                #     decision = int(data[2])
                #     conf_level = int(data[3].strip())
                #     file_name = os.path.split(data[5].replace('\\', '/'))[-1]


                    # if decision == DECISION_MALICIOUS:
                    #     score = 100 - conf_level
                    # elif decision == DECISION_FEEDBACK:
                    #     score = 100 + conf_level
                    # else:
                    #     score = 200 + conf_level

                    # if decision == DECISION_MALICIOUS:
                    #     score = 0
                    # elif decision == DECISION_FEEDBACK:
                    #     score = 100
                    # else:
                    #     score = 200

                    if decision < DECISION_MALICIOUS:
                        info('>> Found bypassed sample: [{}]'.format(line))

                    if file_name not in scores.keys():
                        scores[file_name] = (decision, conf_level)
        return scores
