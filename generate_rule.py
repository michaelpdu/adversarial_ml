import json
import yara
import os

class RuleGenerator:

    def __init__(self,baseline_name):
        self.rule_file = 'bhv_rule_%s' % (baseline_name)
        self.rule_name = baseline_name
        self.rule_number = 0

    def generateRuleFromReport(self, report_map):
        head = 'rule %s' % (self.rule_name) + """\n{\n    strings:\n"""
        tail = """\n    condition:\n        all of them\n}"""
        rules = ''
        signatures = report_map['signatures']
        for sig in signatures:
            description = sig['description']
            singleRule = '        $' + chr(self.rule_number + ord('a')) + ' = ' + description
            rules = rules + '%s\n' % (singleRule)
            self.rule_number += 1
        rule_dir = os.getcwd() + '/baseline_rules'
        if not os.path.exists(rule_dir):
            os.makedirs(rule_dir)
        with open(os.path.join(rule_dir, self.rule_file), 'w+') as f:
            f.write(head)
            f.write(rules)
            f.write(tail)
        


if __name__ == '__main__':
    log_path = r'cuckoo_log'
    for root, dirs, files in os.walk(log_path):
        for name in files:
            if 'task.json' == name:
                task_file = os.path.join(root, name)
                report_file = os.path.join(root, 'reports/report.json')

                with open(report_file, 'r', encoding='utf-8') as fr:
                    report_map = json.load(fr)

                with open(task_file, 'r', encoding='utf-8') as ft: 
                    task_map = json.load(ft)
                    target = task_map['target']
                    dir_path, baseline_name = os.path.split(target)
    
                yara_rule_gen = RuleGenerator(baseline_name)
                yara_rule_gen.generateRuleFromReport(report_map)

