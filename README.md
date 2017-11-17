# Params:
1. Minimum support
2. Minimum confidence
3. Dataset file (input)

# Output
Rules with:
1. Support of (x U y)
2. Confidence
3. lift

# Datasets

## Small 
http://fimi.ua.ac.be/data/retail.dat

## Large
1. https://archive.ics.uci.edu/ml/datasets/Online+Retail

2. Ta-feng dataset: https://sites.google.com/site/dataminingcourse2009/spring2016/annoucement2016/assignment3/D11-02.ZIP
Description:
It contains these files
D11: Transaction data collected in November, 2000
D12: Transaction data collected in December, 2000
D01: Transaction data collected in January, 2001
D02: Transaction data collected in February, 2001
Format of Transaction Data
First line: Column definition in Traditional Chinese
Second line and the rest: data columns separated by ";"
Column definition
Transaction date and time (time invalid and useless)
Customer ID
Age: 10 possible values,
A <25,B 25-29,C 30-34,D 35-39,E 40-44,F 45-49,G 50-54,H 55-59,I 60-64,J >65
Residence Area: 8 possible values, A-F: zipcode area: 105,106,110,114,115,221,G: others, H: Unknown Distance to store, from the closest: 115,221,114,105,106,110
Product subclass
Product ID
Amount
Asset
Sales price
