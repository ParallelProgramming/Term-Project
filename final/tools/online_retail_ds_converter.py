import os

transactions = {}

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, r'Online Retail.csv')) as f:
    line = f.readline()
    while line:
        t_id, i_id = line.split(",")
        if t_id not in transactions:
            transactions[t_id] = []
        transactions[t_id].append(i_id.strip())
        line = f.readline()

with open(os.path.join(dir_path, r'ds2.txt'), 'w') as f:
    for t in transactions:
        f.write(' '.join(str(x) for x in sorted(transactions[t])))
        f.write('\n')
