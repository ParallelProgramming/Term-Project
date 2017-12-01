import os

transactions = []
items = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, r'supermarket.arff')) as f:
    f.readline() #@relation supermarket
    line = f.readline()
    # gather unique items
    atrributes = True
    while atrributes:
        parts = line.split(" ")
        if len(parts) > 1:
            items.append(parts[1].replace("'", ""))
        else:
            atrributes = False
        line = f.readline()
    while line:
        t = []
        t_items = line.split(',')
        i = 0
        for ti in t_items:
            if ti == "t":
                t.append(items[i])
            i += 1
        transactions.append(t)
        line = f.readline()


with open(os.path.join(dir_path, r'ds4.txt'), 'w') as f:
    for t in range(len(transactions)):
        f.write(' '.join(str(x) for x in sorted(transactions[t])))
        f.write('\n')
