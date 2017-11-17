import os
import datetime

def initizilze_transactions():
    transactions = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, r'test.txt')) as f:
        line = f.readline()
        while line:
            t = {}
            for item in line.split():
                t[item] = True
            transactions.append(t)
            line = f.readline()
    return transactions

def initialize_candidates(transactions, min_support):
    candidate_list = []
    candidate_hash = {}
    for t in transactions:
        for i in t:
            if i in candidate_hash:
                candidate_hash[i] += 1
            else:
                candidate_hash[i] = 1
    for k in candidate_hash:
        if candidate_hash[k] > min_support:
            candidate_list.append([k])
    return candidate_list

def calc_all_support(transactions, candidaes):
    supports = [0] * len(candidaes)
    obsolete = []
    for i in range(len(transactions)):
        t = transactions[i]
        relevant = False
        for j in range(len(candidaes)):
            found = True
            for c in candidaes[j]:
                if c not in t:
                    found = False
            if found:
                supports[j] += 1
                relevant = True
        if relevant == False:
            obsolete.append(i)
    obsolete.reverse()
    for i in obsolete:
        del transactions[i]

    return supports

def generate_candidates(filtered_candidates):
    candidates = []
    for i in range(len(filtered_candidates)):
        j = i+1
        while j < len(filtered_candidates):
            temp = list(sorted(set().union(filtered_candidates[i], filtered_candidates[j])))
            if len(temp) == len(filtered_candidates[i]) + 1 and temp not in candidates:
                candidates.append(temp)
            j += 1

    return candidates

time1 = datetime.datetime.now()

transactions = initizilze_transactions()
min_support = len(transactions) / 100
min_confidence = 60/100
next_candidates = initialize_candidates(transactions, min_support)
most_common = []
most_common_supports = {}

while (len(next_candidates) > 0):
    supports = calc_all_support(transactions, next_candidates)

    # filter candidates
    filtered_candidates = []
    for i in range(len(supports)):
        if supports[i] >= min_support:
            filtered_candidates.append(next_candidates[i])
            most_common_supports[str(next_candidates[i])]= supports[i]

    most_common.append(filtered_candidates)
    next_candidates = generate_candidates(filtered_candidates)

for i in range(len(most_common)):
    print("{}: {}".format(i+1, " ".join(str(x) for x in most_common[i])))
#print(most_common_supports)

rules = {}
for k in range(len(most_common) - 1):
    for i in range(len(most_common[k]) - 1):
        j = i + 1
        while j < len(most_common[k]):
            union = set().union(most_common[k][i], most_common[k][j])
            temp = list(sorted(union))
            if temp in most_common[k+1]:
                intersection = set(most_common[k][i]).intersection(most_common[k][j])
                confidence = most_common_supports[str(temp)]/most_common_supports[str(most_common[k][i])]
                if confidence > min_confidence:
                    result = list(set(most_common[k][j]) - intersection)
                    key = "{}=>{}".format(str(most_common[k][i]), str(result))
                    if key not in rules:
                        rules[key] = confidence*100
                confidence = most_common_supports[str(temp)] / most_common_supports[str(most_common[k][j])]
                if confidence > min_confidence:
                    result = list(set(most_common[k][i]) - intersection)
                    key = "{}=>{}".format(str(most_common[k][j]), str(result))
                    if key not in rules:
                        rules[key] = confidence * 100
            j += 1


for k in rules:
    print("{} with {:.2f}%".format(k, rules[k]))

time2 = datetime.datetime.now()
elapsedTime = time2 - time1
print(elapsedTime)
