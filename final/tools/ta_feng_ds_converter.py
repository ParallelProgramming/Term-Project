import os

transactions = {}

dir_path = os.path.dirname(os.path.realpath(__file__))
files = ['D01', 'D02', 'D11', 'D12']
for f_name in files:
    with open(os.path.join(dir_path, r'ta-feng' ,f_name), encoding="utf8") as f:
        line = f.readline()
        while line:
            props = line.split(";")
            t_id = (props[0] + props[1]).strip()
            i_id = props[7]
            if t_id not in transactions:
                transactions[t_id] = []
            transactions[t_id].append(i_id.strip())
            line = f.readline()

with open(os.path.join(dir_path, r'ds3.txt'), 'w') as f:
    for t in transactions:
        f.write(' '.join(str(x) for x in sorted(transactions[t])))
        f.write('\n')