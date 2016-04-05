import json

ds ={"0": [0, 330.0, 112.0, 110.0], "1": [112.0, 330.0, 112.0, 110.0], "2": [224.0, 330.0, 112.0, 110.0]}

index = 0
new = dict()
for value in ds.values():
    for i in range(3):
        new[str(index)]=value
        index+=1

with open('output.json','w') as f:
    json.dump(new,f)
