"""
--------------------------------------------------------------------------------
tools/verifier.py
Checks the correctness of the algorithm using the verbose logs against logs retrieved by
http://www.borgelt.net/doc/apriori/apriori.html
Expeected files in logs dir:
<dataset>-v.log - our programs verbose log output
<dataset>.log - apriori program itemset output with -o param
<dataset>_rules.log - apriori program rules output with -o and -tr params
--------------------------------------------------------------------------------
Authors: Elizabeth Gorbonos, Omer Tal, Tianran Wang
--------------------------------------------------------------------------------
"""

import re
import sys
from collections import namedtuple

Rule = namedtuple('Rule', ['lhs', 'rhs', 'confidence'])

def extract_itemset_and_rules(v_log):
    v_itemsets = set()
    v_rules = set()
    itemset_pattern = re.compile(".*Level \d:.*")
    rule_pattern = re.compile(".*(\['[^\[]*\']->\['[^\[]*\']).*confidence=(0.[\d]+).*")
    itemset_pattern = re.compile("")

    with open(v_log) as f:
        first_line = f.readline()
        confidence = re.match(r".*confidence (\d+.\d)%.*", first_line)
        line = f.readline()
        while line:
            if itemset_pattern.match(line):
                m = re.findall(r"\['[^\[]*'\]", line)
                for i in m:
                    v_itemsets.add(i)
            line = f.readline()
            rule = rule_pattern.match(line)
            if rule:
                lhs, rhs = rule.groups()[0].split("->")
                c = format((float(rule.groups()[1].strip())*100), '.1f')
                v_rules.add(Rule(lhs, rhs, c))

    return v_itemsets, v_rules, confidence.groups()[0]

def verify_itemsets(apriori_log, v_itemsets):
    itemsets = set()
    with open(apriori_log) as f:
        line = f.readline()
        while line:
            items = line.split("(")[0]
            l = []
            for item in items.split():
                l.append(item)
            itemsets.add(str(sorted(l)))
            line = f.readline()

        missing =itemsets ^ v_itemsets
        if missing:
            print(missing)
        else:
            print("itemsets correct")

def verify_rules(apriori_log, v_rules, min_confidence):
    rules = set()
    rule_pattern = re.compile("(.+)<-(.+)\(.*, (.+)\)")
    with open(apriori_log) as f:
        line = f.readline()
        while line:
            match = rule_pattern.match(line)
            rhs = [match.groups()[0].strip()]
            lhs = []
            for i in match.groups()[1].split():
                lhs.append(i.strip())

            c = format(float(match.groups()[2]), '.1f')
            rule = Rule(str(sorted(lhs)), str(rhs), c)
            if rule in rules:
                print(rule)
            else:
                rules.add(rule)
            line = f.readline()


    missing = rules ^ v_rules

    # the apriori program doesn't generate rules in which the rhs has more than 1 element
    # we do - so don't count that as a miss
    # Also, we generate rules with confidence greater than the given parameter,
    # while the program includes rule with confidence greater or equal - so we will ignore those
    really_missing = []
    if missing:
        for m in missing:
            rhs = eval(m.rhs)
            if len(rhs) <= 1 and m.confidence != min_confidence:
                really_missing.append(m)

    if len(really_missing) > 0:
        print(really_missing)
    else:
        print("rules correct")

def verify(dataset):
    v_log = r"logs\{}-v.log".format(dataset)
    apriori_log = r"logs\{}.log".format(dataset)
    apriori_rules_log = r"logs\{}_rules.log".format(dataset)
    v_itemsets, v_rules, min_confidence = extract_itemset_and_rules(v_log)
    verify_itemsets(apriori_log, v_itemsets)
    verify_rules(apriori_rules_log, v_rules, min_confidence)

if __name__ == "__main__":
    verify(sys.argv[1])
