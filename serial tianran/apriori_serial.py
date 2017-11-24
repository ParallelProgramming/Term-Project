from collections import defaultdict
from itertools import chain, combinations
from time import time

min_support = 0.025
min_confidence = 0.6
transaction_list = list()
m = 0
global_count_dict = defaultdict(int)


def load_file(file_name):
    file = open(file_name, 'U')
    for line in file:
        line = line.strip().rstrip(',')
        yield frozenset(line.split(','))


def get_large_set(candidate_set):
    global global_count_dict
    large_set = set()
    local_count_dict = defaultdict(int)
    for item in candidate_set:
        for transaction in transaction_list:
            if item.issubset(transaction):
                local_count_dict[item] += 1
                global_count_dict[item] += 1

    for item, count in local_count_dict.items():
        support = float(count) / m
        # print('\nsupport: %f' % support)
        if support > min_support:
            large_set.add(item)

    return large_set


def get_new_candidate_set(large_set, k):
    return set([i.union(j) for i in large_set for j in large_set if len(i.union(j)) == k])


def get_subset_list(item_set):
    return chain(*[combinations(item_set, i + 1) for i, a in enumerate(item_set)])


def get_support(item_set):
    return float(global_count_dict[item_set]) / m


def apriori(data):
    global global_count_dict
    candidate_set = set()
    for transaction in data:
        transaction_list.append(transaction)
        for item in transaction:
            item = frozenset([item])
            candidate_set.add(item)
            global_count_dict[item] += 1
    global m
    m = len(transaction_list)
    # print('\n1_candidate_set:')
    # print(candidate_set)

    large_set = set()
    for item, count in global_count_dict.items():
        support = float(count) / m
        # print('\nsupport: %f' % support)
        if support > min_support:
            large_set.add(item)
    print('\n1_large_set:')
    print(large_set)

    large_set_dict = dict()
    k = 1
    while len(large_set) != 0:
        large_set_dict[k] = large_set
        candidate_set = get_new_candidate_set(large_set, k + 1)
        # print('\n%d_candidate_set:' % (k + 1))
        # print(candidate_set)
        large_set = get_large_set(candidate_set)
        print('\n%d_large_set:' % (k + 1))
        print(large_set)
        k += 1

    rules = []
    for _, large_set in large_set_dict.items():
        for large in large_set:
            super_list = get_subset_list(large)
            for super in super_list:
                super = frozenset(super)
                lhs_list = get_subset_list(super)
                for lhs in lhs_list:
                    lhs = frozenset(lhs)
                    rhs = super.difference(lhs)
                    if len(rhs) > 0:
                        confidence = get_support(super) / get_support(lhs)
                        # print('\n\nconfidence: %f' % confidence)
                        if confidence > min_confidence:
                            lift = confidence / get_support(rhs)
                            rules.append({'lhs': set(lhs), 'rhs': set(rhs), 'confidence': confidence, 'lift': lift})
    print('\nrules:')
    for rule in rules:
        print(rule)


if __name__ == '__main__':
    start = time()
    data = load_file('retail.csv')
    apriori(data)
    stop = time()
    print('\nruning time: %d s' % (stop - start))
