import json
file= open("yelp_academic_dataset.json","r")
for line in file:
    open_j = json.loads(line)
    if open_j['type']=='business':
        city=open_j['neighborhoods']['city']
        state= open_j['neighborhoods']['state']

#


