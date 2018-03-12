import os, sys, re
from logging import *

DECISION_NORMAL = 0
DECISION_FEEDBACK = 1
DECISION_MALICIOUS = 2

class HouseCallXReport:
    """"""

    def __init__(self, file_path):
        self.scores = {}
        with open(file_path, 'r') as fh:
            for line in fh.readlines():
                pattern = re.compile(r".*?\[.*?\]\s\[.*\]\s\[.*?\]\s\[(.*?)\]\s\[(.*?)\]\s\[(.*?)\]\sin\s(.*)\s\[")
                m = pattern.match(line)
                if m:
                    data = m.groups()
                    decision = int(data[0])
                    conf_level = int(data[1].strip())
                    file_name = os.path.split(data[3].replace('\\', '/'))[-1]

                    # if decision == DECISION_MALICIOUS:
                    #     score = 100 - conf_level
                    # elif decision == DECISION_FEEDBACK:
                    #     score = 100 + conf_level
                    # else:
                    #     score = 200 + conf_level

                    if decision == DECISION_MALICIOUS:
                        score = 0
                    elif decision == DECISION_FEEDBACK:
                        score = 100
                    else:
                        score = 200

                    self.scores[file_name] = score
                    msg = 'Score: {}, Decision: {}, Confidence Level: {}, File Name: {}'.format(score, decision, conf_level, file_name)
                    info(msg)
                    print(msg)

    def get_scores(self):
        return self.scores


if __name__ == '__main__':
    report = HouseCallXReport(sys.argv[1])
    print(report.get_scores())